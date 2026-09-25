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
using System.Xml.Linq;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace BiometricFinEnrolmentVerificationZkteco
{
    public partial class Utilisateur : Form
    {
        public Utilisateur()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void btn_ajouter_Click(object sender, EventArgs e)
        {
            DbConnection.checkConnection();
            try
            {
                SqlCommand cmd = new SqlCommand("select * from Utilisateur where Password='" + txt_password.Text + "' AND Username='" + txt_username.Text + "';", DbConnection.con);
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
                    MessageBox.Show("Cet utilisateur existe dejà dans la base de données!", "Input Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);

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
            if (txt_noms.Text == "" || cb_typeuser.Text == "" || txt_password.Text == "" || txt_username.Text == "" )
            {
                MessageBox.Show("certains de vos champs sonts vides", "Input Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
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

                    string cb = "insert into Utilisateur(Noms,Type_user,Username,Password) VALUES ('" + txt_noms.Text + "','" + cb_typeuser.Text + "','" + txt_username.Text + "','" + txt_password.Text + "')";

                    cmd = new SqlCommand(cb);
                    cmd.Connection = DbConnection.con;
                    cmd.ExecuteReader();
                    DbConnection.con.Close();
                    MessageBox.Show("le compte a été crée avec succès", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    Reset();
                    ActualiserDataGridView();

                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }
        #endregion
        #region Modify Admin
        private void Modifier()
        {
            DbConnection.checkConnection();
            if (txt_noms.Text == "" || cb_typeuser.Text == "" || txt_password.Text == "" || txt_username.Text == "")
            {
                MessageBox.Show("certains de vos champs sonts vides", "Input Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
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

                    string cb = "update  Utilisateur set Type_user='"+cb_typeuser.Text+"',Username='"+txt_username.Text+"',Password='"+txt_password.Text+"' where Noms='"+txt_noms.Text+"'";

                    cmd = new SqlCommand(cb);
                    cmd.Connection = DbConnection.con;
                    cmd.ExecuteReader();
                    DbConnection.con.Close();
                    MessageBox.Show("Modification effectuée avec succès", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    Reset();
                    ActualiserDataGridView();

                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }
        #endregion
        #region supprimer Admin
        private void Supprimer()
        {
            DbConnection.checkConnection();
            if (txt_noms.Text == "" || cb_typeuser.Text == "" || txt_password.Text == "" || txt_username.Text == "")
            {
                MessageBox.Show("certains de vos champs sonts vides", "Input Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            //else if (textBoxpass.Text != textBoxrepass.Text)
            //{
            //    MessageBox.Show("Both password must be match", "Error", MessageBoxButtons.OK, MessageBoxIcon.Stop);
            //}
            else
            {
                try
                {
                    DialogResult result = MessageBox.Show("Voulez-vous vraiment supprimer cet ulisateur de la base de données?", "Confirmation", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                    if (result == DialogResult.Yes)
                    {
                        SqlCommand cmd = new SqlCommand();
                        DbConnection.con.Open();

                        string cb = "delete from  Utilisateur where Noms='" + txt_noms.Text + "'";

                        cmd = new SqlCommand(cb);
                        cmd.Connection = DbConnection.con;
                        cmd.ExecuteReader();
                        DbConnection.con.Close();
                        MessageBox.Show("Suppression de l'utilisateur effectuée avec succès", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        Reset();
                        ActualiserDataGridView();
                    }

                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }
        #endregion
        private void ActualiserDataGridView()
        {
            // Réinitialiser les données du DataGridView
            dataGridView1.DataSource = null;

            // Recharger les données depuis la base de données
            string query = "SELECT * FROM Utilisateur";
            SqlDataAdapter adapter = new SqlDataAdapter(query, DbConnection.con);
            DataTable dataTable = new DataTable();
            adapter.Fill(dataTable);

            // Afficher les données dans le DataGridView
            dataGridView1.DataSource = dataTable;
        }
        private void Rechercher()
        {
            // Réinitialiser les données du DataGridView
            dataGridView1.DataSource = null;

            // Recharger les données depuis la base de données
            string query = "SELECT * FROM Utilisateur where Noms Like'%" + txt_rechercher.Text + "%' or Username Like'%" + txt_rechercher.Text + "%'";
            SqlDataAdapter adapter = new SqlDataAdapter(query, DbConnection.con);
            DataTable dataTable = new DataTable();
            adapter.Fill(dataTable);

            // Afficher les données dans le DataGridView
            dataGridView1.DataSource = dataTable;
        }
        public void Reset()
        {
            
            txt_noms.Text = "";
            txt_password.Text = string.Empty;
            txt_username.Text = string.Empty;
            cb_typeuser.SelectedIndex = -1;

        }

        private void Utilisateur_Load(object sender, EventArgs e)
        {
            ActualiserDataGridView();
        }

        private void txt_rechercher_TextChanged(object sender, EventArgs e)
        {
            Rechercher();
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            // Vérifier si la ligne sélectionnée n'est pas l'en-tête
            if (e.RowIndex >= 0)
            {
                // Récupérer la ligne sélectionnée
                DataGridViewRow row = dataGridView1.Rows[e.RowIndex];

                // Remplir les contrôles avec les valeurs de la ligne sélectionnée
                txt_noms.Text = row.Cells["Noms"].Value.ToString(); // Remplacer "Numero" par le nom de la colonne correspondant à textBox1
                cb_typeuser.Text = row.Cells["Type_user"].Value.ToString(); // Remplacer "AutreChamp" par le nom de la colonne correspondant à textBox3
                txt_username.Text = row.Cells["Username"].Value.ToString();
                txt_password.Text = row.Cells["Password"].Value.ToString();

                


            }
        }

        private void btn_modifier_Click(object sender, EventArgs e)
        {
            Modifier();
        }

        private void btn_supprimer_Click(object sender, EventArgs e)
        {
            Supprimer();
        }

        private void btn_quitter_Click(object sender, EventArgs e)
        {
            DialogResult result = MessageBox.Show("Voulez-vous vraiment fermer cet application?", "Confirmation", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (result == DialogResult.Yes)
            {
                this.Close();
            }
              
        }
    }
}

