[Setup]
AppName=Análise de Vendas
AppVersion=1.0
DefaultDirName={pf}\AnaliseVendas
DefaultGroupName=Análise de Vendas
OutputDir=dist
OutputBaseFilename=Instalador_AnaliseVendas
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\maicon\Desktop\analise_vendas\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\maicon\Desktop\analise_vendas\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Análise de Vendas"; Filename: "{app}\main.exe"
Name: "{group}\Desinstalar Análise de Vendas"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\main.exe"; Description: "Executar Análise de Vendas"; Flags: nowait postinstall skipifsilent
