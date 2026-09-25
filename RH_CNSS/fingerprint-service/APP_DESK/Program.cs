using System;
using System.IO;
using System.Threading;
using System.Windows.Forms;

internal static class Program
{
    private const string MutexName = "Global\\SGRHProFingerprintBridgeSingleton";

    [STAThread]
    static void Main(string[] args)
    {
        var wantHeadless = ShouldRunHeadless(args);

        // Une seule instance : si déjà lancé, le clic web ne fait rien de plus.
        bool createdNew;
        using var mutex = new Mutex(true, MutexName, out createdNew);
        if (!createdNew)
        {
            try
            {
                var ap = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge");
                Directory.CreateDirectory(ap);
                File.AppendAllText(
                    Path.Combine(ap, "bridge.log"),
                    $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] Instance déjà active (demande web/install ignorée).{Environment.NewLine}");
            }
            catch { }
            return;
        }

        if (wantHeadless)
        {
            try
            {
                var hb = new HeadlessBridge();
                hb.StartAsync().GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                try
                {
                    var ap = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FingerprintBridge");
                    if (!Directory.Exists(ap)) Directory.CreateDirectory(ap);
                    var log = Path.Combine(ap, "bridge-error.log");
                    File.AppendAllText(log, $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] Headless start error: {ex}{Environment.NewLine}");
                }
                catch { }
            }
            return;
        }

        ApplicationConfiguration.Initialize();
        Application.Run(new MainForm());
    }

    private static bool ShouldRunHeadless(string[]? args)
    {
        if (args == null || args.Length == 0) return false;
        foreach (var a in args)
        {
            if (string.IsNullOrWhiteSpace(a)) continue;
            var v = a.Trim();
            if (v.Equals("--headless", StringComparison.OrdinalIgnoreCase)) return true;
            if (v.Equals("--from-web", StringComparison.OrdinalIgnoreCase)) return true;
            if (v.StartsWith("sgrhbridge:", StringComparison.OrdinalIgnoreCase)) return true;
            if (v.StartsWith("sgrh-fingerprint:", StringComparison.OrdinalIgnoreCase)) return true;
        }
        return false;
    }
}
