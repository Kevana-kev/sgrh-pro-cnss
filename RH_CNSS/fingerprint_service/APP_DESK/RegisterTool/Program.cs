using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class Program
{
    static async Task<int> Main(string[] args)
    {
        Console.WriteLine("Device Register Tool");
        Console.Write("Backend base URL (https://...): ");
        var baseUrl = Console.ReadLine()?.Trim();
        if (string.IsNullOrEmpty(baseUrl)) { Console.WriteLine("base URL required"); return 1; }

        Console.Write("Admin email: ");
        var email = Console.ReadLine()?.Trim();
        Console.Write("Admin password: ");
        var password = ReadPassword();

        var adminToken = await GetAdminToken(baseUrl, email, password);
        if (adminToken == null) { Console.WriteLine("Failed to obtain admin token"); return 1; }

        Console.Write("Device local URL (default http://localhost:5002): ");
        var deviceUrl = Console.ReadLine();
        if (string.IsNullOrEmpty(deviceUrl)) deviceUrl = "http://localhost:5002";

        // call local pairing endpoint to get local API key (requires user approval on device)
        Console.WriteLine("Requesting local pairing (device will prompt user)...");
        var localApiKey = await RequestLocalPairing(deviceUrl);
        if (localApiKey == null) { Console.WriteLine("Pairing failed or not approved"); return 1; }
        Console.WriteLine("Local API key received.");

        Console.Write("Device name (for server): ");
        var deviceName = Console.ReadLine();

        // call server pairing
        var pairResp = await PostServerPair(baseUrl, adminToken, deviceName, deviceUrl, localApiKey);
        if (pairResp == null) { Console.WriteLine("Server pairing failed"); return 1; }

        Console.WriteLine("Device registered on server:");
        Console.WriteLine(JsonSerializer.Serialize(pairResp, new JsonSerializerOptions { WriteIndented = true }));

        // configure local device with server info
        Console.Write("Target utilisateur_id for automatic upload (enter an integer): ");
        var uidStr = Console.ReadLine();
        if (!int.TryParse(uidStr, out var userId) || userId <= 0)
        {
            Console.WriteLine("Invalid user id; skipping local configuration.");
            return 0;
        }

        var access = pairResp.Value.GetProperty("access").GetString();
        if (string.IsNullOrEmpty(access)) { Console.WriteLine("No access token returned"); return 1; }

        var configured = await ConfigureLocalDevice(deviceUrl, localApiKey, baseUrl, access, userId);
        Console.WriteLine(configured ? "Local device configured." : "Failed to configure local device.");

        return 0;
    }

    static string ReadPassword()
    {
        var sb = new StringBuilder();
        ConsoleKeyInfo key;
        while ((key = Console.ReadKey(true)).Key != ConsoleKey.Enter)
        {
            if (key.Key == ConsoleKey.Backspace && sb.Length > 0)
            {
                sb.Length -= 1;
                Console.Write("\b \b");
            }
            else if (!char.IsControl(key.KeyChar))
            {
                sb.Append(key.KeyChar);
                Console.Write("*");
            }
        }
        Console.WriteLine();
        return sb.ToString();
    }

    static async Task<string?> GetAdminToken(string baseUrl, string email, string password)
    {
        try
        {
            using var client = new HttpClient();
            var payload = new { email = email, password = password };
            var json = JsonSerializer.Serialize(payload);
            var res = await client.PostAsync($"{baseUrl.TrimEnd('/')}/api/token/", new StringContent(json, Encoding.UTF8, "application/json"));
            var body = await res.Content.ReadAsStringAsync();
            if (!res.IsSuccessStatusCode) { Console.WriteLine(body); return null; }
            var doc = JsonDocument.Parse(body).RootElement;
            return doc.GetProperty("access").GetString();
        }
        catch (Exception ex) { Console.WriteLine(ex.Message); return null; }
    }

    static async Task<string?> RequestLocalPairing(string deviceUrl)
    {
        try
        {
            using var client = new HttpClient();
            var payload = new { appName = "ServerRegisterTool" };
            var res = await client.PostAsync($"{deviceUrl.TrimEnd('/')}/pair", new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json"));
            var body = await res.Content.ReadAsStringAsync();
            if (!res.IsSuccessStatusCode) { Console.WriteLine(body); return null; }
            var doc = JsonDocument.Parse(body).RootElement;
            return doc.GetProperty("apiKey").GetString();
        }
        catch (Exception ex) { Console.WriteLine(ex.Message); return null; }
    }

    static async Task<JsonElement?> PostServerPair(string baseUrl, string adminToken, string name, string deviceUrl, string apiKey)
    {
        try
        {
            using var client = new HttpClient();
            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", adminToken);
            var payload = new { name = name, device_url = deviceUrl, api_key = apiKey };
            var res = await client.PostAsync($"{baseUrl.TrimEnd('/')}/api/devices/pair/", new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json"));
            var body = await res.Content.ReadAsStringAsync();
            if (!res.IsSuccessStatusCode) { Console.WriteLine(body); return null; }
            var doc = JsonDocument.Parse(body).RootElement;
            return doc;
        }
        catch (Exception ex) { Console.WriteLine(ex.Message); return null; }
    }

    static async Task<bool> ConfigureLocalDevice(string deviceUrl, string localApiKey, string serverUrl, string accessToken, int userId)
    {
        try
        {
            using var client = new HttpClient();
            client.DefaultRequestHeaders.Add("X-API-KEY", localApiKey);
            var payload = new { serverUrl = serverUrl, accessToken = accessToken, userId = userId };
            var res = await client.PostAsync($"{deviceUrl.TrimEnd('/')}/configure-server", new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json"));
            var body = await res.Content.ReadAsStringAsync();
            if (!res.IsSuccessStatusCode) { Console.WriteLine(body); return false; }
            return true;
        }
        catch (Exception ex) { Console.WriteLine(ex.Message); return false; }
    }
}
