using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Windows.Forms;
using System.Runtime.InteropServices;

namespace prey_lock_dotnet
{
    public class KeyboardFilter
    {
        private Keys[] mFilter;
        private IntPtr mHook;
        private LowLevelKeyboardProc mProc;

        public KeyboardFilter(Keys[] keysToFilter)
        {
            // Install hook 
            try
            {
                mFilter = keysToFilter;
                ProcessModule mod = Process.GetCurrentProcess().MainModule;
                mProc = new LowLevelKeyboardProc(KeyboardProc); // Avoid garbage collector problems 
                mHook = SetWindowsHookEx(13, mProc, GetModuleHandle(mod.ModuleName), 0);
            
                if (mHook == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(), "Failed to set hook");
            }
            catch (Exception)
            {
                
                return;
            }
        }
        public void Dispose()
        {
            // Release hook 
            if (mHook != IntPtr.Zero)
            {
                UnhookWindowsHookEx(mHook);
                mHook = IntPtr.Zero;
            }
        }
        private IntPtr KeyboardProc(int nCode, IntPtr wp, IntPtr lp)
        {
            // Callback, filter key 
            try
            {
                if (nCode >= 0)
                {
                    KBDLLHOOKSTRUCT info = (KBDLLHOOKSTRUCT)Marshal.PtrToStructure(lp, typeof(KBDLLHOOKSTRUCT));
//                    Logger.debug(info.key.ToString());
                    foreach (Keys key in mFilter)
                        if ((key & Keys.KeyCode) == info.key && CheckModifier(key)) return (IntPtr)1;
                }
                return CallNextHookEx(mHook, nCode, wp, lp);
            }
            catch (Exception)
            {
                return CallNextHookEx(mHook, nCode, wp, lp);
            }
        }
        private bool CheckModifier(Keys key)
        {
            // Check if modifier key in required state 
            if ((key & Keys.Control) == Keys.Control &&
                GetAsyncKeyState(Keys.LControlKey) == 0 && GetAsyncKeyState(Keys.RControlKey) == 0) return false;
            if ((key & Keys.Shift) == Keys.Shift &&
                GetAsyncKeyState(Keys.LShiftKey) == 0 && GetAsyncKeyState(Keys.RShiftKey) == 0) return false;
            if ((key & Keys.Alt) == Keys.Alt &&
                GetAsyncKeyState(Keys.LMenu) == 0 && GetAsyncKeyState(Keys.RMenu) == 0) return false;
            return true;
        }

        // P/Invoke declarations 
        [StructLayout(LayoutKind.Sequential)]
        private struct KBDLLHOOKSTRUCT
        {
            public Keys key;
            public int scanCode;
            public int flags;
            public int time;
            public IntPtr extra;
        }
        private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr SetWindowsHookEx(int id, LowLevelKeyboardProc callback, IntPtr hMod, uint dwThreadId);
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern bool UnhookWindowsHookEx(IntPtr hook);
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr CallNextHookEx(IntPtr hook, int nCode, IntPtr wp, IntPtr lp);
        [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr GetModuleHandle(string name);
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        private static extern short GetAsyncKeyState(Keys key);
    } 
}
