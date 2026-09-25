using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;

public class HeadlessBridge
{
    private int _port = 5002;
    private string _apiKey = string.Empty;
    private readonly string _keyFilePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "key.bin");
    private readonly byte[] _entropy = Encoding.UTF8.GetBytes("FingerprintBridgeEntropy_v1");
    private readonly string _serverConfigPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "server.json");
    private string _serverUrl = string.Empty;
    private string _deviceAccessToken = string.Empty;
    private string _deviceRefreshToken = string.Empty;
    private int _serverTargetUserId = 0;
    private readonly string _logFile = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "bridge.log");

    private void Log(string text)
    {
        try
        {
            var dir = Path.GetDirectoryName(_logFile);
            if (!Directory.Exists(dir)) Directory.CreateDirectory(dir!);
            File.AppendAllText(_logFile, $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] {text}{Environment.NewLine}");
        }
        catch { }
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
                Log("Loaded API key from secure storage (headless).");
                return;
            }

            using var rng = RandomNumberGenerator.Create();
            var keyBytes = new byte[32];
            rng.GetBytes(keyBytes);
            _apiKey = Convert.ToBase64String(keyBytes);
            var toProtect = Encoding.UTF8.GetBytes(_apiKey);
            var protectedData = ProtectedData.Protect(toProtect, _entropy, DataProtectionScope.LocalMachine);
            File.WriteAllBytes(_keyFilePath, protectedData);
            Log("Generated and stored new API key securely (headless).");
        }
        catch (Exception ex)
        {
            Log($"API key load/create error (headless): {ex.Message}");
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
                Log("Loaded server config (headless).");
                return;
            }

            _serverUrl = string.Empty;
            _deviceAccessToken = string.Empty;
            _serverTargetUserId = 0;
        }
        catch (Exception ex)
        {
            Log($"Server config load error (headless): {ex.Message}");
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
            Log("Saved server config securely (headless).");
        }
        catch (Exception ex)
        {
            Log($"Server config save error (headless): {ex.Message}");
        }
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

    public async Task StartAsync()
    {
        LoadOrCreateApiKey();
        LoadOrCreateServerConfig();

        var builder = WebApplication.CreateBuilder();
        var app = builder.Build();

        app.Urls.Add($"http://localhost:{_port}");

        app.MapGet("/status", () => Results.Json(new { status = "ok" }));

        app.MapPost("/pair", async (HttpContext context) =>
        {
            // headless: pairing is disabled by default
            return Results.StatusCode((int)HttpStatusCode.Forbidden);
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

        app.MapPost("/match", async (HttpContext context) =>
        {
            if (!context.Request.Headers.TryGetValue("X-API-KEY", out var key2) || key2 != _apiKey)
            {
                return Results.Unauthorized();
            }
            try
            {
                using var doc = await JsonDocument.ParseAsync(context.Request.Body);
                var root = doc.RootElement;
                var probeB64 = root.GetProperty("probe_template").GetString()!;
                var gallery = root.GetProperty("gallery");
                var result = await MatchFingerprintAsync(probeB64, gallery);
                return Results.Json(result);
            }
            catch (Exception ex)
            {
                Log($"Match error: {ex.Message}");
                return Results.Problem(detail: ex.Message);
            }
        });

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

        await app.StartAsync();
        Log($"Headless local API started at http://localhost:{_port}");

        // keep running
        await Task.Delay(Timeout.Infinite);
    }

    private async Task<(bool success, string access, string refresh, int userId, string error)> ExchangeProvisioningTokenAsync(string provisioningToken, string serverUrl, string name, string deviceUrl)
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
            Log("Provisioning exchange succeeded (headless).");
            return (true, access, refresh, userId, null);
        }
        catch (Exception ex)
        {
            return (false, null, null, 0, ex.Message);
        }
    }

    // ScanFingerprintAsync - uses libzkfp SDK v10 via the managed wrapper (libzkfpcsharp.dll)
    // API: Init(), GetDeviceCount(), OpenDevice(int), AcquireFingerprint(IntPtr, byte[], byte[], ref int), CloseDevice(IntPtr), Terminate()
    // BlobToBase64(byte[], int) for base64 conversion
    public async Task<string> ScanFingerprintAsync()
    {
        // Load the managed wrapper
        var managedPath = @"C:\Windows\SysWOW64\libzkfpcsharp.dll";
        if (!File.Exists(managedPath))
        {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            managedPath = Path.Combine(baseDir, "libzkfpcsharp.dll");
        }
        if (!File.Exists(managedPath))
            throw new FileNotFoundException("libzkfpcsharp.dll not found");

        var asm = System.Reflection.Assembly.LoadFrom(managedPath);
        var zkfp = asm.GetType("libzkfpcsharp.zkfp2") ?? asm.GetType("zkfp2");
        if (zkfp == null)
            throw new InvalidOperationException("Cannot find zkfp2 class in libzkfpcsharp.dll");

        Log($"Found SDK class: {zkfp.FullName}");

        // Get method references
        var mInit = zkfp.GetMethod("Init")!;
        var mTerminate = zkfp.GetMethod("Terminate")!;
        var mGetDeviceCount = zkfp.GetMethod("GetDeviceCount")!;
        var mOpenDevice = zkfp.GetMethod("OpenDevice")!;
        var mCloseDevice = zkfp.GetMethod("CloseDevice")!;
        var mAcquire = zkfp.GetMethod("AcquireFingerprint")!;
        var mBlobToBase64 = zkfp.GetMethod("BlobToBase64");
        var mGetParams = zkfp.GetMethod("GetParameters");

        // Init SDK
        int rc = (int)mInit.Invoke(null, null)!;
        Log($"zkfp2.Init() = {rc}");
        if (rc != 0)
            throw new InvalidOperationException($"zkfp2.Init() failed with code {rc}");

        try
        {
            int devCount = (int)mGetDeviceCount.Invoke(null, null)!;
            Log($"GetDeviceCount = {devCount}");
            if (devCount <= 0)
            {
                throw new InvalidOperationException("No fingerprint device found. Is the sensor plugged in?");
            }

            IntPtr handle = (IntPtr)mOpenDevice.Invoke(null, new object[] { 0 })!;
            Log($"OpenDevice returned: {handle}");
            if (handle == IntPtr.Zero)
                throw new InvalidOperationException("OpenDevice(0) returned null handle");

            try
            {
                // Get image dimensions for buffer sizing
                int imgWidth = 0, imgHeight = 0;
                try
                {
                    // parameter code 1=width 2=height
                    var wBuf = new byte[4]; int wSize = 4;
                    var wArgs = new object[] { handle, 1, wBuf, wSize };
                    mGetParams!.Invoke(null, wArgs);
                    wSize = (int)wArgs[3];
                    if (wSize >= 4) imgWidth = BitConverter.ToInt32(wBuf, 0);

                    var hBuf = new byte[4]; int hSize = 4;
                    var hArgs = new object[] { handle, 2, hBuf, hSize };
                    mGetParams.Invoke(null, hArgs);
                    hSize = (int)hArgs[3];
                    if (hSize >= 4) imgHeight = BitConverter.ToInt32(hBuf, 0);
                    Log($"Device image size width={imgWidth} height={imgHeight}");
                }
                catch (Exception ex) { Log($"GetParameters warning: {ex.Message}"); }

                int imgBufSize = imgWidth > 0 && imgHeight > 0 ? imgWidth * imgHeight : 300 * 400;
                var imgBuffer = new byte[imgBufSize];
                var template = new byte[2048];
                int cbCapTmp = 2048;

                // Capture with timeout: poll AcquireFingerprint until success or 20s
                var captured = await Task.Run(() =>
                {
                    var deadline = DateTime.UtcNow.AddSeconds(20);
                    while (DateTime.UtcNow < deadline)
                    {
                        // AcquireFingerprint(IntPtr devHandle, byte[] imgBuffer, byte[] template, ref int size)
                        cbCapTmp = 2048;
                        var args = new object[] { handle, imgBuffer, template, cbCapTmp };
                        int ret = (int)mAcquire.Invoke(null, args)!;
                        cbCapTmp = (int)args[3]; // read back ref param
                        Log($"Acquire returned {ret} cbCapTmp={cbCapTmp}");
                        if (ret == 0)
                            return true;
                        Thread.Sleep(200);
                    }
                    return false;
                });

                if (!captured)
                    throw new TimeoutException("Fingerprint capture timed out (20s). Place your finger on the sensor.");

                // Convert to base64 via SDK or manual
                Log($"Empreinte capturée (lib) length={cbCapTmp}.");
                var finalTemplate = new byte[cbCapTmp];
                Array.Copy(template, finalTemplate, cbCapTmp);

                string b64;
                if (mBlobToBase64 != null)
                {
                    b64 = (string)mBlobToBase64.Invoke(null, new object[] { finalTemplate, cbCapTmp })!;
                }
                else
                {
                    b64 = Convert.ToBase64String(finalTemplate);
                }
                return b64;
            }
            finally
            {
                try { mCloseDevice.Invoke(null, new object[] { handle }); Log("Device closed"); } catch { }
            }
        }
        finally
        {
            try { mTerminate.Invoke(null, null); } catch { }
        }
    }

    /// <summary>
    /// Match a probe fingerprint template against a gallery of stored templates using
    /// the ZKTeco SDK DBMatch function (biometric 1:N matching).
    /// </summary>
    public async Task<object> MatchFingerprintAsync(string probeB64, JsonElement gallery)
    {
        var managedPath = @"C:\Windows\SysWOW64\libzkfpcsharp.dll";
        if (!File.Exists(managedPath))
        {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            managedPath = Path.Combine(baseDir, "libzkfpcsharp.dll");
        }
        if (!File.Exists(managedPath))
            throw new FileNotFoundException("libzkfpcsharp.dll not found");

        var asm = System.Reflection.Assembly.LoadFrom(managedPath);
        var zkfp = asm.GetType("libzkfpcsharp.zkfp2") ?? asm.GetType("zkfp2");
        if (zkfp == null)
            throw new InvalidOperationException("Cannot find zkfp2 class in libzkfpcsharp.dll");

        var mInit = zkfp.GetMethod("Init")!;
        var mTerminate = zkfp.GetMethod("Terminate")!;
        var mDBInit = zkfp.GetMethod("DBInit");
        var mDBFree = zkfp.GetMethod("DBFree");
        var mDBMatch = zkfp.GetMethod("DBMatch");
        var mBase64ToBlob = zkfp.GetMethod("Base64ToBlob");

        if (mDBInit == null || mDBFree == null || mDBMatch == null)
            throw new InvalidOperationException("SDK matching functions not found (DBInit/DBFree/DBMatch)");

        // Init SDK (needed for algorithm functions)
        int rc = (int)mInit.Invoke(null, null)!;
        Log($"Match: zkfp2.Init() = {rc}");
        if (rc != 0)
            throw new InvalidOperationException($"zkfp2.Init() failed with code {rc}");

        try
        {
            IntPtr dbHandle = (IntPtr)mDBInit.Invoke(null, null)!;
            Log($"Match: DBInit handle = {dbHandle}");
            if (dbHandle == IntPtr.Zero)
                throw new InvalidOperationException("DBInit failed (returned null handle)");

            try
            {
                // Convert probe from base64 to byte[]
                byte[] probeBytes;
                if (mBase64ToBlob != null)
                {
                    probeBytes = (byte[])mBase64ToBlob.Invoke(null, new object[] { probeB64 })!;
                }
                else
                {
                    probeBytes = Convert.FromBase64String(probeB64);
                }
                Log($"Match: probe size = {probeBytes.Length}");

                int bestScore = 0;
                int bestId = -1;

                foreach (var item in gallery.EnumerateArray())
                {
                    int id = item.GetProperty("id").GetInt32();
                    string tplB64 = item.GetProperty("template_b64").GetString()!;

                    byte[] galleryBytes;
                    if (mBase64ToBlob != null)
                    {
                        galleryBytes = (byte[])mBase64ToBlob.Invoke(null, new object[] { tplB64 })!;
                    }
                    else
                    {
                        galleryBytes = Convert.FromBase64String(tplB64);
                    }

                    int score = (int)mDBMatch.Invoke(null, new object[] { dbHandle, probeBytes, galleryBytes })!;
                    Log($"Match: id={id} score={score}");

                    if (score > bestScore)
                    {
                        bestScore = score;
                        bestId = id;
                    }
                }

                if (bestScore > 0 && bestId >= 0)
                {
                    Log($"Match: FOUND id={bestId} score={bestScore}");
                    return new { matched = true, empreinte_id = bestId, score = bestScore };
                }

                Log("Match: no match found");
                return new { matched = false, empreinte_id = -1, score = 0 };
            }
            finally
            {
                try { mDBFree.Invoke(null, new object[] { dbHandle }); } catch { }
            }
        }
        finally
        {
            try { mTerminate.Invoke(null, null); } catch { }
        }
    }

    public async Task<bool> UploadTemplateToServerAsync(string base64Template)
    {
        if (string.IsNullOrEmpty(_serverUrl) || string.IsNullOrEmpty(_deviceAccessToken))
        {
            Log("Server URL or device token not configured (headless).");
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
                Log("Upload unauthorized. Attempting to refresh access token (headless)...");
                var refreshed = await RefreshAccessTokenAsync();
                if (!refreshed)
                {
                    Log("Token refresh failed; aborting upload (headless).");
                    return false;
                }
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _deviceAccessToken);
                res = await client.PostAsync($"{_serverUrl.TrimEnd('/')}/api/empreintes/", new StringContent(json, Encoding.UTF8, "application/json"));
                body = await res.Content.ReadAsStringAsync();
            }

            if (!res.IsSuccessStatusCode)
            {
                Log($"Server upload failed (headless): {res.StatusCode} {body}");
                return false;
            }
            return true;
        }
        catch (Exception ex)
        {
            Log($"Upload error (headless): {ex.Message}");
            return false;
        }
    }

    private async Task<bool> RefreshAccessTokenAsync()
    {
        if (string.IsNullOrEmpty(_deviceRefreshToken) || string.IsNullOrEmpty(_serverUrl))
        {
            Log("No refresh token available (headless).");
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
                Log($"Refresh failed (headless): {res.StatusCode} {body}");
                return false;
            }
            using var doc = JsonDocument.Parse(body);
            var root = doc.RootElement;
            var access = root.TryGetProperty("access", out var a) ? a.GetString() ?? string.Empty : string.Empty;
            if (!string.IsNullOrEmpty(access))
            {
                _deviceAccessToken = access;
                SaveServerConfig(_serverUrl, _deviceAccessToken, _serverTargetUserId, _deviceRefreshToken);
                Log("Access token refreshed (headless).");
                return true;
            }
            return false;
        }
        catch (Exception ex)
        {
            Log($"Refresh error (headless): {ex.Message}");
            return false;
        }
    }
}
