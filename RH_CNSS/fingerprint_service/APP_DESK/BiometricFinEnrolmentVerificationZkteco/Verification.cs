using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SqlClient;
using AxZKFPEngXControl;
using System.IO;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace BiometricFinEnrolmentVerificationZkteco
{
    public partial class Verification : Form
    {
        SqlConnection con;
        SqlCommand cmd;
        SqlDataReader dr;
        DataTable dt;
        SqlDataAdapter da;
        private AxZKFPEngX ZkFprint = new AxZKFPEngX();
        //private bool Check;
        public bool StopAutoCheckin { get; set; }
        public Verification()
        {
            InitializeComponent();
        }

        private void Verification_Load(object sender, EventArgs e)
        {
            Controls.Add(ZkFprint);
            InitialAxZkfp();
            txt_rfid.Select();
            con = new SqlConnection("Data Source=(LocalDB)\\MSSQLLocalDB;AttachDbFilename=C:\\Users\\Lingole\\Desktop\\FP_Project\\GestionEtudiants.mdf;Integrated Security=True;Connect Timeout=30");
            cmd = new SqlCommand("", con);

        }

        private void InitialAxZkfp()
        {
            try
            {

                ZkFprint.OnImageReceived += zkFprint_OnImageReceived;
                ZkFprint.OnFeatureInfo += zkFprint_OnFeatureInfo;
                //zkFprint.OnFingerTouching 
                //zkFprint.OnFingerLeaving
                //ZkFprint.OnEnroll += zkFprint_OnEnroll;

                if (ZkFprint.InitEngine() == 0)
                {
                    ZkFprint.FPEngineVersion = "9";
                    ZkFprint.EnrollCount = 3;
                    txtdeviceSerial.Text = " " + ZkFprint.SensorSN + " Count: " + ZkFprint.SensorCount.ToString() + " Index: " + ZkFprint.SensorIndex.ToString();
                    ShowHintInfo("Device successfully connected");

                    if (ZkFprint.IsRegister)
                    {
                        ZkFprint.CancelEnroll();
                    }
                    ZkFprint.OnCapture += zkFprint_OnCapture;
                    ZkFprint.BeginCapture();
                    ShowHintInfo("Please give fingerprint sample.");
                }
                else
                {
                    ShowHintInfo("Device disconnected");
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

        private void zkFprint_OnCapture(object sender, IZKFPEngXEvents_OnCaptureEvent e)
        {
            string key = ZkFprint.EncodeTemplate1(e.aTemplate);

            // Get finger print key
            //string key = _fpEngine.GetTemplateAsString();

            // Check the key with all persons in the class
            DbConnection.checkConnection();
            SqlDataReader sqlDataReader;

            SqlCommand sqlCommand = new SqlCommand("SELECT Matricule, Noms,Sexe , Telephone, Faculte,Promotion, Num_rfid, FP_Key, Photo FROM Enrolment", DbConnection.con);

            if (DbConnection.con.State == System.Data.ConnectionState.Closed)
            {
                DbConnection.con.Open();
            }
            sqlDataReader = sqlCommand.ExecuteReader();

            // Store all persons that register this class into a list
            List<PerItem> lstStd = new List<PerItem>();
            while (sqlDataReader.Read())
            {
                lstStd.Add(new PerItem
                {
                    Matricule = (string)sqlDataReader["Matricule"],
                    Noms = (string)sqlDataReader["Noms"],
                    Sexe = (string)sqlDataReader["Sexe"],
                    Telephone = (string)sqlDataReader["Telephone"],
                    Faculte = (string)sqlDataReader["Faculte"],
                    Promotion = (string)sqlDataReader["Promotion"],
                    Num_Rfid = (string)sqlDataReader["Num_Rfid"],
                    FP_Key = (string)sqlDataReader["FP_Key"],
                    //Photo = sqlDataReader["Photo"]
                }
                    );
            }
            sqlDataReader.Close();
            DbConnection.con.Close();

            // Search a person that has a finger key matchs with key from finger print device 
            foreach (PerItem item in lstStd)
            {
                bool bRegChanged = false;       // Not use but we need to have it
                bool bMatched = false;          // Return value from verify 2 keys   
                string regKey = item.FP_Key;    // person's finger print key
                bMatched = ZkFprint.VerFingerFromStr(ref regKey, key, false, ref bRegChanged);
                // If key from device matched with the person's key
                if (bMatched == true)
                {

                    // Update result
                    txtRegID.Text = item.Matricule;
                    txtName.Text = item.Noms;
                    txt_phone.Text = item.Telephone;
                    txt_fac.Text = item.Faculte;
                    txt_prom.Text = item.Promotion;
                    txt_sexe.Text = item.Sexe;
                    txt_rfid.Text = item.Num_Rfid;

                    DbConnection.checkConnection();

                    string strcom = "select Photo from Enrolment where Matricule='" + item.Matricule + "'";
                    SqlDataAdapter daDetails = new SqlDataAdapter(strcom, DbConnection.con);
                    DataSet dsDetails = new DataSet();
                    daDetails.Fill(dsDetails);

                    DbConnection.con.Open();

                    if (dsDetails.Tables[0].Rows.Count > 0)
                    {
                        MemoryStream ms = new MemoryStream((byte[])dsDetails.Tables[0].Rows[0]["Photo"]);
                        pictureBox1.Image = new Bitmap(ms);

                    }
                    DbConnection.con.Close();

                    ShowHintInfo("Verified");
                    // here we can put codes for 

                    ZkFprint.CancelEnroll();

                    return;
                }
                if (bMatched == false)
                {
                    //txtError.Visible = true;
                    Reset();
                    ShowHintInfo("Not Verified");
                    ZkFprint.CancelEnroll();
                }
            }

            //if (ZkFprint.VerFingerFromStr(ref template, txtTemplate.Text, false, ref Check))
            //{
            //    ShowHintInfo("Verified");
            //}
            //else
            //    ShowHintInfo("Not Verified");

        }

        public class PerItem
        {
            public string Matricule { get; set; }
            public string Noms { get; set; }
            public string Sexe { get; set; }
            public string Telephone { get; set; }
            public string Faculte { get; set; }
            public string Promotion { get; set; }
            public string Num_Rfid { get; set; }
            public string FP_Key { get; set; }
            public byte Photo { get; set; }
        }

        private void Verification_FormClosed(object sender, FormClosedEventArgs e)
        {
            ZkFprint.EndInit();
            ZkFprint.EndEngine();
        }

        public void GetStopAutoCheckin(ref bool bValue)
        {
            bValue = StopAutoCheckin;
        }

        public void Reset()
        {
            txtRegID.Text = "";
            txtName.Text = "";
            txt_phone.Text = "";
            txt_fac.Text = "";
            txt_rfid.Text = "";
            txt_prom.Text = "";
            pictureBox1.Image = null;
            fpicture.Image = null;
            txt_sexe.Text = "";
            //txtFinger.Text = string.Empty;
            lblmsg.Text = string.Empty;
            txt_rfid.Select();

        }

        private void ShowHintInfo(String s)
        {
            prompt.Text = s;
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            StopAutoCheckin = true;
            ZkFprint.EndInit();
            ZkFprint.EndEngine();
            this.Close();
        }


        public void rechercher()
        {
            
        }
        private void txt_rfid_TextChanged_1(object sender, EventArgs e)
        {

            con = new SqlConnection("Data Source=(LocalDB)\\MSSQLLocalDB;AttachDbFilename=C:\\Users\\Lingole\\Desktop\\FP_Project\\GestionEtudiants.mdf;Integrated Security=True;Connect Timeout=30");
            cmd = new SqlCommand("", con);
            try
            {
                con.Open();
                cmd.CommandType = CommandType.Text;
                cmd.CommandText = ("select Matricule, Noms, Sexe, Telephone, Faculte, Promotion,Photo from Enrolment where Num_Rfid='" + txt_rfid.Text + "'");

                dr = cmd.ExecuteReader();
                while (dr.Read())
                {
                    txtRegID.Text = dr[0].ToString();
                    txtName.Text = dr[1].ToString();
                    txt_sexe.Text = dr[2].ToString();
                    txt_phone.Text = dr[3].ToString();
                    txt_fac.Text = dr[4].ToString();
                    txt_prom.Text = dr[5].ToString();
                    // Charger et afficher la photo
                    if (dr["Photo"] != DBNull.Value)
                    {
                        byte[] photoBytes = (byte[])dr["Photo"];
                        using (MemoryStream ms = new MemoryStream(photoBytes))
                        {
                            pictureBox1.Image = Image.FromStream(ms);
                        }
                    }
                }

                con.Close();

            }
            catch (Exception ex)
            {

                MessageBox.Show("erreur " + ex.Message, "Message", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
            
        }

        private void btnRecommencer_Click(object sender, EventArgs e)
        {
            Reset();
           
        }
        
    }
}

