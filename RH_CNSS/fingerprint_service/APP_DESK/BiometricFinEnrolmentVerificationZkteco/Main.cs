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
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }

        private void enrolmentStripMenuItem1_Click(object sender, EventArgs e)
        {
            Enrolment enrolment = new Enrolment();
            enrolment.ShowDialog();
        }

        private void verificationStripMenuItem1_Click(object sender, EventArgs e)
        {
            Verification verification = new Verification();
            verification.ShowDialog();
        }

        private void RegAdminToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AdminRegister adminRegister = new AdminRegister();
            adminRegister.ShowDialog();
        }

        private void LogoutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void Main_Load(object sender, EventArgs e)
        {

        }

        private void StudentsToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void addUserToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Utilisateur ut = new Utilisateur();
            ut.ShowDialog();
        }
    }
}
