; Prey Lock Script
; By Newstart, Ttcvb32, Tomas Pollak and Carlos Yaconi
; http://preyproject.com

#SingleInstance Force
#Notrayicon

;Works only on XP. Vista and 7 need administrator rights
;-----------------------------
RegWrite,REG_DWORD,HKEY_LOCAL_MACHINE,SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System,HideFastUserSwitching,1
RegWrite,REG_DWORD,HKEY_CURRENT_USER,SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System,DisableChangePassword,1
DllCall("WinLockDll.dll\CtrlAltDel_Enable_Disable",UInt,0)
DllCall("WinLockDll.dll\TaskManager_Enable_Disable",UInt,0)
;-----------------------------
DllCall("WinLockDll.dll\TaskSwitching_Enable_Disable",UInt,0)

RegRead, PreyPath, HKEY_LOCAL_MACHINE, SOFTWARE\Prey, Path

if (%0% == 0) {
	InputBox, unlock_password_plain, Password, Please enter a password for Prey lock.,,300, 130
	if ErrorLevel
		exitapp, 1
	unlock_len := StrLen(unlock_password_plain)
	unlock_password = % MD5( unlock_password_plain, unlock_len)
	}
else {
	unlock_password = %1%
}

;Grab extended desktop information
SysGet, VirtualX, 76
SysGet, VirtualY, 77
SysGet, VirtualWidth, 78
SysGet, VirtualHeight, 79

;Create a black always on top overlay to cover applications
Gui, 2:Color, Black
Gui, 2:Maximize
Gui, 2:-Caption
Gui 2:+AlwaysOnTop
Gui, 2:Show, x%VirtualX% y%VirtualY% w%VirtualWidth%  h%VirtualHeight%

WinGetPos, X, Y, Width, Height, Program Manager
w := 420	;width size of password box
X := (Width - w) // 2	;center password
Y := Height // 2
Z := Height
A := Width // 2
Q := 120

BackgroundX := (Width // 2 - 512)
BackgroundY := (Y - 480)

Gui, Color, 000000
Gui, Add, Picture, x%BackgroundX% y%BackgroundY%, %PreyPath%\modules\lock\lib\bg-lock-with-input.png

Gui, Font, s15, Arial
Gui, Add, Edit, vpass Password c333333 -E0x200 w%w% X%X% Y%Y%
Gui, Font, s16, Calibri
Gui, Add, Text, vBadPasswordLabel BackgroundTrans cRed hidden, Incorrect password! Access denied.

Gui +AlwaysOnTop +Center
Gui, Maximize
Gui, -Caption
Gui, show, W%Width% h%Height%, Locked

locked = 1
SetTimer, CloseTaskmgr, 600 ;Check every 600ms if Task Manager is opened
SetTimer, AlwaysTop, 100 ;Every 100ms puts password screen on top.
WinGetPos, X, Y, Width, Height, Locked

loop {
	if (!locked) {
		Gui, hide
		break
	}
	sleep 50
	IfWinNotExist Locked
	{
		Gui, show, center
	}
	IfWinNotActive Locked
	{
		WinActivate Locked
	}

	WinGetPos, X1, Y1, Width, Height, Locked
	if (X1 != X || Y1 != Y)
		Gui, show, center
}

return

#IfWinActive Locked

NumpadEnter::
enter::
	Gui, submit, NoHide	;pass will have the entered password.
	passLen := StrLen(pass)
	passMD5 = % MD5( pass, passLen )
	if (passMD5 == unlock_password)
		{
		;Process, close, base.exe
		RegDelete, HKEY_LOCAL_MACHINE, SOFTWARE\Prey, Lock
		RegWrite,REG_DWORD,HKEY_LOCAL_MACHINE,SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System,HideFastUserSwitching,0
		RegWrite,REG_DWORD,HKEY_CURRENT_USER,SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System,DisableChangePassword,0
		DllCall("WinLockDll.dll\CtrlAltDel_Enable_Disable",UInt,1)
		DllCall("WinLockDll.dll\TaskSwitching_Enable_Disable",UInt,1)
		DllCall("WinLockDll.dll\TaskManager_Enable_Disable",UInt,1)
		exitapp, 66
		}
	else {
		guicontrol, show, BadPasswordLabel
		sleep (2000)
		guicontrol, hide, BadPasswordLabel
	}
return

#IfWinActive

CloseTaskmgr:
 SetTimer, CloseTaskmgr, off
 Process, Wait, taskmgr.exe, 4
 Process, Close, taskmgr.exe
 SetTimer, CloseTaskmgr, on
return

AlwaysTop:
	SetTimer, AlwaysTop, off
	Gui +AlwaysOnTop +Center
	SetTimer, AlwaysTop, on
return

MD5( ByRef V, L=0 ) { ; www.autohotkey.com/forum/viewtopic.php?p=275910#275910
 VarSetCapacity( MD5_CTX,104,0 ), DllCall( "advapi32\MD5Init", Str,MD5_CTX )
 DllCall( "advapi32\MD5Update", Str,MD5_CTX, Str,V, UInt,L ? L : VarSetCapacity(V) )
 DllCall( "advapi32\MD5Final", Str,MD5_CTX )
 Loop % StrLen( Hex:="123456789ABCDEF0" )
  N := NumGet( MD5_CTX,87+A_Index,"Char"), MD5 .= SubStr(Hex,N>>4,1) . SubStr(Hex,N&15,1)
  StringLower, MD5, MD5
Return MD5
}
