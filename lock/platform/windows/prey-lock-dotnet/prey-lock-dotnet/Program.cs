using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Drawing;

namespace prey_lock_dotnet
{
    static class Program
    {
        private static KeyboardFilter filter;
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            filter = new KeyboardFilter(new Keys[] { Keys.LWin, Keys.RWin, Keys.Escape, Keys.Alt, Keys.Tab, Keys.F4, Keys.F1, Keys.LaunchApplication1, Keys.LaunchApplication2, Keys.LaunchMail, Keys.BrowserHome, Keys.SelectMedia, Keys.Control });
            filter.run();
            try
            {
                Application.Run(new LockForm());
            }
            catch (Exception)
            {
                Console.WriteLine("Exception caught... but lock won't die hehe!") ;
            }
        }
    }
}
