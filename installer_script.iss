; ============================================================
;  INSTALLER SCRIPT - Trascrizione Audio/Video
;  Software Professionale creato dall’Ing. Francesco Barbato
; ============================================================

#define MyAppName "Trascrizione Audio/Video"
#define MyAppVersion "1.0"
#define MyAppPublisher "Ing. Francesco Barbato"
#define MyAppExeName "main.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-G7H8-I9J0-K1L2M3N4O5P6}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\TrascrizioneAudioVideo
DefaultGroupName=Trascrizione Audio/Video
OutputDir=output
OutputBaseFilename=Setup_TrascrizioneAudioVideo
SetupIconFile=icona\icona.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ShowLanguageDialog=no
UninstallDisplayIcon={app}\icona.ico
ArchitecturesInstallIn64BitMode=x64compatible


; 🔹 Immagini personalizzate (usa splash.bmp nella cartella icona)
WizardImageFile=icona\splash.bmp
WizardSmallImageFile=icona\splash.bmp

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

; 🔹 Testi personalizzati nelle finestre
[Messages]
WelcomeLabel1=Benvenuto nel programma di installazione di {#MyAppName}
WelcomeLabel2=Questo software professionale è sviluppato e distribuito dall’Ing. Francesco Barbato.\n\nPremi Avanti per continuare l’installazione.
FinishedLabel=Installazione completata con successo!
FinishedHeadingLabel=Grazie per aver scelto il software professionale dell’Ing. Francesco Barbato
FinishedRestartLabel=È possibile avviare il programma immediatamente selezionando la casella qui sotto.

[Tasks]
Name: "desktopicon"; Description: "Crea icona sul desktop"; GroupDescription: "Icone:"

[Files]
; 🔸 File principale generato da PyInstaller
Source: "dist\TrascrizioneAudioVideo.exe"; DestDir: "{app}"; DestName: "{#MyAppExeName}"; Flags: ignoreversion
; 🔸 Cartella icone (inclusa icona.ico e splash.bmp)
Source: "icona\*"; DestDir: "{app}\icona"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Trascrizione Audio/Video"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icona\icona.ico"
Name: "{autodesktop}\Trascrizione Audio/Video"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icona\icona.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Avvia {#MyAppName}"; Flags: nowait postinstall skipifsilent shellexec unchecked

