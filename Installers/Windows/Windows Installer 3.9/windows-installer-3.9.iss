[Setup]
AppName=Calculator
AppVersion=1.0.8
AppPublisher=Rdiffurissu
DefaultDirName={autopf}\Calculator
DefaultGroupName=Calculator
AllowNoIcons=no
OutputDir=Output
OutputBaseFilename=Calculator-Windows-3.9-Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "dist\calculator-Windows-3.9.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Calculator"; Filename: "{app}\calculator-Windows-3.9.exe"
Name: "{commondesktop}\Calculator"; Filename: "{app}\calculator-Windows-3.9.exe"
Name: "{group}\Uninstall Calculator"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\calculator-Windows-3.9.exe"; Description: "Launch Calculator"; Flags: nowait postinstall skipifsilent
