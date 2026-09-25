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

namespace BiometricFinEnrolmentVerificationZkteco
{
    public partial class Login : Form
    {
        public string uType;
        public Login()
        {
            InitializeComponent();
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            LoginAdmin();
        }

        #region LogIN
        private void LoginAdmin()
        {
            DbConnection.checkConnection();
            try
            {
                SqlCommand cmd = new SqlCommand("select Type_user from Utilisateur where Username='" + this.textBoxUserName.Text + "' AND Password='" + this.textBoxPassword.Text + "';", DbConnection.con);
                SqlDataReader mreader;
                DbConnection.con.Open();
                mreader = cmd.ExecuteReader();
                int count = 0;

                if (mreader.Read())
                {
                    count = count + 1;

                    
                    uType = (mreader.GetString(0));
                }
                if (count == 1)
                {
                    if (uType == "Admin")
                    {
                        Main main = new Main();
                        main.Show();
                        this.Hide();
                    }
                    else if(uType == "User")
                    {
                        UserMain userMain = new UserMain();
                        userMain.Show();
                        this.Hide();
                    }
                    
                }
                else
                {
                    MessageBox.Show("Wrong username or password!", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
                DbConnection.con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
        #endregion

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void Login_Load(object sender, EventArgs e)
        {

        }
    }
}
