using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BiometricFinEnrolmentVerificationZkteco.Resources
{
    public partial class Demarrage : Form
    {
        public Demarrage()
        {
            InitializeComponent();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            timer1.Start();
            if (progressBar1.Value < 100)
            {
                progressBar1.Value += 1;
                if(progressBar1.Value <= 20) { label2.Text = "Chargement en cours..."; }
                else if (progressBar1.Value <= 50) { label2.Text = "Bienvenu dans le système de controle des frais..."; }
                else if (progressBar1.Value <= 70) { label2.Text = "Il vous 5 secondes..."; }
                else if (progressBar1.Value <= 90) { label2.Text = "C'est parti..."; }

            }
            else if (progressBar1.Value == 100) 
            {
                timer1 .Stop();
                Connexion con = new Connexion();
                con.Show();
                this.Hide();
            }
            label3.Text = progressBar1.Value + "%";
        }

        private void Demarrage_Load(object sender, EventArgs e)
        {
            timer1.Start();
        }
    }
}
