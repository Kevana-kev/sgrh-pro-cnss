namespace BiometricFinEnrolmentVerificationZkteco
{
    partial class Etudiant
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
            this.panel1 = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.label2 = new System.Windows.Forms.Label();
            this.txtRegID = new Guna.UI2.WinForms.Guna2TextBox();
            this.txt_noms = new Guna.UI2.WinForms.Guna2TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.txt_sexe = new Guna.UI2.WinForms.Guna2TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.txt_telephone = new Guna.UI2.WinForms.Guna2TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.txt_adresse = new Guna.UI2.WinForms.Guna2TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.btn_parcourir = new Guna.UI2.WinForms.Guna2Button();
            this.fpicture = new System.Windows.Forms.PictureBox();
            this.label7 = new System.Windows.Forms.Label();
            this.txtdeviceSerial = new System.Windows.Forms.TextBox();
            this.prompt = new System.Windows.Forms.Label();
            this.btn_demarrer = new Guna.UI2.WinForms.Guna2Button();
            this.btn_capturer = new Guna.UI2.WinForms.Guna2Button();
            this.label9 = new System.Windows.Forms.Label();
            this.txt_rfid_n = new Guna.UI2.WinForms.Guna2TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.txt_rfid_ch = new Guna.UI2.WinForms.Guna2TextBox();
            this.dataGridView1 = new System.Windows.Forms.DataGridView();
            this.btn_quitter = new Guna.UI2.WinForms.Guna2Button();
            this.lblmsg = new System.Windows.Forms.Label();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.fpicture)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).BeginInit();
            this.SuspendLayout();
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.Color.Red;
            this.panel1.Controls.Add(this.label1);
            this.panel1.Location = new System.Drawing.Point(0, 1);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(987, 58);
            this.panel1.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Impact", 28.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.White;
            this.label1.Location = new System.Drawing.Point(213, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(541, 59);
            this.label1.TabIndex = 1;
            this.label1.Text = "Formulaire d\'enrôllement";
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = global::BiometricFinEnrolmentVerificationZkteco.Properties.Resources.icons8_User_Group_Man_Man_50px;
            this.pictureBox1.Location = new System.Drawing.Point(13, 99);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(180, 250);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 1;
            this.pictureBox1.TabStop = false;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(226, 99);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(97, 22);
            this.label2.TabIndex = 2;
            this.label2.Text = "Matricule:";
            // 
            // txtRegID
            // 
            this.txtRegID.BorderColor = System.Drawing.Color.Blue;
            this.txtRegID.BorderRadius = 10;
            this.txtRegID.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txtRegID.DefaultText = "";
            this.txtRegID.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txtRegID.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txtRegID.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txtRegID.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txtRegID.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txtRegID.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtRegID.ForeColor = System.Drawing.Color.Black;
            this.txtRegID.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txtRegID.Location = new System.Drawing.Point(230, 127);
            this.txtRegID.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txtRegID.Name = "txtRegID";
            this.txtRegID.PasswordChar = '\0';
            this.txtRegID.PlaceholderText = "Taper matricule";
            this.txtRegID.SelectedText = "";
            this.txtRegID.Size = new System.Drawing.Size(373, 42);
            this.txtRegID.TabIndex = 7;
            this.txtRegID.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // txt_noms
            // 
            this.txt_noms.BorderColor = System.Drawing.Color.Blue;
            this.txt_noms.BorderRadius = 10;
            this.txt_noms.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txt_noms.DefaultText = "";
            this.txt_noms.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txt_noms.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txt_noms.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_noms.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_noms.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_noms.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_noms.ForeColor = System.Drawing.Color.Black;
            this.txt_noms.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_noms.Location = new System.Drawing.Point(230, 203);
            this.txt_noms.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txt_noms.Name = "txt_noms";
            this.txt_noms.PasswordChar = '\0';
            this.txt_noms.PlaceholderText = "Taper le nom";
            this.txt_noms.SelectedText = "";
            this.txt_noms.Size = new System.Drawing.Size(373, 42);
            this.txt_noms.TabIndex = 9;
            this.txt_noms.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(226, 175);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(66, 22);
            this.label3.TabIndex = 8;
            this.label3.Text = "Noms:";
            // 
            // txt_sexe
            // 
            this.txt_sexe.BorderColor = System.Drawing.Color.Blue;
            this.txt_sexe.BorderRadius = 10;
            this.txt_sexe.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txt_sexe.DefaultText = "";
            this.txt_sexe.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txt_sexe.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txt_sexe.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_sexe.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_sexe.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_sexe.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_sexe.ForeColor = System.Drawing.Color.Black;
            this.txt_sexe.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_sexe.Location = new System.Drawing.Point(230, 285);
            this.txt_sexe.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txt_sexe.Name = "txt_sexe";
            this.txt_sexe.PasswordChar = '\0';
            this.txt_sexe.PlaceholderText = "Taper le sexe";
            this.txt_sexe.SelectedText = "";
            this.txt_sexe.Size = new System.Drawing.Size(373, 42);
            this.txt_sexe.TabIndex = 11;
            this.txt_sexe.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(226, 257);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(61, 22);
            this.label4.TabIndex = 10;
            this.label4.Text = "Sexe:";
            // 
            // txt_telephone
            // 
            this.txt_telephone.BorderColor = System.Drawing.Color.Blue;
            this.txt_telephone.BorderRadius = 10;
            this.txt_telephone.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txt_telephone.DefaultText = "";
            this.txt_telephone.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txt_telephone.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txt_telephone.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_telephone.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_telephone.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_telephone.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_telephone.ForeColor = System.Drawing.Color.Black;
            this.txt_telephone.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_telephone.Location = new System.Drawing.Point(230, 367);
            this.txt_telephone.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txt_telephone.Name = "txt_telephone";
            this.txt_telephone.PasswordChar = '\0';
            this.txt_telephone.PlaceholderText = "Taper le numero de téléphone";
            this.txt_telephone.SelectedText = "";
            this.txt_telephone.Size = new System.Drawing.Size(373, 42);
            this.txt_telephone.TabIndex = 13;
            this.txt_telephone.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(234, 415);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(89, 22);
            this.label5.TabIndex = 12;
            this.label5.Text = "Adresse:";
            // 
            // txt_adresse
            // 
            this.txt_adresse.BorderColor = System.Drawing.Color.Blue;
            this.txt_adresse.BorderRadius = 10;
            this.txt_adresse.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txt_adresse.DefaultText = "";
            this.txt_adresse.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txt_adresse.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txt_adresse.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_adresse.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_adresse.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_adresse.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_adresse.ForeColor = System.Drawing.Color.Black;
            this.txt_adresse.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_adresse.Location = new System.Drawing.Point(14, 449);
            this.txt_adresse.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txt_adresse.Name = "txt_adresse";
            this.txt_adresse.PasswordChar = '\0';
            this.txt_adresse.PlaceholderText = "Votre adresse ici";
            this.txt_adresse.SelectedText = "";
            this.txt_adresse.Size = new System.Drawing.Size(595, 42);
            this.txt_adresse.TabIndex = 15;
            this.txt_adresse.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(232, 339);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(111, 22);
            this.label6.TabIndex = 14;
            this.label6.Text = "Téléphone:";
            // 
            // btn_parcourir
            // 
            this.btn_parcourir.BorderRadius = 10;
            this.btn_parcourir.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btn_parcourir.DisabledState.BorderColor = System.Drawing.Color.DarkGray;
            this.btn_parcourir.DisabledState.CustomBorderColor = System.Drawing.Color.DarkGray;
            this.btn_parcourir.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(169)))), ((int)(((byte)(169)))), ((int)(((byte)(169)))));
            this.btn_parcourir.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(141)))), ((int)(((byte)(141)))), ((int)(((byte)(141)))));
            this.btn_parcourir.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(192)))));
            this.btn_parcourir.FocusedColor = System.Drawing.Color.Red;
            this.btn_parcourir.Font = new System.Drawing.Font("Segoe UI", 10.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btn_parcourir.ForeColor = System.Drawing.Color.Red;
            this.btn_parcourir.Location = new System.Drawing.Point(13, 367);
            this.btn_parcourir.Name = "btn_parcourir";
            this.btn_parcourir.Size = new System.Drawing.Size(180, 54);
            this.btn_parcourir.TabIndex = 16;
            this.btn_parcourir.Text = "Parcourir";
            this.btn_parcourir.Click += new System.EventHandler(this.btn_parcourir_Click);
            // 
            // fpicture
            // 
            this.fpicture.BackColor = System.Drawing.SystemColors.AppWorkspace;
            this.fpicture.Location = new System.Drawing.Point(710, 119);
            this.fpicture.Name = "fpicture";
            this.fpicture.Size = new System.Drawing.Size(209, 179);
            this.fpicture.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.fpicture.TabIndex = 17;
            this.fpicture.TabStop = false;
            this.fpicture.Click += new System.EventHandler(this.pictureBox2_Click);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.ForeColor = System.Drawing.Color.Blue;
            this.label7.Location = new System.Drawing.Point(25, 69);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(78, 25);
            this.label7.TabIndex = 18;
            this.label7.Text = "Serial : ";
            // 
            // txtdeviceSerial
            // 
            this.txtdeviceSerial.Location = new System.Drawing.Point(105, 72);
            this.txtdeviceSerial.Name = "txtdeviceSerial";
            this.txtdeviceSerial.Size = new System.Drawing.Size(857, 22);
            this.txtdeviceSerial.TabIndex = 19;
            // 
            // prompt
            // 
            this.prompt.AutoSize = true;
            this.prompt.Location = new System.Drawing.Point(710, 301);
            this.prompt.Name = "prompt";
            this.prompt.Size = new System.Drawing.Size(57, 16);
            this.prompt.TabIndex = 20;
            this.prompt.Text = "Ready...";
            this.prompt.Click += new System.EventHandler(this.label8_Click);
            // 
            // btn_demarrer
            // 
            this.btn_demarrer.BorderRadius = 10;
            this.btn_demarrer.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btn_demarrer.DisabledState.BorderColor = System.Drawing.Color.DarkGray;
            this.btn_demarrer.DisabledState.CustomBorderColor = System.Drawing.Color.DarkGray;
            this.btn_demarrer.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(169)))), ((int)(((byte)(169)))), ((int)(((byte)(169)))));
            this.btn_demarrer.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(141)))), ((int)(((byte)(141)))), ((int)(((byte)(141)))));
            this.btn_demarrer.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(192)))));
            this.btn_demarrer.FocusedColor = System.Drawing.Color.Red;
            this.btn_demarrer.Font = new System.Drawing.Font("Segoe UI", 10.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btn_demarrer.ForeColor = System.Drawing.Color.Red;
            this.btn_demarrer.Location = new System.Drawing.Point(14, 500);
            this.btn_demarrer.Name = "btn_demarrer";
            this.btn_demarrer.Size = new System.Drawing.Size(180, 54);
            this.btn_demarrer.TabIndex = 21;
            this.btn_demarrer.Text = "Demarrer";
            this.btn_demarrer.Click += new System.EventHandler(this.btn_demarrer_Click);
            // 
            // btn_capturer
            // 
            this.btn_capturer.BorderRadius = 10;
            this.btn_capturer.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btn_capturer.DisabledState.BorderColor = System.Drawing.Color.DarkGray;
            this.btn_capturer.DisabledState.CustomBorderColor = System.Drawing.Color.DarkGray;
            this.btn_capturer.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(169)))), ((int)(((byte)(169)))), ((int)(((byte)(169)))));
            this.btn_capturer.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(141)))), ((int)(((byte)(141)))), ((int)(((byte)(141)))));
            this.btn_capturer.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(192)))));
            this.btn_capturer.FocusedColor = System.Drawing.Color.Red;
            this.btn_capturer.Font = new System.Drawing.Font("Segoe UI", 10.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btn_capturer.ForeColor = System.Drawing.Color.Red;
            this.btn_capturer.Location = new System.Drawing.Point(200, 499);
            this.btn_capturer.Name = "btn_capturer";
            this.btn_capturer.Size = new System.Drawing.Size(180, 54);
            this.btn_capturer.TabIndex = 22;
            this.btn_capturer.Text = "Capturer";
            this.btn_capturer.Click += new System.EventHandler(this.btn_capturer_Click);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label9.Location = new System.Drawing.Point(712, 347);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(55, 22);
            this.label9.TabIndex = 24;
            this.label9.Text = "RFID";
            // 
            // txt_rfid_n
            // 
            this.txt_rfid_n.BorderColor = System.Drawing.Color.Blue;
            this.txt_rfid_n.BorderRadius = 10;
            this.txt_rfid_n.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txt_rfid_n.DefaultText = "";
            this.txt_rfid_n.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txt_rfid_n.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txt_rfid_n.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_rfid_n.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_rfid_n.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_rfid_n.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_rfid_n.ForeColor = System.Drawing.Color.Black;
            this.txt_rfid_n.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_rfid_n.Location = new System.Drawing.Point(710, 375);
            this.txt_rfid_n.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txt_rfid_n.Name = "txt_rfid_n";
            this.txt_rfid_n.PasswordChar = '\0';
            this.txt_rfid_n.PlaceholderText = "RFID numerique";
            this.txt_rfid_n.SelectedText = "";
            this.txt_rfid_n.Size = new System.Drawing.Size(209, 42);
            this.txt_rfid_n.TabIndex = 23;
            this.txt_rfid_n.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label10.Location = new System.Drawing.Point(712, 423);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(174, 22);
            this.label10.TabIndex = 26;
            this.label10.Text = "RFID Confirmation";
            // 
            // txt_rfid_ch
            // 
            this.txt_rfid_ch.BorderColor = System.Drawing.Color.Blue;
            this.txt_rfid_ch.BorderRadius = 10;
            this.txt_rfid_ch.Cursor = System.Windows.Forms.Cursors.IBeam;
            this.txt_rfid_ch.DefaultText = "";
            this.txt_rfid_ch.DisabledState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(208)))), ((int)(((byte)(208)))), ((int)(((byte)(208)))));
            this.txt_rfid_ch.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(226)))), ((int)(((byte)(226)))));
            this.txt_rfid_ch.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_rfid_ch.DisabledState.PlaceholderForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(138)))), ((int)(((byte)(138)))), ((int)(((byte)(138)))));
            this.txt_rfid_ch.FocusedState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_rfid_ch.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txt_rfid_ch.ForeColor = System.Drawing.Color.Black;
            this.txt_rfid_ch.HoverState.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(94)))), ((int)(((byte)(148)))), ((int)(((byte)(255)))));
            this.txt_rfid_ch.Location = new System.Drawing.Point(710, 451);
            this.txt_rfid_ch.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.txt_rfid_ch.Name = "txt_rfid_ch";
            this.txt_rfid_ch.PasswordChar = '\0';
            this.txt_rfid_ch.PlaceholderText = "RFID Chainne";
            this.txt_rfid_ch.SelectedText = "";
            this.txt_rfid_ch.Size = new System.Drawing.Size(209, 42);
            this.txt_rfid_ch.TabIndex = 25;
            this.txt_rfid_ch.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // dataGridView1
            // 
            this.dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView1.Location = new System.Drawing.Point(20, 565);
            this.dataGridView1.Name = "dataGridView1";
            this.dataGridView1.RowHeadersWidth = 51;
            this.dataGridView1.RowTemplate.Height = 24;
            this.dataGridView1.Size = new System.Drawing.Size(899, 181);
            this.dataGridView1.TabIndex = 27;
            // 
            // btn_quitter
            // 
            this.btn_quitter.BorderRadius = 10;
            this.btn_quitter.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btn_quitter.DisabledState.BorderColor = System.Drawing.Color.DarkGray;
            this.btn_quitter.DisabledState.CustomBorderColor = System.Drawing.Color.DarkGray;
            this.btn_quitter.DisabledState.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(169)))), ((int)(((byte)(169)))), ((int)(((byte)(169)))));
            this.btn_quitter.DisabledState.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(141)))), ((int)(((byte)(141)))), ((int)(((byte)(141)))));
            this.btn_quitter.FillColor = System.Drawing.Color.FromArgb(((int)(((byte)(0)))), ((int)(((byte)(0)))), ((int)(((byte)(192)))));
            this.btn_quitter.FocusedColor = System.Drawing.Color.Red;
            this.btn_quitter.Font = new System.Drawing.Font("Segoe UI", 10.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btn_quitter.ForeColor = System.Drawing.Color.Red;
            this.btn_quitter.Location = new System.Drawing.Point(429, 500);
            this.btn_quitter.Name = "btn_quitter";
            this.btn_quitter.Size = new System.Drawing.Size(180, 54);
            this.btn_quitter.TabIndex = 28;
            this.btn_quitter.Text = "Quitter";
            this.btn_quitter.Click += new System.EventHandler(this.guna2Button4_Click);
            // 
            // lblmsg
            // 
            this.lblmsg.AutoSize = true;
            this.lblmsg.Location = new System.Drawing.Point(636, 525);
            this.lblmsg.Name = "lblmsg";
            this.lblmsg.Size = new System.Drawing.Size(44, 16);
            this.lblmsg.TabIndex = 29;
            this.lblmsg.Text = "label8";
            // 
            // Etudiant
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(988, 758);
            this.Controls.Add(this.lblmsg);
            this.Controls.Add(this.btn_quitter);
            this.Controls.Add(this.dataGridView1);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.txt_rfid_ch);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.txt_rfid_n);
            this.Controls.Add(this.btn_capturer);
            this.Controls.Add(this.btn_demarrer);
            this.Controls.Add(this.prompt);
            this.Controls.Add(this.txtdeviceSerial);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.fpicture);
            this.Controls.Add(this.btn_parcourir);
            this.Controls.Add(this.txt_adresse);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.txt_telephone);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.txt_sexe);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.txt_noms);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.txtRegID);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.panel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "Etudiant";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Etudiant";
            this.Load += new System.EventHandler(this.Etudiant_Load);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.fpicture)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label label2;
        private Guna.UI2.WinForms.Guna2TextBox txtRegID;
        private Guna.UI2.WinForms.Guna2TextBox txt_noms;
        private System.Windows.Forms.Label label3;
        private Guna.UI2.WinForms.Guna2TextBox txt_sexe;
        private System.Windows.Forms.Label label4;
        private Guna.UI2.WinForms.Guna2TextBox txt_telephone;
        private System.Windows.Forms.Label label5;
        private Guna.UI2.WinForms.Guna2TextBox txt_adresse;
        private System.Windows.Forms.Label label6;
        private Guna.UI2.WinForms.Guna2Button btn_parcourir;
        private System.Windows.Forms.PictureBox fpicture;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox txtdeviceSerial;
        private System.Windows.Forms.Label prompt;
        private Guna.UI2.WinForms.Guna2Button btn_demarrer;
        private Guna.UI2.WinForms.Guna2Button btn_capturer;
        private System.Windows.Forms.Label label9;
        private Guna.UI2.WinForms.Guna2TextBox txt_rfid_n;
        private System.Windows.Forms.Label label10;
        private Guna.UI2.WinForms.Guna2TextBox txt_rfid_ch;
        private System.Windows.Forms.DataGridView dataGridView1;
        private Guna.UI2.WinForms.Guna2Button btn_quitter;
        private System.Windows.Forms.Label lblmsg;
    }
}