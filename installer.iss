; Inno Setup 脚本 - CONTER 点名器安装程序
; 需要安装 Inno Setup 6.0 或更高版本: https://jrsoftware.org/isinfo.php

#define MyAppName "CONTER 点名器"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "CONTER Team"
#define MyAppURL "https://github.com/jer-jjj/CONTER"
#define MyAppExeName "CONTER.exe"
#define MyAppId "{{8F6A9B2C-4D3E-4F5A-9B7C-1E2D3F4A5B6C}"

[Setup]
; 基本信息
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; 默认安装目录
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; 允许用户选择安装路径
DisableProgramGroupPage=no
AllowNoIcons=yes

; 输出设置
OutputDir=installer_output
OutputBaseFilename=CONTER_Setup_{#MyAppVersion}

; 检查图标文件是否存在，如果存在则使用
#ifexist "assets\app.ico"
SetupIconFile=assets\app.ico
#endif

; 压缩设置
Compression=lzma2/max
SolidCompression=yes

; 权限设置
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 界面设置
WizardStyle=modern
DisableWelcomePage=no
LicenseFile=LICENSE.txt
InfoBeforeFile=README.txt

; 卸载设置
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; 系统要求
MinVersion=6.1sp1

[Languages]
#ifdef UseZh
#ifexist "compiler:Languages\ChineseSimplified.isl"
#define HasZh
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
#endif
#endif
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 主程序和依赖文件
Source: "dist\CONTER\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 文档文件
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "DATA_STORAGE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 开始菜单图标
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{group}\用户手册"; Filename: "{app}\USER_GUIDE.md"
Name: "{group}\数据存储说明"; Filename: "{app}\DATA_STORAGE.md"
; 桌面图标（可选）
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
; 快速启动图标（可选）
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; 安装完成后选项
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 卸载时删除用户数据（可选，默认保留）
; Type: filesandordirs; Name: "{app}\data"

[Code]
var
  DataDirPage: TInputDirWizardPage;
  KeepDataCheckBox: TNewCheckBox;

procedure InitializeWizard;
begin
  // 创建自定义页面 - 询问是否保留数据
  DataDirPage := CreateInputDirPage(wpSelectDir,
    '数据目录设置', '选择数据存储位置',
    '应用数据将存储在应用安装目录下的 data 子目录中。' + #13#10 +
    '您也可以在安装后手动移动数据文件。',
    False, 'data');
  DataDirPage.Add('');
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  // 跳过数据目录页面，因为数据总是存储在应用目录
  Result := PageID = DataDirPage.ID;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
  DataPath: String;
begin
  if CurUninstallStep = usUninstall then
  begin
    DataPath := ExpandConstant('{app}\data');
    
    if DirExists(DataPath) then
    begin
      if MsgBox('是否删除用户数据？' + #13#10 + #13#10 +
                '选择"是"将删除所有学生名单和抽取记录。' + #13#10 +
                '选择"否"将保留数据以便将来使用。', 
                mbConfirmation, MB_YESNO) = IDYES then
      begin
        DelTree(DataPath, True, True, True);
      end
      else
      begin
        MsgBox('用户数据已保留在：' + #13#10 + DataPath + #13#10 + #13#10 +
               '您可以在重新安装后继续使用这些数据。', 
               mbInformation, MB_OK);
      end;
    end;
  end;
end;

[Messages]
; 自定义消息（仅当中文语言可用时注入）
#ifdef HasZh
chinesesimplified.WelcomeLabel2=这将在您的计算机上安装 [name/ver]。%n%n推荐在继续之前关闭所有其他应用程序。%n%n点击"下一步"继续，或点击"取消"退出安装程序。
chinesesimplified.FinishedLabel=安装完成！%n%n[name] 已成功安装到您的计算机。%n%n应用数据将存储在安装目录的 data 子目录中。
#endif

