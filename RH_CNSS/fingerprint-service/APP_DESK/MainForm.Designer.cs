partial class MainForm
{
    /// <summary>
    /// Required designer variable.
    /// </summary>
    private System.ComponentModel.IContainer components = null;

    /// <summary>
    /// Clean up any resources being used.
    /// </summary>
    /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
    protected override void Dispose(bool disposing)
    {
        if (disposing && (components != null))
        {
            components.Dispose();
        }
        base.Dispose(disposing);
    }

    #region Windows Form Designer generated code

    /// <summary>
    /// Required method for Designer support - do not modify
    /// the contents of this method with the code editor.
    /// </summary>
    private void InitializeComponent()
    {
        this.btnScan = new System.Windows.Forms.Button();
        this.txtLog = new System.Windows.Forms.TextBox();
        this.SuspendLayout();
        // 
        // btnScan
        // 
        this.btnScan.Location = new System.Drawing.Point(12, 12);
        this.btnScan.Name = "btnScan";
        this.btnScan.Size = new System.Drawing.Size(120, 34);
        this.btnScan.TabIndex = 0;
        this.btnScan.Text = "Scan Fingerprint";
        this.btnScan.UseVisualStyleBackColor = true;
        this.btnScan.Click += new System.EventHandler(this.BtnScan_Click);
        // 
        // txtLog
        // 
        this.txtLog.Location = new System.Drawing.Point(12, 62);
        this.txtLog.Multiline = true;
        this.txtLog.Name = "txtLog";
        this.txtLog.ReadOnly = true;
        this.txtLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
        this.txtLog.Size = new System.Drawing.Size(560, 287);
        this.txtLog.TabIndex = 1;
        // 
        // MainForm
        // 
        this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
        this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
        this.ClientSize = new System.Drawing.Size(584, 361);
        this.Controls.Add(this.txtLog);
        this.Controls.Add(this.btnScan);
        this.Name = "MainForm";
        this.Text = "Fingerprint Bridge";
        this.ResumeLayout(false);
        this.PerformLayout();

    }

    #endregion

    private System.Windows.Forms.Button btnScan;
    private System.Windows.Forms.TextBox txtLog;
}
