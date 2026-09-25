using System;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Text.Json;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;

public partial class MainForm : Form
{
    private WebApplication? _webApp;
    private int _port = 5002;
    private string _apiKey = string.Empty;
    private bool _autoMode = false;
    private readonly string _keyFilePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "key.bin");

    private readonly byte[] _entropy = Encoding.UTF8.GetBytes("FingerprintBridgeEntropy_v1");

    public MainForm()
    {
        InitializeComponent();
        LoadOrCreateApiKey();
        try
        {
            var autoFlagPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge", "auto.enable");
            _autoMode = Environment.GetEnvironmentVariable("FINGERPRINT_BRIDGE_AUTO") == "1" || File.Exists(autoFlagPath);
            if (_autoMode) Log("Auto mode enabled: pairing and scans will proceed without user interaction.");
        }
        catch { }
        StartLocalApi();
        // Start an initial automatic scan only if explicitly allowed via env var
        if (_autoMode && Environment.GetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_AUTO_SCAN") == "1")
        {
            StartInitialScan();
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

    private Task<bool> AskUserToApprovePairing(string appName)
    {
        if (_autoMode)
        {
            // Auto-approve only if explicitly enabled via environment
            if (Environment.GetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_AUTO_APPROVE") == "1")
            {
                Log($"Auto-approve pairing for {appName}");
                return Task.FromResult(true);
            }
        }
        var tcs = new TaskCompletionSource<bool>();
        if (InvokeRequired)
        {
            BeginInvoke(new Action(async () => tcs.SetResult(ShowPairingDialog(appName))));
        }
        else
        {
            tcs.SetResult(ShowPairingDialog(appName));
        }
        return tcs.Task;
    }

    private bool ShowPairingDialog(string appName)
    {
        var msg = $"A web application named '{appName}' is requesting to pair with this fingerprint bridge. Approve?";
        var r = MessageBox.Show(this, msg, "Approve pairing", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
        return r == DialogResult.Yes;
    }

    private Task<bool> AskUserToPlaceFingerAsync()
    {
        // Removed confirmation dialog. Start capture immediately without requiring user to click OK.
        Log("Starting capture immediately (no OK confirmation).");
        return Task.FromResult(true);
    }

    private bool ShowPlaceFingerDialog()
    {
        // Confirmation removed; keep method for compatibility but do not block.
        return true;
    }

    private void ShowCaptureSuccess()
    {
        if (InvokeRequired)
        {
            BeginInvoke(new Action(() => MessageBox.Show(this, "Empreinte capturée.", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information)));
        }
        else
        {
            MessageBox.Show(this, "Empreinte capturée.", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
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

    // Enhanced: prompt user, wait for finger placement, then capture (libzkfpcsharp or ActiveX)
    public async Task<string> ScanFingerprintAsync()
    {
        Log("Veuillez poser votre doigt sur le capteur...");
        if (_autoMode)
        {
            // Return mock template in auto-mode only when explicitly allowed
            if (Environment.GetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_MOCK") == "1")
            {
                Log("Auto-mode enabled: returning mock template without waiting for finger.");
                return Convert.ToBase64String(Encoding.UTF8.GetBytes("mock-template"));
            }
            else
            {
                Log("Auto-mode enabled but mock templates are disabled. Proceeding with normal capture.");
            }
        }
        // Show modal dialog so user explicitly places finger when ready
        var userOk = await AskUserToPlaceFingerAsync();
        if (!userOk)
        {
            Log("Scan annulé par l'utilisateur.");
            throw new OperationCanceledException("User cancelled scan");
        }
        var maxWaitMs = 30_000; // wait up to 30 seconds for a finger
        var pollMs = 250;

        // Try direct SDK wrapper (libzkfpcsharp) first with additional diagnostics
        try
        {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;
            Log($"libzkfpcsharp probe baseDir: {baseDir}");
            var sdkRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "..", "ZKFinger Standard SDK 5.3.0.33", "C#", "lib"));
            var arch = IntPtr.Size == 8 ? "x64" : "x86";
            var libName = "libzkfpcsharp.dll";
            var libPath = Path.Combine(sdkRoot, arch, libName);

            Log($"Trying lib path: {libPath}");
            if (!File.Exists(libPath))
            {
                libPath = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "ZKFinger Standard SDK 5.3.0.33", "C#", "lib", arch, libName));
                Log($"Trying fallback lib path: {libPath}");
            }

            var localPath = Path.Combine(baseDir, libName);
            Log($"Also checking local path: {localPath}");
            if (File.Exists(localPath) && !File.Exists(libPath))
            {
                Log($"Found local lib at: {localPath} (using it)");
                libPath = localPath;
            }

            if (!File.Exists(libPath))
            {
                Log("libzkfpcsharp.dll not found in probing paths.");
            }
            else
            {
                try
                {
                    var libAsm = System.Reflection.Assembly.LoadFrom(libPath);
                    Log($"Loaded lib assembly from {libPath}");
                    var zkfp2Type = libAsm.GetTypes().FirstOrDefault(t => string.Equals(t.Name, "zkfp2", StringComparison.OrdinalIgnoreCase));
                    var zkfpErrType = libAsm.GetTypes().FirstOrDefault(t => t.Name.IndexOf("errdef", StringComparison.OrdinalIgnoreCase) >= 0 || t.Name.IndexOf("err", StringComparison.OrdinalIgnoreCase) >= 0);
                    var zkfpConstOK = 0;
                    if (zkfpErrType != null)
                    {
                        var f = zkfpErrType.GetField("ZKFP_ERR_OK", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        if (f != null) zkfpConstOK = Convert.ToInt32(f.GetValue(null));
                        Log($"Found errdef type; ZKFP_ERR_OK={zkfpConstOK}");
                    }
                    else
                    {
                        Log("No errdef type found in lib.");
                    }

                    if (zkfp2Type != null)
                    {
                        Log("Found type 'zkfp2' in lib.");
                        var init = zkfp2Type.GetMethod("Init", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var getDeviceCount = zkfp2Type.GetMethod("GetDeviceCount", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var openDevice = zkfp2Type.GetMethod("OpenDevice", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var dbInit = zkfp2Type.GetMethod("DBInit", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var getParameters = zkfp2Type.GetMethod("GetParameters", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var byteArray2Int = zkfp2Type.GetMethod("ByteArray2Int", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var acquire = zkfp2Type.GetMethod("AcquireFingerprint", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        var blobToBase64 = zkfp2Type.GetMethod("BlobToBase64", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);

                        if (init != null && getDeviceCount != null && openDevice != null && dbInit != null && getParameters != null && acquire != null && blobToBase64 != null)
                        {
                            try
                            {
                                var initRet = Convert.ToInt32(init.Invoke(null, null));
                                Log($"zkfp2.Init() returned {initRet}");
                                if (zkfpConstOK != 0 && initRet != zkfpConstOK) Log("libzkfpcsharp.Init returned " + initRet);
                            }
                            catch (Exception exInit)
                            {
                                Log("Init invoke error: " + exInit.Message);
                            }

                            int nCount = 0;
                            try { nCount = Convert.ToInt32(getDeviceCount.Invoke(null, null)); } catch (Exception exGc) { Log("GetDeviceCount error: " + exGc.Message); }
                            Log($"GetDeviceCount -> {nCount}");
                            if (nCount <= 0)
                            {
                                Log("Aucun appareil détecté par libzkfpcsharp.");
                            }
                            else
                            {
                                object devObj = null;
                                try { devObj = openDevice.Invoke(null, new object[] { 0 }); } catch (Exception exOpen) { Log("OpenDevice invoke error: " + exOpen.Message); }
                                Log($"OpenDevice returned: {(devObj == null ? "(null)" : devObj.ToString())}");
                                var isZeroPtr = (devObj is IntPtr ip && ip == IntPtr.Zero);
                                if (devObj == null || isZeroPtr)
                                {
                                    Log("OpenDevice returned null/zero handle");
                                }
                                else
                                {
                                    try { dbInit.Invoke(null, null); } catch (Exception exDbInit) { Log("DBInit invoke error: " + exDbInit.Message); }

                                    var paramValue = new byte[4];
                                    object[] gpArgs = new object[] { devObj, 1, paramValue, 4 };
                                    try { getParameters.Invoke(null, gpArgs); } catch { }
                                    object[] baiArgs = new object[] { paramValue, 0 };
                                    try { byteArray2Int.Invoke(null, baiArgs); } catch { }
                                    int width = 0;
                                    try { width = Convert.ToInt32(baiArgs[1]); } catch { }

                                    gpArgs = new object[] { devObj, 2, paramValue, 4 };
                                    try { getParameters.Invoke(null, gpArgs); } catch { }
                                    baiArgs = new object[] { paramValue, 0 };
                                    try { byteArray2Int.Invoke(null, baiArgs); } catch { }
                                    int height = 0;
                                    try { height = Convert.ToInt32(baiArgs[1]); } catch { }

                                    Log($"Device image size width={width} height={height}");

                                    var fpBuffer = new byte[Math.Max(1, width * height)];

                                    var sw = Stopwatch.StartNew();
                                    while (sw.ElapsedMilliseconds < maxWaitMs)
                                    {
                                        var capTmp = new byte[2048];
                                        var cbCapTmp = 2048;
                                        object[] acqArgs = new object[] { devObj, fpBuffer, capTmp, cbCapTmp };
                                        int ret;
                                        try { ret = Convert.ToInt32(acquire.Invoke(null, acqArgs)); } catch (Exception ex) { Log("Acquire error: " + ex.Message); ret = -1; }
                                        try { cbCapTmp = Convert.ToInt32(acqArgs[3]); } catch { }

                                        Log($"Acquire returned {ret} cbCapTmp={cbCapTmp}");

                                        if (ret == 0 || ret == zkfpConstOK)
                                        {
                                            object[] b2aArgs = new object[] { capTmp, cbCapTmp };
                                            var s = blobToBase64.Invoke(null, b2aArgs) as string;
                                            if (!string.IsNullOrEmpty(s))
                                            {
                                                Log($"Empreinte capturée (lib) length={s.Length}.");
                                                return s;
                                            }
                                        }
                                        await Task.Delay(pollMs);
                                    }
                                    Log("Temps d'attente dépassé (libzkfpcsharp).");
                                }
                            }
                        }
                        else
                        {
                            Log("Required methods not found on zkfp2 type in lib.");
                        }
                    }
                    else
                    {
                        Log("Type 'zkfp2' not found in libzkfpcsharp assembly.");
                    }
                }
                catch (Exception exLoad)
                {
                    Log("Failed to load or inspect libzkfpcsharp assembly: " + exLoad.Message);
                }
            }
        }
        catch (Exception ex)
        {
            Log("libzkfpcsharp attempt failed: " + ex.Message);
        }

        // Fallback: ActiveX/Interop with prompting and polling
        var baseDir2 = AppDomain.CurrentDomain.BaseDirectory;
        var asmName2 = "Interop.ZKFPEngXControl.dll";
        var asmPath2 = Path.Combine(baseDir2, asmName2);

        if (!File.Exists(asmPath2))
        {
            var sdkPath2 = Path.Combine(baseDir2, "..", "BiometricFinEnrolmentVerificationZkteco", "bin", "Debug", asmName2);
            sdkPath2 = Path.GetFullPath(sdkPath2);
            if (File.Exists(sdkPath2))
            {
                try { File.Copy(sdkPath2, asmPath2, overwrite: true); Log($"Copied SDK interop from {sdkPath2} to {asmPath2}."); } catch (Exception ex) { Log($"Failed to copy interop DLL: {ex.Message}"); }
            }
        }

        if (File.Exists(asmPath2))
        {
            try
            {
                var asm2 = System.Reflection.Assembly.LoadFrom(asmPath2);
                var progids = new[] { "ZKFPEngX.ZKFPEngX", "ZKFPEngX.ZKFPEngXCtrl", "ZKFPEngXControl.ZKFPEngXCtrl", "ZKFPEngXControl.ZKFPEngX" };
                string[] methodNames = new[] { "GetRegisterTemplate", "GetTemplateAsString", "GetTemplate", "GetBase64Template", "GetBiometricTemplate", "GetTemplateAsStringEx", "GetTemplateAsString" };

                foreach (var progid in progids)
                {
                    try
                    {
                        var t = Type.GetTypeFromProgID(progid);
                        if (t == null) continue;

                        var result = await RunInSta(() =>
                        {
                            var inst = Activator.CreateInstance(t);

                            // Ensure simulation is off if available
                            try
                            {
                                var fakeProp = t.GetProperty("FakeFunOn");
                                if (fakeProp != null && fakeProp.CanWrite)
                                {
                                    fakeProp.SetValue(inst, 0);
                                }
                                else
                                {
                                    var setFake = t.GetMethod("put_FakeFunOn");
                                    if (setFake != null) setFake.Invoke(inst, new object[] { 0 });
                                }
                            }
                            catch { }

                            // Try to init engine and begin capture
                            try
                            {
                                var setVer = t.GetProperty("FPEngineVersion");
                                if (setVer != null && setVer.CanWrite) setVer.SetValue(inst, "9");
                                var initM = t.GetMethod("InitEngine");
                                if (initM != null) initM.Invoke(inst, null);
                                var cancel = t.GetMethod("CancelEnroll");
                                if (cancel != null) cancel.Invoke(inst, null);
                                var beginM = t.GetMethod("BeginCapture");
                                if (beginM != null) beginM.Invoke(inst, null);
                            }
                            catch { }

                            var swLocal = Stopwatch.StartNew();
                            while (swLocal.ElapsedMilliseconds < maxWaitMs)
                            {
                                // Prefer methods that return a template string
                                foreach (var name in methodNames)
                                {
                                    try
                                    {
                                        var m = t.GetMethod(name, System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.IgnoreCase);
                                        if (m == null) continue;

                                        object res = null;
                                        if (m.GetParameters().Length == 0)
                                        {
                                            res = m.Invoke(inst, null);
                                        }
                                        else if (m.GetParameters().Length == 1 && m.GetParameters()[0].ParameterType == typeof(string))
                                        {
                                            res = m.Invoke(inst, new object[] { "9" });
                                        }

                                        if (res is string s && !string.IsNullOrEmpty(s))
                                        {
                                            // Basic heuristic: require non-trivial length
                                            if (s.Length > 50)
                                            {
                                                ShowCaptureSuccess();
                                                return s;
                                            }
                                        }
                                        if (res is byte[] b && b.Length > 0)
                                        {
                                            ShowCaptureSuccess();
                                            return Convert.ToBase64String(b);
                                        }
                                    }
                                    catch { }
                                }

                                // Also check a quality property if available
                                try
                                {
                                    var qProp = t.GetProperty("LastQuality") ?? t.GetProperty("aQuality");
                                    if (qProp != null)
                                    {
                                        var qv = qProp.GetValue(inst);
                                        if (qv is int qi && qi >= 0)
                                        {
                                            // If device reports a quality >= 0, we likely have an image
                                            // attempt to retrieve template again immediately
                                            foreach (var name in methodNames)
                                            {
                                                try
                                                {
                                                    var m = t.GetMethod(name, System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.IgnoreCase);
                                                    if (m == null) continue;
                                                    object res = m.GetParameters().Length == 0 ? m.Invoke(inst, null) : m.Invoke(inst, new object[] { "9" });
                                                    if (res is string s2 && s2.Length > 50) { ShowCaptureSuccess(); return s2; }
                                                    if (res is byte[] b2 && b2.Length > 0) { ShowCaptureSuccess(); return Convert.ToBase64String(b2); }
                                                }
                                                catch { }
                                            }
                                        }
                                    }
                                }
                                catch { }

                                System.Threading.Thread.Sleep(pollMs);
                            }
                            return null;
                        });

                        if (result is string ss)
                        {
                            try { Convert.FromBase64String(ss); return ss; }
                            catch { return Convert.ToBase64String(Encoding.UTF8.GetBytes(ss)); }
                        }
                    }
                    catch { }
                }
            }
            catch (Exception ex)
            {
                Log("ActiveX attempt failed: " + ex.Message);
            }
        }

        Log("Aucun SDK utilisable trouvé — aucune capture possible.");
        throw new InvalidOperationException("Aucun capteur d'empreinte trouvé ou aucun SDK disponible. Vérifiez que le lecteur est bien branché.");
    }

    public async Task<object> MatchFingerprintAsync(string probeB64, JsonElement gallery)
    {
        // Try to find already-loaded assembly first (avoids "Assembly with same name" error)
        var asm = AppDomain.CurrentDomain.GetAssemblies()
            .FirstOrDefault(a => a.GetName().Name == "libzkfpcsharp");

        if (asm == null)
        {
            var managedPath = @"C:\Windows\SysWOW64\libzkfpcsharp.dll";
            if (!File.Exists(managedPath))
            {
                var baseDir = AppDomain.CurrentDomain.BaseDirectory;
                managedPath = Path.Combine(baseDir, "libzkfpcsharp.dll");
            }
            if (!File.Exists(managedPath))
                throw new FileNotFoundException("libzkfpcsharp.dll not found");

            asm = System.Reflection.Assembly.LoadFrom(managedPath);
        }

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

        int rc = (int)mInit.Invoke(null, null)!;
        Log($"Match: zkfp2.Init() = {rc}");
        // rc == 0 means fresh init; rc == 1 means already initialized (e.g. after scan) — both are OK
        bool weInitialized = (rc == 0);
        if (rc != 0 && rc != 1)
            throw new InvalidOperationException($"zkfp2.Init() failed with code {rc}");

        try
        {
            IntPtr dbHandle = (IntPtr)mDBInit.Invoke(null, null)!;
            Log($"Match: DBInit handle = {dbHandle}");
            if (dbHandle == IntPtr.Zero)
                throw new InvalidOperationException("DBInit failed (returned null handle)");

            try
            {
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
                    int id = -1;
                    try
                    {
                        id = item.GetProperty("id").GetInt32();
                        string tplB64 = item.GetProperty("template_b64").GetString()!;

                        // Skip obviously invalid templates (real ZKTeco templates are 600+ bytes raw)
                        if (string.IsNullOrEmpty(tplB64) || tplB64.Length < 100)
                        {
                            Log($"Match: id={id} SKIPPED (template too short: {tplB64?.Length ?? 0} chars)");
                            continue;
                        }

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

                        if (score > 0 && score > bestScore)
                        {
                            bestScore = score;
                            bestId = id;
                        }
                    }
                    catch (Exception itemEx)
                    {
                        Log($"Match: id={id} ERROR (skipped): {itemEx.InnerException?.Message ?? itemEx.Message}");
                        continue;
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
            // Only terminate if we were the ones who initialized (rc == 0)
            if (weInitialized)
            {
                try { mTerminate.Invoke(null, null); } catch { }
            }
        }
    }

    private void StartInitialScan()
    {
        Task.Run(async () =>
        {
            try
            {
                Log("Initial automatic scan starting (30s timeout)...");
                var tpl = await ScanFingerprintAsync();
                if (!string.IsNullOrEmpty(tpl))
                {
                    Log($"Initial scan template: {tpl}");
                }
                else
                {
                    Log("Initial scan completed with no template.");
                }
            }
            catch (Exception ex)
            {
                Log($"Initial scan error: {ex.Message}");
            }
        });
    }

    private void Log(string text)
    {
        if (InvokeRequired)
        {
            BeginInvoke(new Action(() => Log(text)));
            return;
        }
        var line = $"[{DateTime.Now:HH:mm:ss}] {text}";
        txtLog.AppendText(line + Environment.NewLine);
        try { Console.WriteLine(line); } catch { }
        try
        {
            var logDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge");
            if (!Directory.Exists(logDir)) Directory.CreateDirectory(logDir);
            var logPath = Path.Combine(logDir, "bridge.log");
            File.AppendAllText(logPath, line + Environment.NewLine);
        }
        catch { }
    }

    private async void BtnScan_Click(object sender, EventArgs e)
    {
        Log("Manual scan requested...");
        try
        {
            var tpl = await ScanFingerprintAsync();
            Log($"Template: {tpl}");
        }
        catch (Exception ex)
        {
            Log($"Scan error: {ex.Message}");
        }
    }
}
