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
    public partial class AdminRegister : Form
    {
        public AdminRegister()
        {
            InitializeComponent();
        }

        private void btnRegister_Click(object sender, EventArgs e)
        {
            DbConnection.checkConnection();
            try
            {
                SqlCommand cmd = new SqlCommand("select * from RegisterUser where Name='" + txtName.Text + "' AND Username='" + txtUsername.Text + "';", DbConnection.con);
                SqlDataReader mreader;
                DbConnection.con.Open();
                mreader = cmd.ExecuteReader();
                int count = 0;
                while (mreader.Read())
                {
                    count = count + 1;
                }
                if (count == 1)
                {
                    //Display error message
                    MessageBox.Show("User Exist!", "Input Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    
                }
                else
                {
                    CreateUser();
                }
                DbConnection.con.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        #region Create Admin
        private void CreateUser()
        {
            DbConnection.checkConnection();
            if (txtContactNo.Text == "" || txtEmailID.Text == "" || txtName.Text == "" || txtPassword.Text == "" || txtUsername.Text == "" || cmbUserType.Text == "")
            {
                MessageBox.Show("Can't submit empty form", "Input Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            //else if (textBoxpass.Text != textBoxrepass.Text)
            //{
            //    MessageBox.Show("Both password must be match", "Error", MessageBoxButtons.OK, MessageBoxIcon.Stop);
            //}
            else
            {
                try
                {
                    SqlCommand cmd = new SqlCommand();
                    DbConnection.con.Open();

                    string cb = "insert into RegisterUser(Name,Email,Usertype,Username,Password,ContactNo) VALUES ('" + txtName.Text + "','" + txtEmailID.Text + "','" + cmbUserType.Text + "','" + txtUsername.Text + "','" + txtPassword.Text + "','" + txtContactNo.Text + "')";

                    cmd = new SqlCommand(cb);
                    cmd.Connection = DbConnection.con;
                    cmd.ExecuteReader();
                    DbConnection.con.Close();
                    MessageBox.Show("Account successfully created", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    Reset();
                    
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }
        #endregion

        public void Reset()
        {
            txtContactNo.Text = string.Empty;
            txtEmailID.Text = string.Empty;
            txtName.Text = string.Empty;
            txtPassword.Text = string.Empty;
            txtUsername.Text = string.Empty;
            cmbUserType.SelectedIndex = -1;

        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            this.Hide();
        }

        private void AdminRegister_Load(object sender, EventArgs e)
        {

        }
    }
}
