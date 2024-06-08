# Name des Installers
Outfile "GitManagerInstaller.exe"

# Installationsverzeichnis
InstallDir $PROGRAMFILES\GitManager

# Symbol für den Installer
Icon "icon.ico"

# MUI2 einbinden
!include "MUI2.nsh"

# Standard-Headerbilder von MUI2 verwenden, anstatt spezifische Bilddateien zu benötigen
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT

# Seiten
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Uninstall
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Sprachen
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath $INSTDIR
  File /r "dist\GitManager\*.*"
  CreateShortcut "$DESKTOP\GitManager.lnk" "$INSTDIR\GitManager.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\*.*"
  RMDir "$INSTDIR"
  Delete "$DESKTOP\GitManager.lnk"
SectionEnd
