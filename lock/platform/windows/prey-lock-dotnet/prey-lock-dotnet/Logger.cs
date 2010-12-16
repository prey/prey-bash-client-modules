using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace prey_lock_dotnet
{
    class Logger
    {

        public static void debug(String text){
            StreamWriter log = File.AppendText("c:\\Temp\\lock.log");
            log.WriteLine(text);
            log.Flush();
            log.Close();
        }
    }
}
