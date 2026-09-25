using System;
using System.IO;
using System.Windows.Forms;

internal static class Program
{
    [STAThread]
    static void Main(string[] args)
    {
        // support headless/service mode: run the local web API without showing UI
        if (args != null && args.Length > 0 && Array.Exists(args, a => a == "--headless"))
        {
            try
            {
                var hb = new HeadlessBridge();
                hb.StartAsync().GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                // best-effort logging
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
}