# 安装器构建指南

本项目支持生成专业的 Windows 安装程序，用户可以选择安装位置、创建桌面图标，并附带卸载器。

## 📋 前置要求

### 1. 安装 Inno Setup

下载并安装 Inno Setup 6.0 或更高版本：

- 官网：https://jrsoftware.org/isinfo.php
- 下载：https://jrsoftware.org/isdl.php

选择 "Inno Setup 6.x.x" 标准版本即可。

### 2. 准备图标文件（可选）

将应用图标放置在：

```
assets\app.ico
```

图标规格：

- 格式：ICO 格式
- 建议尺寸：包含 16x16, 32x32, 48x48, 256x256
- 工具：可使用在线转换工具或 IcoFX

如果没有图标，脚本会使用 Windows 默认图标。

## 🚀 快速开始

### 方式一：一键构建（推荐）

```powershell
# 完整构建：打包 + 生成安装器
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1
```

### 方式二：分步构建

```powershell
# 1. 仅打包应用（不生成安装器）
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -SkipInstaller

# 2. 使用已有的 dist 目录生成安装器
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -SkipBuild
```

### 方式三：自定义图标

```powershell
# 指定自定义图标路径
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -IconPath "my_custom_icon.ico"
```

### 方式四：清理后重新构建

```powershell
# 清理旧文件并重新构建
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -Clean
```

## 📦 输出文件

构建完成后，会生成：

```
项目目录/
├── dist/
│   └── CONTER/              # 可执行文件目录
│       ├── CONTER.exe       # 主程序
│       ├── assets/          # 资源文件（含字体）
│       └── [依赖库...]
│
└── installer_output/
    └── CONTER_Setup_2.0.0.exe  # 安装程序
```

## 🎯 安装器功能

生成的安装程序具有以下功能：

### 安装时

- ✅ 允许用户选择安装位置
- ✅ 显示许可协议（LICENSE.txt）
- ✅ 显示安装说明（README.txt）
- ✅ 可选创建桌面图标
- ✅ 可选创建快速启动图标
- ✅ 自动创建开始菜单快捷方式
- ✅ 包含所有必需文件（应用、字体、资源）
- ✅ 支持中文和英文界面
- ✅ 现代化向导界面

### 安装后

- ✅ 数据存储在应用目录的 data 子目录
- ✅ 开始菜单包含：应用快捷方式、用户手册、卸载程序
- ✅ 可选的桌面快捷方式
- ✅ 应用图标显示正确

### 卸载时

- ✅ 完整的卸载向导
- ✅ 询问是否保留用户数据
- ✅ 清理所有安装文件
- ✅ 清理开始菜单和桌面图标
- ✅ 如果保留数据，提示数据位置

## ⚙️ 自定义配置

### 修改应用信息

编辑 `installer.iss` 文件开头部分：

```inno
#define MyAppName "CONTER 点名器"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "CONTER Team"
#define MyAppURL "https://github.com/jer-jjj/CONTER"
```

### 修改默认安装路径

```inno
DefaultDirName={autopf}\{#MyAppName}  ; Program Files
; 或
DefaultDirName={localappdata}\{#MyAppName}  ; AppData\Local
```

### 添加更多文件

在 `[Files]` 部分添加：

```inno
Source: "myfile.txt"; DestDir: "{app}"; Flags: ignoreversion
```

### 修改图标位置

在 `[Setup]` 部分：

```inno
SetupIconFile=path\to\your\icon.ico
```

## 🔧 高级选项

### 参数说明

| 参数             | 类型   | 说明                                 |
| ---------------- | ------ | ------------------------------------ |
| `-Name`          | String | 应用名称（默认：CONTER）             |
| `-IconPath`      | String | 图标文件路径（默认：assets\app.ico） |
| `-Clean`         | Switch | 清理旧构建文件                       |
| `-SkipInstaller` | Switch | 仅打包，不生成安装器                 |
| `-SkipBuild`     | Switch | 仅生成安装器，不打包                 |

### 使用示例

```powershell
# 示例1：完整构建并清理
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -Clean

# 示例2：使用自定义图标
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -IconPath "D:\icons\myapp.ico"

# 示例3：仅打包便携版
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -SkipInstaller

# 示例4：快速重新生成安装器（已有 dist 目录）
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -SkipBuild
```

## 📝 构建流程

完整构建流程：

```
1. 检查 Python 环境
   ↓
2. 激活虚拟环境
   ↓
3. 安装依赖（flet、pandas、openpyxl、pyinstaller）
   ↓
4. 检查资源文件（字体、图标）
   ↓
5. 使用 PyInstaller 打包
   ├─ 包含所有 Python 依赖
   ├─ 包含 assets 资源
   └─ 应用自定义图标
   ↓
6. 生成 dist/CONTER/ 目录
   ↓
7. 检查 Inno Setup
   ↓
8. 编译 installer.iss
   ├─ 创建安装向导
   ├─ 配置卸载程序
   └─ 打包所有文件
   ↓
9. 生成安装程序
   ↓
10. 输出到 installer_output/
```

## 🐛 常见问题

### Q1: 提示"未找到 Inno Setup"

**A:**

1. 下载并安装：https://jrsoftware.org/isdl.php
2. 默认安装路径：`C:\Program Files (x86)\Inno Setup 6\`
3. 重新运行构建脚本

### Q2: 图标不显示

**A:**

1. 确认图标格式为 ICO
2. 图标路径正确
3. 重新打包：`-Clean` 参数

### Q3: 安装器语言是英文

**A:**
在安装向导第一页选择 "中文（简体）"

### Q4: 如何创建 ICO 图标

**A:**

- 在线工具：https://www.icoconverter.com/
- 桌面工具：IcoFX、GIMP
- 从 PNG 转换：推荐 256x256 PNG

### Q5: 想要便携版（无需安装）

**A:**

```powershell
# 使用 SkipInstaller 参数
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -SkipInstaller

# 输出在 dist\CONTER\ 目录
# 直接复制该目录即可
```

### Q6: 修改安装器外观

**A:**
编辑 `installer.iss`：

```inno
WizardStyle=modern           ; 现代风格
WizardImageFile=myimage.bmp  ; 侧边栏图片
WizardSmallImageFile=mysmall.bmp  ; 顶部小图
```

## 📊 文件大小参考

- 可执行文件：约 50-80 MB
- 安装程序：约 30-50 MB（压缩后）
- 安装后占用：约 100-150 MB

## 🔐 代码签名（可选）

对于正式发布，建议进行代码签名：

1. 获取代码签名证书
2. 在 `installer.iss` 添加：

```inno
[Setup]
SignTool=signtool
SignedUninstaller=yes
```

3. 配置 signtool 路径

## 📚 相关文档

- Inno Setup 文档：https://jrsoftware.org/ishelp/
- PyInstaller 文档：https://pyinstaller.org/
- 本项目文档：
  - [BUILD.md](BUILD.md) - 基础打包
  - [DATA_STORAGE.md](DATA_STORAGE.md) - 数据存储
  - [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南

---

**准备就绪！** 运行构建脚本开始创建安装器。

如有问题，请查看构建日志或提交 Issue。
