using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace FingerprintBridgeApp
{
    public class DeviceUploader
    {
        private readonly HttpClient _http;
        private readonly string _baseUrl;

        public DeviceUploader(string baseUrl)
        {
            _baseUrl = baseUrl.TrimEnd('/');
            _http = new HttpClient();
        }

        // Create device using an admin JWT token. Returns access and refresh tokens for the device.
        public async Task<JsonElement?> RegisterDeviceAsync(string adminJwt, string deviceName)
        {
            _http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", adminJwt);
            var payload = new { name = deviceName };
            var json = JsonSerializer.Serialize(payload);
            var resp = await _http.PostAsync($"{_baseUrl}/api/devices/", new StringContent(json, Encoding.UTF8, "application/json"));
            var body = await resp.Content.ReadAsStringAsync();
            if (!resp.IsSuccessStatusCode)
            {
                Console.WriteLine("Device registration failed: " + body);
                return null;
            }
            var doc = JsonSerializer.Deserialize<JsonElement>(body);
            return doc;
        }

        // Upload a base64-encoded template as an 'empreinte' for a given utilisateur_id
        public async Task<bool> UploadTemplateAsync(string accessToken, int utilisateurId, string base64Template, int fingerIndex = 0)
        {
            _http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);
            var payload = new
            {
                utilisateur_id = utilisateurId,
                template_biometrique = base64Template,
                finger_index = fingerIndex,
                actif = true
            };
            var json = JsonSerializer.Serialize(payload);
            var resp = await _http.PostAsync($"{_baseUrl}/api/empreintes/", new StringContent(json, Encoding.UTF8, "application/json"));
            var body = await resp.Content.ReadAsStringAsync();
            if (!resp.IsSuccessStatusCode)
            {
                Console.WriteLine("Upload failed: " + body);
            }
            return resp.IsSuccessStatusCode;
        }
    }
}
