namespace prey_lock_dotnet
{
    partial class LockForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.imgPrey = new System.Windows.Forms.PictureBox();
            this.textPass = new System.Windows.Forms.TextBox();
            this.lblError = new System.Windows.Forms.Label();
            this.timerLabel = new System.Windows.Forms.Timer(this.components);
            this.timerAlwaysOnTop = new System.Windows.Forms.Timer(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.imgPrey)).BeginInit();
            this.SuspendLayout();
            // 
            // imgPrey
            // 
            this.imgPrey.Location = new System.Drawing.Point(146, 114);
            this.imgPrey.Name = "imgPrey";
            this.imgPrey.Size = new System.Drawing.Size(119, 68);
            this.imgPrey.TabIndex = 2;
            this.imgPrey.TabStop = false;
            // 
            // textPass
            // 
            this.textPass.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textPass.CausesValidation = false;
            this.textPass.Font = new System.Drawing.Font("Microsoft Sans Serif", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textPass.Location = new System.Drawing.Point(146, 56);
            this.textPass.MaxLength = 20;
            this.textPass.Name = "textPass";
            this.textPass.PasswordChar = '*';
            this.textPass.Size = new System.Drawing.Size(100, 23);
            this.textPass.TabIndex = 3;
            this.textPass.UseSystemPasswordChar = true;
            this.textPass.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.CheckPass);
            // 
            // lblError
            // 
            this.lblError.AutoSize = true;
            this.lblError.CausesValidation = false;
            this.lblError.Font = new System.Drawing.Font("Calibri", 16F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblError.ForeColor = System.Drawing.Color.Red;
            this.lblError.Location = new System.Drawing.Point(48, 231);
            this.lblError.Name = "lblError";
            this.lblError.Size = new System.Drawing.Size(334, 27);
            this.lblError.TabIndex = 4;
            this.lblError.Text = "Incorrect password! Access denied.";
            this.lblError.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.lblError.UseMnemonic = false;
            // 
            // timerLabel
            // 
            this.timerLabel.Interval = 2000;
            this.timerLabel.Tick += new System.EventHandler(this.timerLabel_Tick);
            // 
            // timerAlwaysOnTop
            // 
            this.timerAlwaysOnTop.Tick += new System.EventHandler(this.timerAlwaysOnTop_Tick);
            // 
            // LockForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(440, 352);
            this.Controls.Add(this.lblError);
            this.Controls.Add(this.textPass);
            this.Controls.Add(this.imgPrey);
            this.Name = "LockForm";
            this.Text = "Prey Lock";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.imgPrey)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox imgPrey;
        private System.Windows.Forms.TextBox textPass;
        private System.Windows.Forms.Label lblError;
        private System.Windows.Forms.Timer timerLabel;
        private System.Windows.Forms.Timer timerAlwaysOnTop;
    }
}

