using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BiometricFinEnrolmentVerificationZkteco
{
    public partial class UserMain : Form
    {
        public UserMain()
        {
            InitializeComponent();
        }

        private void verificationStripMenuItem1_Click(object sender, EventArgs e)
        {
            Verification verification = new Verification();
            verification.ShowDialog();
        }

        private void LogoutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void UserMain_Load(object sender, EventArgs e)
        {

        }
    }
}
