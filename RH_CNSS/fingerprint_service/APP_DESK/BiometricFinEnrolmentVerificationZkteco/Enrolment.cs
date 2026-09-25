using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Emgu.CV;
using Emgu.CV.Structure;
using Emgu.CV.CvEnum;
using AxZKFPEngXControl;
using System.Security.Cryptography;

namespace BiometricFinEnrolmentVerificationZkteco
{
    public partial class Enrolment : Form
    {
        private AxZKFPEngX ZkFprint = new AxZKFPEngX();
        private bool Check;

        //Declaration of all variables, vectors and haarcascades
        Image<Bgr, Byte> currentFrame;
        Capture grabber;
        public Enrolment()
        {
            InitializeComponent();
        }

        private void Enrolment_Load(object sender, EventArgs e)
        {
            Controls.Add(ZkFprint);
            InitialAxZkfp();

            GetID();

        }

        private void InitialAxZkfp()
        {
            try
            {

                ZkFprint.OnImageReceived += zkFprint_OnImageReceived;
                ZkFprint.OnFeatureInfo += zkFprint_OnFeatureInfo;
                //zkFprint.OnFingerTouching 
                //zkFprint.OnFingerLeaving
                ZkFprint.OnEnroll += zkFprint_OnEnroll;

                if (ZkFprint.InitEngine() == 0)
                {
                    ZkFprint.FPEngineVersion = "9";
                    ZkFprint.EnrollCount = 3;
                    txtdeviceSerial.Text = " " + ZkFprint.SensorSN + " Count: " + ZkFprint.SensorCount.ToString() + " Index: " + ZkFprint.SensorIndex.ToString();
                    ShowHintInfo("Device successfully connected");

                    ZkFprint.CancelEnroll();
                    ZkFprint.EnrollCount = 3;
                    ZkFprint.BeginEnroll();
                    ShowHintInfo("Please give fingerprint sample.");
                }

            }
            catch (Exception ex)
            {
                ShowHintInfo("Device init err, error: " + ex.Message);
            }
        }

        private void zkFprint_OnImageReceived(object sender, IZKFPEngXEvents_OnImageReceivedEvent e)
        {
            Graphics g = fpicture.CreateGraphics();
            Bitmap bmp = new Bitmap(fpicture.Width, fpicture.Height);
            g = Graphics.FromImage(bmp);
            int dc = g.GetHdc().ToInt32();
            ZkFprint.PrintImageAt(dc, 0, 0, bmp.Width, bmp.Height);
            g.Dispose();
            fpicture.Image = bmp;
        }

        private void zkFprint_OnFeatureInfo(object sender, IZKFPEngXEvents_OnFeatureInfoEvent e)
        {

            String strTemp = string.Empty;
            if (ZkFprint.EnrollIndex != 1)
            {
                if (ZkFprint.IsRegister)
                {
                    if (ZkFprint.EnrollIndex - 1 > 0)
                    {
                        int eindex = ZkFprint.EnrollIndex - 1;
                        strTemp = "Please scan again ..." + eindex;
                    }
                }
            }
            ShowHintInfo(strTemp);
        }

        private void zkFprint_OnEnroll(object sender, IZKFPEngXEvents_OnEnrollEvent e)
        {
            if (e.actionResult)
            {

                string template = ZkFprint.EncodeTemplate1(e.aTemplate);
                //txtTemplate.Text = template;

                DbConnection.checkConnection();
                try
                {
                    if (!(txtRegID.Text == "" || txtName.Text == "" || cb_sexe.Text == "" || template == "" || txt_phone.Text == "" || pictureBox1.Image == null || fpicture.Image == null || cb_fac.Text == "" || cb_prom.Text == ""))
                    {
                        SqlCommand sqlCommand = new SqlCommand("select * from Enrolment where Matricule='" + txtRegID.Text + "' AND Noms='" + txtName.Text + "';", DbConnection.con);
                        SqlDataReader mreader;
                        DbConnection.con.Open();
                        mreader = sqlCommand.ExecuteReader();
                        int count = 0;

                        while (mreader.Read())
                        {
                            count = count + 1;
                        }
                        if (count == 1)
                        {
                           // Duplicate Entry Dictected.
                           lblmsg.ForeColor = System.Drawing.Color.Red;
                           lblmsg.Text = "Cet utilisateur est déjà enregistré dans le système";
                        }
                        else
                        {
                            DbConnection.checkConnection();

                            SqlCommand cmd = new SqlCommand("insert into Enrolment (Matricule,Noms,Sexe,Telephone,Faculte,Promotion,Num_Rfid,FP_Key,Photo)values(@matricule,@noms,@sexe,@telephone,@fac,@prom,@num_rfid,@fp_key,@photo)", DbConnection.con);

                            MemoryStream stream = new MemoryStream();
                            pictureBox1.Image.Save(stream, System.Drawing.Imaging.ImageFormat.Jpeg);
                            byte[] picc = stream.ToArray();

                            cmd.Parameters.Add(new SqlParameter("@matricule", txtRegID.Text));
                            cmd.Parameters.Add(new SqlParameter("@noms", txtName.Text));
                            cmd.Parameters.Add(new SqlParameter("@sexe", cb_sexe.Text));
                            cmd.Parameters.Add(new SqlParameter("@telephone", txt_phone.Text));
                            cmd.Parameters.Add(new SqlParameter("@fac", cb_fac.Text));
                            cmd.Parameters.Add(new SqlParameter("@prom", cb_prom.Text));
                            cmd.Parameters.Add(new SqlParameter("@num_rfid", txt_rfid.Text));
                            cmd.Parameters.Add(new SqlParameter("@fp_key", template));
                            cmd.Parameters.Add(new SqlParameter("@photo", picc));

                            if (DbConnection.con.State == System.Data.ConnectionState.Closed)
                            {
                                DbConnection.con.Open();
                            }

                            int i = cmd.ExecuteNonQuery();

                            if (i != 0)
                            {
                                //ShowHintInfo("Registration successful. You can verify now");
                                //lblmsg.ForeColor = System.Drawing.Color.Green;
                                //lblmsg.Text = "Fingerprint Record Saved";
                                Reset();
                                template = "";
                                GetID();

                                MessageBox.Show("Fingerprint Record Saved", "Fingerprint Enrollment", MessageBoxButtons.OK, MessageBoxIcon.Information);

                                ZkFprint.CancelEnroll();
                                ZkFprint.EnrollCount = 3;
                                ZkFprint.BeginEnroll();
                                ShowHintInfo("Please give fingerprint sample.");
                            }
                            else
                            {
                                lblmsg.ForeColor = System.Drawing.Color.Red;
                                lblmsg.Text = "Try again";
                            }
                        }
                        DbConnection.con.Close();
                        
                    }
                    else
                    {
                        lblmsg.ForeColor = System.Drawing.Color.Red;
                        lblmsg.Text = "Input Validation: Some fields are empty";

                    }

                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
            else
            {
                ShowHintInfo("Error, please register again.");

            }
        }

        public void Reset()
        {
            txtRegID.Text = "";
            txtName.Text = "";
            cb_fac.Text = "";
            cb_prom.Text = "";
            txt_phone.Text = "";
            txt_rfid.Text = "";
            cb_sexe.SelectedIndex = -1;
            fpicture.Image = null;
            pictureBox1.Image = null;
            //lblmsg.Text = string.Empty;
        }

        private void ShowHintInfo(String s)
        {
            prompt.Text = s;
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            fpicture.Image = null;
        }

        private void btnBrowseImage_Click(object sender, EventArgs e)
        {
            // open file dialog   
            OpenFileDialog openFileDialog = new OpenFileDialog();
            // image filters  
            openFileDialog.Filter = "Image Files(*.jpg; *.jpeg; *.gif; *.bmp)|*.jpg; *.jpeg; *.gif; *.bmp";
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                // display image in picture box  
                pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
                pictureBox1.Image = new Bitmap(openFileDialog.FileName);
                // image file path  
                //textBox1.Text = open.FileName;
            }
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            try
            {
                grabber = new Capture();
                grabber.QueryFrame();

                //Initialize the FrameGraber event
                Application.Idle += new EventHandler(FrameGrabber);
                //button1.Enabled = false;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        void FrameGrabber(object sender, EventArgs e)
        {
            //Get the current frame form capture device
            currentFrame = grabber.QueryFrame().Resize(200, 185, Emgu.CV.CvEnum.INTER.CV_INTER_CUBIC);

            pictureBox1.Image = currentFrame.ToBitmap();

        }

        private void btnCapture_Click(object sender, EventArgs e)
        {
            //You'll want to unsubcribe from the event handler so this doesn't occur
            Application.Idle -= FrameGrabber;
            grabber.Dispose();
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            ZkFprint.EndInit();
            ZkFprint.EndEngine();
            this.Hide();
        }

        public static string GetUniqueKey(int maxSize)
        {
            char[] chars = new char[62];
            chars = "123456789".ToCharArray();
            byte[] data = new byte[1];
            RNGCryptoServiceProvider crypto = new RNGCryptoServiceProvider();
            crypto.GetNonZeroBytes(data);
            data = new byte[maxSize];
            crypto.GetNonZeroBytes(data);
            StringBuilder result = new StringBuilder(maxSize);
            foreach (byte b in data)
            {
                result.Append(chars[b % (chars.Length)]);
            }
            return result.ToString();
        }

        private void GetID()
        {
            txtRegID.Text = GetUniqueKey(6);
        }

        
    }
}
