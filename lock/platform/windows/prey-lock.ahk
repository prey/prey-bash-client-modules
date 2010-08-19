; Prey Runner Script
; By Newstart, Ttcvb32, and Tomas Pollak
; http://preyproject.com

#SingleInstance Force
#Notrayicon

RegRead, PreyPath, HKEY_LOCAL_MACHINE, SOFTWARE\Prey, Path
; RegRead, unlock_password, HKEY_LOCAL_MACHINE, SOFTWARE\Prey, Lock

if (%0% == 0) {
	InputBox, unlock_password_plain, Password, Please enter a password for Prey lock.,,300, 130
	if ErrorLevel
		exitapp
	unlock_len := StrLen(unlock_password_plain)
	unlock_password = % MD5( unlock_password_plain, unlock_len)
	}
else {
	unlock_password = %1%
}

; Run, base.exe
WinGetPos, X, Y, Width, Height, Program Manager
Height += 100	;offset size to include the header on top
w := 420	;width size of password box
X := (Width - w) // 2	;center password
Y := Height // 2
Z := Height
A := Width // 2
Q := 120

BackgroundX := (Width // 2 - 512)
BackgroundY := (Y - 480)

Gui, Color, 000000
gui, Add, Picture, x%BackgroundX% y%BackgroundY%, %PreyPath%\modules\lock\lib\bg-lock-with-input.png

; Gui, Add, Text, cBlue, Please type in the password to unlock this computer:

gui, Font, s15, Arial
gui, Add, Edit, vpass Password c333333 -E0x200 w%w% X%X% Y%Y%
gui, Font, s16, Calibri
gui, Add, Text, vBadPasswordLabel BackgroundTrans cRed hidden, Incorrect password! Access denied.

gui +AlwaysOnTop +Center
gui, Maximize
gui, show, W%Width% h%Height%, Locked

locked = 1

WinGetPos, X, Y, Width, Height, Locked

loop {
	if (!locked) {
		gui, hide
		break
	}
	sleep 50
	IfWinNotExist Locked
	{
		gui, show, center
	}
	IfWinNotActive Locked
	{
		WinActivate Locked
	}

	WinGetPos, X1, Y1, Width, Height, Locked
	if (X1 != X || Y1 != Y)
		gui, show, center
}

return

#IfWinActive Locked
NumpadEnter::
enter::
	gui, submit, NoHide	;pass will have the entered password.
	passLen := StrLen(pass)
	passMD5 = % MD5( pass, passLen )
	if (passMD5 == unlock_password)
		{
		;Process, close, base.exe
		RegDelete, HKEY_LOCAL_MACHINE, SOFTWARE\Prey, Lock
		exitapp
		}
	else {
		guicontrol, show, BadPasswordLabel
		sleep (2000)
		guicontrol, hide, BadPasswordLabel
	}
return
#IfWinActive

MD5( ByRef V, L=0 ) { ; www.autohotkey.com/forum/viewtopic.php?p=275910#275910
 VarSetCapacity( MD5_CTX,104,0 ), DllCall( "advapi32\MD5Init", Str,MD5_CTX )
 DllCall( "advapi32\MD5Update", Str,MD5_CTX, Str,V, UInt,L ? L : VarSetCapacity(V) )
 DllCall( "advapi32\MD5Final", Str,MD5_CTX )
 Loop % StrLen( Hex:="123456789ABCDEF0" )
  N := NumGet( MD5_CTX,87+A_Index,"Char"), MD5 .= SubStr(Hex,N>>4,1) . SubStr(Hex,N&15,1)
  StringLower, MD5, MD5
Return MD5
}
