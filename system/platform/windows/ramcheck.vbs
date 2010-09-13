'Script for Win32_PhysicalMemory WMI Class
'Generated using 'WMI Win32 Class Autoscript Generator' - Developed by Karthikeyan
'Homepage: http://www.geocities.com/marskarthik

On Error Resume Next
Computer = "."
Set OutFile = CreateObject("WScript.Shell")
'Const ForAppending = 2
'Set FileSystem = CreateObject("Scripting.FileSystemObject")
'Set TextFile = FileSystem.OpenTextFile ("c:\Win32_PhysicalMemory.txt", ForAppending, True)
Wscript.Echo "Script for Win32_PhysicalMemory Class by Karthikeyan"
Wscript.Echo
Set WMIService = GetObject("winmgmts:\\" & Computer & "\root\cimv2")
Set Items = WMIService.ExecQuery("Select * from Win32_PhysicalMemory",,48)
For Each SubItems in Items
Wscript.Echo "==============================="
    Wscript.Echo "BankLabel: " & SubItems.BankLabel
    Wscript.Echo "Capacity: " & SubItems.Capacity
    Wscript.Echo "Caption: " & SubItems.Caption
    Wscript.Echo "CreationClassName: " & SubItems.CreationClassName
    Wscript.Echo "DataWidth: " & SubItems.DataWidth
    Wscript.Echo "Description: " & SubItems.Description
    Wscript.Echo "DeviceLocator: " & SubItems.DeviceLocator
    Wscript.Echo "FormFactor: " & SubItems.FormFactor
    Wscript.Echo "HotSwappable: " & SubItems.HotSwappable
    Wscript.Echo "InstallDate: " & SubItems.InstallDate
    Wscript.Echo "InterleaveDataDepth: " & SubItems.InterleaveDataDepth
    Wscript.Echo "InterleavePosition: " & SubItems.InterleavePosition
    Wscript.Echo "Manufacturer: " & SubItems.Manufacturer
    Wscript.Echo "MemoryType: " & SubItems.MemoryType
    Wscript.Echo "Model: " & SubItems.Model
    Wscript.Echo "Name: " & SubItems.Name
    Wscript.Echo "OtherIdentifyingInfo: " & SubItems.OtherIdentifyingInfo
    Wscript.Echo "PartNumber: " & SubItems.PartNumber
    Wscript.Echo "PositionInRow: " & SubItems.PositionInRow
    Wscript.Echo "PoweredOn: " & SubItems.PoweredOn
    Wscript.Echo "Removable: " & SubItems.Removable
    Wscript.Echo "Replaceable: " & SubItems.Replaceable
    Wscript.Echo "SerialNumber: " & SubItems.SerialNumber
    Wscript.Echo "SKU: " & SubItems.SKU
    Wscript.Echo "Speed: " & SubItems.Speed
    Wscript.Echo "Status: " & SubItems.Status
    Wscript.Echo "Tag: " & SubItems.Tag
    Wscript.Echo "TotalWidth: " & SubItems.TotalWidth
    Wscript.Echo "TypeDetail: " & SubItems.TypeDetail
    Wscript.Echo "Version: " & SubItems.Version
Wscript.Echo "=====================================0"
Next
'TextFile.Close
'OutFile.Run "notepad.exe c:\Win32_PhysicalMemory.txt",1,True
