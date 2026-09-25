using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;

public partial class MainForm : Form
{
    private IHost? _webHost;
    private WebApplication? _webApp;
    private int _port = 5002;
    private string _apiKey = string.Empty;
    private readonly string _keyFilePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "key.bin");

    private readonly byte[] _entropy = Encoding.UTF8.GetBytes("FingerprintBridgeEntropy_v1");
    private readonly string _serverConfigPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "server.json");
    private string _serverUrl = string.Empty;
    private string _deviceAccessToken = string.Empty;
    private string _deviceRefreshToken = string.Empty;
    private int _serverTargetUserId = 0;

    public MainForm()
    {
        InitializeComponent();
        LoadOrCreateApiKey();
        LoadOrCreateServerConfig();
        StartLocalApi();
    }

    private Task<object?> RunInSta(Func<object?> func)
    {
        var tcs = new TaskCompletionSource<object?>();
        var thread = new Thread(() =>
        {
            try
            {
                var res = func();
                tcs.SetResult(res);
            }
            catch (Exception ex)
            {
                tcs.SetException(ex);
            }
        });
        thread.SetApartmentState(ApartmentState.STA);
        thread.IsBackground = true;
        thread.Start();
        return tcs.Task;
    }

    private void LoadOrCreateApiKey()
    {
        try
        {
            var dir = Path.GetDirectoryName(_keyFilePath);
            if (!Directory.Exists(dir)) Directory.CreateDirectory(dir!);

            if (File.Exists(_keyFilePath))
            {
                var protectedBytes = File.ReadAllBytes(_keyFilePath);
                var bytes = ProtectedData.Unprotect(protectedBytes, _entropy, DataProtectionScope.LocalMachine);
                _apiKey = Encoding.UTF8.GetString(bytes);
                Log("Loaded API key from secure storage.");
                return;
            }

            // create a new random API key
            using var rng = RandomNumberGenerator.Create();
            var keyBytes = new byte[32];
            rng.GetBytes(keyBytes);
            _apiKey = Convert.ToBase64String(keyBytes);
            var toProtect = Encoding.UTF8.GetBytes(_apiKey);
            var protectedData = ProtectedData.Protect(toProtect, _entropy, DataProtectionScope.LocalMachine);
            File.WriteAllBytes(_keyFilePath, protectedData);
            Log("Generated and stored new API key securely.");
        }
        catch (Exception ex)
        {
            Log($"API key load/create error: {ex.Message}");
            // fallback to in-memory key
            _apiKey = "local-secret-key";
        }
    }

    private void LoadOrCreateServerConfig()
    {
        try
        {
            var dir = Path.GetDirectoryName(_serverConfigPath);
            if (!Directory.Exists(dir)) Directory.CreateDirectory(dir!);

            if (File.Exists(_serverConfigPath))
            {
                var protectedBytes = File.ReadAllBytes(_serverConfigPath);
                var bytes = ProtectedData.Unprotect(protectedBytes, _entropy, DataProtectionScope.LocalMachine);
                var json = Encoding.UTF8.GetString(bytes);
                using var doc = JsonDocument.Parse(json);
                var root = doc.RootElement;
                _serverUrl = root.TryGetProperty("serverUrl", out var s) ? s.GetString() ?? string.Empty : string.Empty;
                _deviceAccessToken = root.TryGetProperty("accessToken", out var t) ? t.GetString() ?? string.Empty : string.Empty;
                _deviceRefreshToken = root.TryGetProperty("refreshToken", out var r) ? r.GetString() ?? string.Empty : string.Empty;
                _serverTargetUserId = root.TryGetProperty("userId", out var u) && u.TryGetInt32(out var id) ? id : 0;
                Log("Loaded server config.");
                return;
            }

            // no config yet
            _serverUrl = string.Empty;
            _deviceAccessToken = string.Empty;
            _serverTargetUserId = 0;
        }
        catch (Exception ex)
        {
            Log($"Server config load error: {ex.Message}");
            _serverUrl = string.Empty;
            _deviceAccessToken = string.Empty;
            _serverTargetUserId = 0;
        }
    }

    private void SaveServerConfig(string serverUrl, string accessToken, int userId, string refreshToken = null)
    {
        try
        {
            var dir = Path.GetDirectoryName(_serverConfigPath);
            if (!Directory.Exists(dir)) Directory.CreateDirectory(dir!);
            var json = JsonSerializer.Serialize(new { serverUrl, accessToken, refreshToken = refreshToken ?? string.Empty, userId });
            var bytes = Encoding.UTF8.GetBytes(json);
            var protectedData = ProtectedData.Protect(bytes, _entropy, DataProtectionScope.LocalMachine);
            File.WriteAllBytes(_serverConfigPath, protectedData);
            _serverUrl = serverUrl; _deviceAccessToken = accessToken; _serverTargetUserId = userId;
            if (!string.IsNullOrEmpty(refreshToken)) _deviceRefreshToken = refreshToken;
            Log("Saved server config securely.");
        }
        catch (Exception ex)
        {
            Log($"Server config save error: {ex.Message}");
        }
    }

    private async Task<bool> AskUserToApprovePairing(string appName)
    {
        var tcs = new TaskCompletionSource<bool>();
        if (InvokeRequired)
        {
            BeginInvoke(new Action(async () => tcs.SetResult(ShowPairingDialog(appName))));
        }
        else
        {
            tcs.SetResult(ShowPairingDialog(appName));
        }
        return await tcs.Task;
    }

    private bool ShowPairingDialog(string appName)
    {
        var msg = $"A web application named '{appName}' is requesting to pair with this fingerprint bridge. Approve?";
        var r = MessageBox.Show(this, msg, "Approve pairing", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
        return r == DialogResult.Yes;
    }

    private void StartLocalApi()
    {
        // Use minimal WebApplication for .NET 7
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddRouting();
        var app = builder.Build();
        _webApp = app;

        app.Urls.Add($"http://localhost:{_port}");

        app.MapGet("/status", () => Results.Json(new { status = "ok" }));

        // Pairing endpoint: webapp can request pairing; UI will ask user to approve and will return API key if approved.
        app.MapPost("/pair", async (HttpContext context) =>
        {
            try
            {
                using var doc = await JsonDocument.ParseAsync(context.Request.Body);
                var root = doc.RootElement;
                var appName = root.TryGetProperty("appName", out var a) ? a.GetString() : "Unknown";

                var approved = await AskUserToApprovePairing(appName ?? "Unknown");
                if (!approved)
                {
                    return Results.StatusCode((int)HttpStatusCode.Forbidden);
                }

                // return API key to the caller (only after explicit user approval)
                return Results.Json(new { apiKey = _apiKey });
            }
            catch (Exception ex)
            {
                return Results.Problem(detail: ex.Message);
            }
        });

        app.MapPost("/scan", async (HttpContext context) =>
        {
            if (!context.Request.Headers.TryGetValue("X-API-KEY", out var key) || key != _apiKey)
            {
                return Results.Unauthorized();
            }

            try
            {
                var templateB64 = await ScanFingerprintAsync();
                return Results.Json(new { template = templateB64 });
            }
            catch (Exception ex)
            {
                return Results.Problem(detail: ex.Message);
            }
        });

        // configure remote server (requires local API key)
        app.MapPost("/configure-server", async (HttpContext context) =>
        {
            if (!context.Request.Headers.TryGetValue("X-API-KEY", out var key) || key != _apiKey)
            {
                return Results.Unauthorized();
            }
            try
            {
                using var doc = await JsonDocument.ParseAsync(context.Request.Body);
                var root = doc.RootElement;
                var serverUrl = root.TryGetProperty("serverUrl", out var s) ? s.GetString() ?? string.Empty : string.Empty;
                var accessToken = root.TryGetProperty("accessToken", out var t) ? t.GetString() ?? string.Empty : string.Empty;
                var refreshToken = root.TryGetProperty("refreshToken", out var r) ? r.GetString() ?? string.Empty : string.Empty;
                var userId = root.TryGetProperty("userId", out var u) && u.TryGetInt32(out var id) ? id : 0;
                var provisioningToken = root.TryGetProperty("provisioningToken", out var p) ? p.GetString() ?? string.Empty : string.Empty;
                var deviceName = root.TryGetProperty("name", out var n) ? n.GetString() ?? "provisioned-device" : "provisioned-device";
                var deviceUrl = root.TryGetProperty("deviceUrl", out var d) ? d.GetString() : null;

                if (string.IsNullOrEmpty(serverUrl))
                {
                    return Results.BadRequest(new { error = "serverUrl is required" });
                }

                // If provisioning token provided, call server to exchange it for tokens
                if (!string.IsNullOrEmpty(provisioningToken))
                {
                    var exch = await ExchangeProvisioningTokenAsync(provisioningToken, serverUrl, deviceName, deviceUrl);
                    if (!exch.success)
                    {
                        return Results.Json(new { error = exch.error }, statusCode: (int)HttpStatusCode.BadGateway);
                    }
                    accessToken = exch.access;
                    refreshToken = exch.refresh;
                    userId = exch.userId;
                }

                if (string.IsNullOrEmpty(accessToken) || userId == 0)
                {
                    return Results.BadRequest(new { error = "accessToken and userId are required (or provide provisioningToken)" });
                }

                // enforce HTTPS for non-local server URLs
                var lower = serverUrl.ToLowerInvariant();
                var isLocal = lower.Contains("localhost") || lower.Contains("127.0.0.1") || lower.StartsWith("http://192.") || lower.StartsWith("http://10.") || lower.StartsWith("http://172.");
                if (!lower.StartsWith("https://") && !isLocal)
                {
                    return Results.BadRequest(new { error = "serverUrl must use https in production" });
                }

                SaveServerConfig(serverUrl, accessToken, userId, string.IsNullOrEmpty(refreshToken) ? null : refreshToken);
                return Results.Ok(new { status = "saved" });
            }
            catch (Exception ex)
            {
                return Results.Problem(detail: ex.Message);
            }
        });

        // Helper: call backend provisioning exchange endpoint
        async Task<(bool success, string access, string refresh, int userId, string error)> ExchangeProvisioningTokenAsync(string provisioningToken, string serverUrl, string name, string deviceUrl)
        {
            try
            {
                using var client = new HttpClient();
                var payload = new { token = provisioningToken, name = name, device_url = deviceUrl };
                var json = JsonSerializer.Serialize(payload);
                var res = await client.PostAsync($"{serverUrl.TrimEnd('/')}/api/provisioning/exchange/", new StringContent(json, Encoding.UTF8, "application/json"));
                var body = await res.Content.ReadAsStringAsync();
                if (!res.IsSuccessStatusCode)
                {
                    return (false, null, null, 0, $"exchange failed: {res.StatusCode} {body}");
                }
                using var doc = JsonDocument.Parse(body);
                var root = doc.RootElement;
                var access = root.TryGetProperty("access", out var a) ? a.GetString() ?? string.Empty : string.Empty;
                var refresh = root.TryGetProperty("refresh", out var r) ? r.GetString() ?? string.Empty : string.Empty;
                var userId = root.TryGetProperty("user_id", out var uid) && uid.TryGetInt32(out var id) ? id : 0;
                if (string.IsNullOrEmpty(access) || string.IsNullOrEmpty(refresh) || userId == 0)
                {
                    return (false, null, null, 0, $"invalid exchange response: {body}");
                }
                Log("Provisioning exchange succeeded.");
                return (true, access, refresh, userId, null);
            }
            catch (Exception ex)
            {
                return (false, null, null, 0, ex.Message);
            }
        }

        Task.Run(async () =>
        {
            await app.StartAsync();
        });

        Log($"Local API started at http://localhost:{_port}");
        Log($"API key stored securely at: {_keyFilePath}");
    }

    protected override void OnFormClosed(FormClosedEventArgs e)
    {
        base.OnFormClosed(e);
        if (_webApp != null)
        {
            _webApp.StopAsync().GetAwaiter().GetResult();
            if (_webApp is IAsyncDisposable ad)
            {
                ad.DisposeAsync().AsTask().GetAwaiter().GetResult();
            }
        }
    }

    // Placeholder: call SDK to scan and return template/base64
    public async Task<string> ScanFingerprintAsync()
    {
        // Attempt to load the interop assembly provided by the SDK and call a known method.
        // This is a best-effort reflection-based integration. If your SDK exposes
        // a documented .NET type or method (recommended), replace this implementation
        // with direct calls to that API.

        var baseDir = AppDomain.CurrentDomain.BaseDirectory;
        var asmPath = Path.Combine(baseDir, "Interop.ZKFPEngXControl.dll");
        if (!File.Exists(asmPath))
        {
            throw new FileNotFoundException($"SDK interop assembly not found: {asmPath}");
        }

        var asm = System.Reflection.Assembly.LoadFrom(asmPath);

        // First attempt: instantiate SDK as a COM/ActiveX object (requires STA).
        var progids = new[] { "ZKFPEngX.ZKFPEngX", "ZKFPEngX.ZKFPEngXCtrl", "ZKFPEngXControl.ZKFPEngXCtrl", "ZKFPEngXControl.ZKFPEngX" };
        string[] methodNames = new[] { "GetRegisterTemplate", "GetTemplateAsString", "GetTemplate", "GetBase64Template", "GetBiometricTemplate" };

        foreach (var progid in progids)
        {
            try
            {
                var t = Type.GetTypeFromProgID(progid);
                if (t == null) continue;

                // COM objects often require STA � run in STA thread
                var result = await RunInSta(() =>
                {
                    var inst = Activator.CreateInstance(t);
                    foreach (var name in methodNames)
                    {
                        var m = t.GetMethod(name, System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.IgnoreCase);
                        if (m != null && m.GetParameters().Length == 0)
                        {
                            var res = m.Invoke(inst, null);
                            return res;
                        }
                    }
                    return null;
                });

                if (result is byte[] bb) return Convert.ToBase64String(bb);
                if (result is string ss)
                {
                    try { Convert.FromBase64String(ss); return ss; }
                    catch { return Convert.ToBase64String(Encoding.UTF8.GetBytes(ss)); }
                }
            }
            catch { /* try next */ }
        }

        // Second attempt: reflection against Interop/AxInterop assembly types
        foreach (var type in asm.GetExportedTypes())
        {
            // Skip interfaces and abstract classes – they cannot be instantiated
            if (type.IsInterface || type.IsAbstract) continue;

            foreach (var name in methodNames)
            {
                var m = type.GetMethod(name, System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.IgnoreCase);
                if (m != null && m.GetParameters().Length == 0)
                {
                    var inst = Activator.CreateInstance(type);
                    var res = m.Invoke(inst, null);
                    if (res is byte[] b) return Convert.ToBase64String(b);
                    if (res is string s)
                    {
                        try { Convert.FromBase64String(s); return s; }
                        catch { return Convert.ToBase64String(Encoding.UTF8.GetBytes(s)); }
                    }
                }
            }
        }

        // If we reach here, we couldn't find an automated reflection call.
        // The SDK likely requires using an ActiveX WinForms control or explicit P/Invoke.
        // Provide an informative error so you can wire the correct calls.
        throw new InvalidOperationException("Could not auto-detect SDK method. Please update 'ScanFingerprintAsync' to call the correct SDK API (e.g. using the provided AxInterop/Interop types or P/Invoke). Look into the SDK folder and documentation for method names like GetTemplate/GetRegisterTemplate.");
    }

    private void Log(string text)
    {
        if (InvokeRequired)
        {
            BeginInvoke(new Action(() => Log(text)));
            return;
        }
        txtLog.AppendText($"[{DateTime.Now:HH:mm:ss}] {text}{Environment.NewLine}");
    }

    private async void BtnScan_Click(object sender, EventArgs e)
    {
        Log("Manual scan requested...");
        try
        {
            var tpl = await ScanFingerprintAsync();
            Log($"Template: {tpl}");
            // if server config present, upload automatically
            if (!string.IsNullOrEmpty(_deviceAccessToken) && !string.IsNullOrEmpty(_serverUrl) && _serverTargetUserId > 0)
            {
                var ok = await UploadTemplateToServerAsync(tpl);
                Log(ok ? "Uploaded template to server." : "Failed to upload template to server.");
            }
        }
        catch (Exception ex)
        {
            Log($"Scan error: {ex.Message}");
        }
    }

    // Upload the base64 template to configured Django backend
    public async Task<bool> UploadTemplateToServerAsync(string base64Template)
    {
        if (string.IsNullOrEmpty(_serverUrl) || string.IsNullOrEmpty(_deviceAccessToken))
        {
            Log("Server URL or device token not configured.");
            return false;
        }

        try
        {
            using var client = new HttpClient();
            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _deviceAccessToken);
            var payload = new
            {
                utilisateur_id = _serverTargetUserId,
                template_biometrique = base64Template,
                finger_index = 0,
                actif = true
            };
            var json = JsonSerializer.Serialize(payload);
            var res = await client.PostAsync($"{_serverUrl.TrimEnd('/')}/api/empreintes/", new StringContent(json, Encoding.UTF8, "application/json"));
            var body = await res.Content.ReadAsStringAsync();

            if (res.StatusCode == HttpStatusCode.Unauthorized)
            {
                Log("Upload unauthorized. Attempting to refresh access token...");
                var refreshed = await RefreshAccessTokenAsync();
                if (!refreshed)
                {
                    Log("Token refresh failed; aborting upload.");
                    return false;
                }
                // retry once with new token
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _deviceAccessToken);
                res = await client.PostAsync($"{_serverUrl.TrimEnd('/')}/api/empreintes/", new StringContent(json, Encoding.UTF8, "application/json"));
                body = await res.Content.ReadAsStringAsync();
            }

            if (!res.IsSuccessStatusCode)
            {
                Log($"Server upload failed: {res.StatusCode} {body}");
                return false;
            }
            return true;
        }
        catch (Exception ex)
        {
            Log($"Upload error: {ex.Message}");
            return false;
        }
    }

    private async Task<bool> RefreshAccessTokenAsync()
    {
        if (string.IsNullOrEmpty(_deviceRefreshToken) || string.IsNullOrEmpty(_serverUrl))
        {
            Log("No refresh token available.");
            return false;
        }

        try
        {
            using var client = new HttpClient();
            var payload = JsonSerializer.Serialize(new { refresh = _deviceRefreshToken });
            var res = await client.PostAsync($"{_serverUrl.TrimEnd('/')}/api/token/refresh/", new StringContent(payload, Encoding.UTF8, "application/json"));
            var body = await res.Content.ReadAsStringAsync();
            if (!res.IsSuccessStatusCode)
            {
                Log($"Refresh failed: {res.StatusCode} {body}");
                return false;
            }
            using var doc = JsonDocument.Parse(body);
            var root = doc.RootElement;
            var access = root.TryGetProperty("access", out var a) ? a.GetString() ?? string.Empty : string.Empty;
            if (!string.IsNullOrEmpty(access))
            {
                _deviceAccessToken = access;
                SaveServerConfig(_serverUrl, _deviceAccessToken, _serverTargetUserId, _deviceRefreshToken);
                Log("Access token refreshed.");
                return true;
            }
            return false;
        }
        catch (Exception ex)
        {
            Log($"Refresh error: {ex.Message}");
            return false;
        }
    }
}
