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
    public partial class Principal : Form
    {
        public Principal()
        {
            InitializeComponent();
        }

        private void enrollToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Etudiant et=new Etudiant();
            et.ShowDialog();
        }

        private void paiementToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Promotion promotion = new Promotion();
            promotion.ShowDialog();
        }

        private void pToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Paiement paiement = new Paiement();
            paiement.ShowDialog();
        }

        private void verificationToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Control_Frais control_Frais = new Control_Frais();
            control_Frais.ShowDialog();
        }

        private void quitterToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Admin admin = new Admin();
            admin.ShowDialog();
        }

        private void quitterToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
