
using System;
using Microsoft.Win32;
using System.Diagnostics;


namespace prey_lock_dotnet
{
	public class ModifyRegistry
	{

		private string subKey = "SOFTWARE\\Prey";
		/// <summary>
		/// A property to set the SubKey value
		/// (default = "SOFTWARE\\" + Application.ProductName.ToUpper())
		/// </summary>
		public string SubKey
		{
			get { return subKey; }
			set	{ subKey = value; }
		}

		private RegistryKey baseRegistryKey = Registry.LocalMachine;
		/// <summary>
		/// A property to set the BaseRegistryKey value.
		/// (default = Registry.LocalMachine)
		/// </summary>
		public RegistryKey BaseRegistryKey
		{
			get { return baseRegistryKey; }
			set	{ baseRegistryKey = value; }
		}

		/* **************************************************************************
		 * **************************************************************************/

		/// <summary>
		/// To read a registry key.
		/// input: KeyName (string)
		/// output: value (string) 
		/// </summary>
		public string Read(string KeyName)
		{
			// Opening the registry key
			RegistryKey rk = baseRegistryKey ;
			// Open a subKey as read-only
			RegistryKey sk1 = rk.OpenSubKey(subKey);
			// If the RegistrySubKey doesn't exist -> (null)
			if ( sk1 == null )
			{
				return null;
			}
			else
			{
				try 
				{
					// If the RegistryKey exists I get its value
					// or null is returned.
					return (string)sk1.GetValue(KeyName.ToUpper());
				}
				catch (Exception e)
				{
#if DEBUG
                    PreyLogger.error(e.Message);
#endif
					return null;
				}
			}
		}	

		/* **************************************************************************
		 * **************************************************************************/

		/// <summary>
		/// To write into a registry key.
		/// input: KeyName (string) , Value (object)
		/// output: true or false 
		/// </summary>
		public bool Write(string KeyName, object Value)
		{
			try
			{
				// Setting
				RegistryKey rk = baseRegistryKey ;
				// I have to use CreateSubKey 
				// (create or open it if already exits), 
				// 'cause OpenSubKey open a subKey as read-only
				RegistryKey sk1 = rk.CreateSubKey(subKey);
				// Save the value
				sk1.SetValue(KeyName.ToUpper(), Value);
				return true;
			}
			catch (Exception e)
			{
#if DEBUG
                PreyLogger.error(e.Message);
#endif
				return false;
			}
		}

        

		/* **************************************************************************
		 * **************************************************************************/

		/// <summary>
		/// To delete a registry key.
		/// input: KeyName (string)
		/// output: true or false 
		/// </summary>
		public bool DeleteKey(string KeyName)
		{
			try
			{
				// Setting
				RegistryKey rk = baseRegistryKey ;
				RegistryKey sk1 = rk.CreateSubKey(subKey);
				// If the RegistrySubKey doesn't exists -> (true)
				if ( sk1 == null )
					return true;
				else
					sk1.DeleteValue(KeyName);

				return true;
			}
			catch (Exception e)
			{
#if DEBUG
                PreyLogger.error(e.Message);
#endif
				return false;
			}
		}

		/* **************************************************************************
		 * **************************************************************************/

		/// <summary>
		/// To delete a sub key and any child.
		/// input: void
		/// output: true or false 
		/// </summary>
		public bool DeleteSubKeyTree()
		{
			try
			{
				// Setting
				RegistryKey rk = baseRegistryKey ;
				RegistryKey sk1 = rk.OpenSubKey(subKey);
				// If the RegistryKey exists, I delete it
				if ( sk1 != null )
					rk.DeleteSubKeyTree(subKey);

				return true;
			}
			catch (Exception e)
			{
#if DEBUG
                PreyLogger.error(e.Message);
#endif
				return false;
			}
		}

		/* **************************************************************************
		 * **************************************************************************/

		/// <summary>
		/// Retrive the count of subkeys at the current key.
		/// input: void
		/// output: number of subkeys
		/// </summary>
		public int SubKeyCount()
		{
			try
			{
				// Setting
				RegistryKey rk = baseRegistryKey ;
				RegistryKey sk1 = rk.OpenSubKey(subKey);
				// If the RegistryKey exists...
				if ( sk1 != null )
					return sk1.SubKeyCount;
				else
					return 0; 
			}
			catch (Exception e)
			{
#if DEBUG
                PreyLogger.error(e.Message);
#endif
				return 0;
			}
		}

		/* **************************************************************************
		 * **************************************************************************/

		/// <summary>
		/// Retrive the count of values in the key.
		/// input: void
		/// output: number of keys
		/// </summary>
		public int ValueCount()
		{
			try
			{
				// Setting
				RegistryKey rk = baseRegistryKey ;
				RegistryKey sk1 = rk.OpenSubKey(subKey);
				// If the RegistryKey exists...
				if ( sk1 != null )
					return sk1.ValueCount;
				else
					return 0; 
			}
			catch (Exception e)
			{
#if DEBUG
               PreyLogger.error(e.Message);
#endif
				return 0;
			}
		}

		
	}
}
