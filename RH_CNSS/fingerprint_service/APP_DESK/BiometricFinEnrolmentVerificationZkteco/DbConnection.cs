using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;
using System.Data;

namespace BiometricFinEnrolmentVerificationZkteco
{
    internal class DbConnection
    {
        public static SqlConnection con = new SqlConnection("Data Source=(LocalDB)\\MSSQLLocalDB;AttachDbFilename=C:\\Users\\Lingole\\Desktop\\FASIA\\FP_Project\\BiometricFinEnrolmentVerificationZkteco\\bin\\Debug\\BD_FASIA.mdf;Integrated Security=True;Connect Timeout=30");

        public static void checkConnection()
        {
            if (DbConnection.con.State == ConnectionState.Open)
            {
                DbConnection.con.Close();
            }
        }
    }
}
