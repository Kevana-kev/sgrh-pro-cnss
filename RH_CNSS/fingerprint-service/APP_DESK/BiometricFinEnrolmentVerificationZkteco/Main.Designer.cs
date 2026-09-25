namespace BiometricFinEnrolmentVerificationZkteco
{
    partial class Main
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Main));
            this.menuStrip3 = new System.Windows.Forms.MenuStrip();
            this.enrolmentStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.verificationStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.StudentsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.RegAdminToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.LogoutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.addUserToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip3.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip3
            // 
            this.menuStrip3.BackColor = System.Drawing.Color.White;
            this.menuStrip3.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.menuStrip3.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.menuStrip3.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.enrolmentStripMenuItem1,
            this.verificationStripMenuItem1,
            this.StudentsToolStripMenuItem,
            this.LogoutToolStripMenuItem});
            this.menuStrip3.Location = new System.Drawing.Point(0, 0);
            this.menuStrip3.Name = "menuStrip3";
            this.menuStrip3.Size = new System.Drawing.Size(1349, 65);
            this.menuStrip3.TabIndex = 10;
            this.menuStrip3.Text = "menuStrip3";
            // 
            // enrolmentStripMenuItem1
            // 
            this.enrolmentStripMenuItem1.Font = new System.Drawing.Font("Bookman Old Style", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.enrolmentStripMenuItem1.Image = global::BiometricFinEnrolmentVerificationZkteco.Properties.Resources.ic_action_fingerprint;
            this.enrolmentStripMenuItem1.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.enrolmentStripMenuItem1.Name = "enrolmentStripMenuItem1";
            this.enrolmentStripMenuItem1.Size = new System.Drawing.Size(123, 61);
            this.enrolmentStripMenuItem1.Text = "Enrolment";
            this.enrolmentStripMenuItem1.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.enrolmentStripMenuItem1.Click += new System.EventHandler(this.enrolmentStripMenuItem1_Click);
            // 
            // verificationStripMenuItem1
            // 
            this.verificationStripMenuItem1.Font = new System.Drawing.Font("Bookman Old Style", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.verificationStripMenuItem1.Image = global::BiometricFinEnrolmentVerificationZkteco.Properties.Resources.ic_action_fingerprint;
            this.verificationStripMenuItem1.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.verificationStripMenuItem1.Name = "verificationStripMenuItem1";
            this.verificationStripMenuItem1.Size = new System.Drawing.Size(131, 61);
            this.verificationStripMenuItem1.Text = "Verification";
            this.verificationStripMenuItem1.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.verificationStripMenuItem1.Click += new System.EventHandler(this.verificationStripMenuItem1_Click);
            // 
            // StudentsToolStripMenuItem
            // 
            this.StudentsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.RegAdminToolStripMenuItem,
            this.addUserToolStripMenuItem});
            this.StudentsToolStripMenuItem.Font = new System.Drawing.Font("Bookman Old Style", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.StudentsToolStripMenuItem.Image = global::BiometricFinEnrolmentVerificationZkteco.Properties.Resources.ic_action_person_add;
            this.StudentsToolStripMenuItem.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.StudentsToolStripMenuItem.Name = "StudentsToolStripMenuItem";
            this.StudentsToolStripMenuItem.Size = new System.Drawing.Size(131, 61);
            this.StudentsToolStripMenuItem.Text = "New Admin";
            this.StudentsToolStripMenuItem.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.StudentsToolStripMenuItem.Click += new System.EventHandler(this.StudentsToolStripMenuItem_Click);
            // 
            // RegAdminToolStripMenuItem
            // 
            this.RegAdminToolStripMenuItem.Name = "RegAdminToolStripMenuItem";
            this.RegAdminToolStripMenuItem.Size = new System.Drawing.Size(224, 26);
            this.RegAdminToolStripMenuItem.Text = "Register";
            this.RegAdminToolStripMenuItem.Click += new System.EventHandler(this.RegAdminToolStripMenuItem_Click);
            // 
            // LogoutToolStripMenuItem
            // 
            this.LogoutToolStripMenuItem.Font = new System.Drawing.Font("Bookman Old Style", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.LogoutToolStripMenuItem.Image = global::BiometricFinEnrolmentVerificationZkteco.Properties.Resources.ic_action_logout;
            this.LogoutToolStripMenuItem.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.LogoutToolStripMenuItem.Name = "LogoutToolStripMenuItem";
            this.LogoutToolStripMenuItem.Size = new System.Drawing.Size(87, 61);
            this.LogoutToolStripMenuItem.Text = "Logout";
            this.LogoutToolStripMenuItem.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText;
            this.LogoutToolStripMenuItem.Click += new System.EventHandler(this.LogoutToolStripMenuItem_Click);
            // 
            // addUserToolStripMenuItem
            // 
            this.addUserToolStripMenuItem.Name = "addUserToolStripMenuItem";
            this.addUserToolStripMenuItem.Size = new System.Drawing.Size(224, 26);
            this.addUserToolStripMenuItem.Text = "Add user";
            this.addUserToolStripMenuItem.Click += new System.EventHandler(this.addUserToolStripMenuItem_Click);
            // 
            // Main
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = global::BiometricFinEnrolmentVerificationZkteco.Properties.Resources.background_image_4735444;
            this.ClientSize = new System.Drawing.Size(1349, 635);
            this.Controls.Add(this.menuStrip3);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "Main";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Tag = "";
            this.Text = "Biometric Fingerprint Enrolment and Verification Sysem";
            this.WindowState = System.Windows.Forms.FormWindowState.Maximized;
            this.Load += new System.EventHandler(this.Main_Load);
            this.menuStrip3.ResumeLayout(false);
            this.menuStrip3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        internal System.Windows.Forms.MenuStrip menuStrip3;
        internal System.Windows.Forms.ToolStripMenuItem enrolmentStripMenuItem1;
        internal System.Windows.Forms.ToolStripMenuItem StudentsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem RegAdminToolStripMenuItem;
        internal System.Windows.Forms.ToolStripMenuItem LogoutToolStripMenuItem;
        internal System.Windows.Forms.ToolStripMenuItem verificationStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem addUserToolStripMenuItem;
    }
}