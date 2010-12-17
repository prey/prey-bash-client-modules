using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Security.Cryptography;
using Microsoft.Win32;
using System.ServiceProcess;
using System.Collections;

namespace prey_lock_dotnet
{
    public partial class LockForm : Form
    {

        private String pass = "e75f0173be748b6f68b3feb61255693c";

        public LockForm()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
           // _hookID = SetHook(_proc);
            //Logger.debug("Starting lock");
            if (Environment.GetCommandLineArgs().Length >= 2)
                pass = Environment.GetCommandLineArgs()[1];
            //KeyboardFilter filter = new KeyboardFilter(new Keys[] { Keys.LWin, Keys.RWin, Keys.Escape, Keys.Alt, Keys.Tab, Keys.F4, Keys.F1, Keys.LaunchApplication1, Keys.LaunchApplication2, Keys.LaunchMail, Keys.BrowserHome, Keys.SelectMedia, Keys.Control });
            this.TopMost = true;
            this.Location = new Point(0, 0);
            this.FormBorderStyle = FormBorderStyle.None;
            this.Width = Screen.PrimaryScreen.Bounds.Width;
            this.Height = Screen.PrimaryScreen.Bounds.Height;
            this.blockScreens();
            this.BackColor = Color.Black;
            this.showBG();
            this.renderPasswordBox();
            this.renderErrorLabel();
            this.Activate();
            this.textPass.Focus();
            //TaskMgrHidder.hide();
        }


        private void renderPasswordBox() {
            this.textPass.Width = 420;
            this.textPass.Height = 50;
            int x = (this.Width - this.textPass.Width)/2;
            int y = this.Height / 2;
            Point p = new Point(x, y);
            this.textPass.Location = p;

        }

        private void renderErrorLabel()
        {
            int x = (this.Width - this.lblError.Width) / 2;
            int y = this.textPass.Bounds.Y + 40;
            Point p = new Point(x, y);
            this.lblError.Location = p;
            this.lblError.Hide();

        }

        private void showBG() {
            this.imgPrey.Width = 1024;
            this.imgPrey.Height = 960;
            int x = (this.Width - this.imgPrey.Width) / 2;
            int y = (this.Height - this.imgPrey.Height) / 2;
            Point p = new Point(x,y);
            this.imgPrey.Location = p;
            ModifyRegistry registry = new ModifyRegistry();
            String imgPath = registry.Read("Path") + "\\modules\\lock\\lib\\bg-lock-with-input.png";
            this.imgPrey.Image = Image.FromFile(imgPath);

        }
        private void blockScreens()
        {
            foreach (Screen s in Screen.AllScreens) {
                if (!s.Primary)
                {
                    Form f = new Form();
                    f.StartPosition = FormStartPosition.Manual;
                    f.TopMost = true;
                    f.FormBorderStyle = FormBorderStyle.None;
                    f.BackColor = Color.Black;
                    f.Bounds = s.Bounds;
                    f.Show();
                    
                }
            }

        }

        private void CheckPass(object sender, System.Windows.Forms.KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)13)
            {
                if (EncodePassword(this.textPass.Text).Equals(pass))
                {
                    //Application.Exit(66);
                    Environment.Exit(66);
                }
                else
                {
                    this.textPass.SelectAll();
                    this.lblError.Show();
                    timerLabel.Start();
                }
            }
        }

        public string EncodePassword(string originalPassword)
        {
            System.Security.Cryptography.MD5CryptoServiceProvider x = new System.Security.Cryptography.MD5CryptoServiceProvider();
            byte[] bs = System.Text.Encoding.UTF8.GetBytes(originalPassword);
            bs = x.ComputeHash(bs);
            System.Text.StringBuilder s = new System.Text.StringBuilder();
            foreach (byte b in bs)
            {
                s.Append(b.ToString("x2").ToLower());
            }
            string password = s.ToString();
            return password;
        }

        private void timerLabel_Tick(object sender, EventArgs e)
        {
            
            timerLabel.Stop();
            this.lblError.Hide();
        }


        private void timerAlwaysOnTop_Tick(object sender, EventArgs e)
        {


            //this.closeTaskManager();
            if (!this.ContainsFocus || !this.textPass.Focused)
            {
                foreach (Form form in Application.OpenForms)
                {
                    form.BringToFront();
                }
                this.BringToFront();
                this.textPass.Focus();
                this.Activate();
            }
        }
/*
        private void closeTaskManager()
        {
            int taskManager = FindWindow("#32770", "Windows Task Manager");
            if (taskManager == 0)
            {
                Process[] processes = Process.GetProcessesByName("taskmgr");
                foreach (Process p in processes)
                {
                    IntPtr wHandle = p.MainWindowHandle;
                    taskManager = (int)wHandle;
                }
            }
            if (taskManager != 0)
                {
                    const int WM_CLOSE = 0x0010;
                    SendMessage(taskManager, WM_CLOSE, 0, 0);
                }
        }
*/
       
    }




}
