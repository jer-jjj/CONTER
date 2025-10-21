# 安装器功能实现总结

## ✅ 已实现功能

### 1. **专业安装程序**

使用 Inno Setup 创建的 Windows 安装器，具备以下功能：

#### 安装时

- ✅ **选择安装位置**：用户可自定义安装目录
- ✅ **许可协议**：显示 MIT 许可证
- ✅ **安装说明**：显示应用介绍和系统要求
- ✅ **创建桌面图标**：可选项（默认不选）
- ✅ **创建快速启动图标**：可选项（仅 Windows 7）
- ✅ **开始菜单快捷方式**：自动创建
- ✅ **包含所有资源**：应用、字体、文档
- ✅ **多语言界面**：支持中文和英文
- ✅ **现代化 UI**：使用 Modern 风格
- ✅ **自定义图标**：支持指定应用图标

#### 安装后

- ✅ **数据独立存储**：data 目录在应用目录下
- ✅ **完整开始菜单组**：
  - 应用快捷方式
  - 用户手册
  - 数据存储说明
  - 卸载程序
- ✅ **可选桌面快捷方式**
- ✅ **完整图标显示**
- ✅ **启动后运行**：可选项

#### 卸载时

- ✅ **完整卸载向导**：标准 Windows 卸载流程
- ✅ **数据保留选项**：询问是否删除用户数据
- ✅ **智能清理**：
  - 保留数据：仅删除程序文件
  - 删除数据：清理所有内容
- ✅ **友好提示**：告知数据保存位置
- ✅ **注册表清理**：自动清理安装信息

### 2. **一键构建脚本**

`build_installer.ps1` 支持：

- ✅ **自动化流程**：从打包到安装器一键完成
- ✅ **自定义图标**：`-IconPath` 参数
- ✅ **默认图标支持**：无图标时使用默认
- ✅ **清理功能**：`-Clean` 清理旧构建
- ✅ **分步构建**：
  - `-SkipInstaller`：仅打包
  - `-SkipBuild`：仅生成安装器
- ✅ **错误处理**：完整的错误检查和提示
- ✅ **彩色输出**：友好的终端提示
- ✅ **进度显示**：每步都有清晰说明

### 3. **完整文档体系**

| 文档                  | 说明                       |
| --------------------- | -------------------------- |
| `INSTALLER_GUIDE.md`  | 安装器完整指南（7000+ 字） |
| `ICON_GUIDE.md`       | 图标准备指南               |
| `README.txt`          | 安装器显示的说明           |
| `LICENSE.txt`         | MIT 许可证                 |
| `QUICKSTART_BUILD.md` | 快速开始（已更新）         |

## 📁 项目结构

```
CONTER/
├── build_installer.ps1      # 完整构建脚本（新）
├── build.ps1                # 简单打包脚本
├── installer.iss            # Inno Setup 配置（新）
├── README.txt               # 安装说明（新）
├── LICENSE.txt              # 许可证（新）
├── INSTALLER_GUIDE.md       # 安装器指南（新）
├── ICON_GUIDE.md            # 图标指南（新）
├── assets/
│   ├── app.ico             # 应用图标（需准备）
│   └── fonts/              # 字体文件
├── dist/
│   └── CONTER/             # 打包输出
└── installer_output/       # 安装器输出（新）
    └── CONTER_Setup_2.0.0.exe
```

## 🚀 使用流程

### 完整构建流程

```powershell
# 1. 准备图标（可选）
# 将 app.ico 放入 assets 目录

# 2. 运行构建脚本
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1

# 3. 等待完成
# - 打包应用：约 2-3 分钟
# - 生成安装器：约 30 秒

# 4. 获取安装器
# installer_output\CONTER_Setup_2.0.0.exe
```

### 分发给用户

用户运行 `CONTER_Setup_2.0.0.exe`：

1. 选择语言（中文/English）
2. 阅读许可协议
3. 选择安装位置
4. 选择是否创建桌面图标
5. 等待安装完成
6. 启动应用

### 用户卸载

通过"添加或删除程序"卸载：

1. 运行卸载程序
2. 选择是否保留数据
3. 完成卸载

## 🎯 关键特性

### 数据管理

**安装时**：

- 数据目录：`安装路径\data\`
- 自动创建空 data.json

**使用时**：

- 所有数据存储在 data 目录
- 便携、可备份

**卸载时**：

- 询问用户是否删除数据
- 保留数据则提示位置
- 删除数据则完全清理

### 图标支持

**默认行为**：

- 查找 `assets\app.ico`
- 找不到使用 Windows 默认图标
- 不影响功能

**自定义图标**：

```powershell
# 指定图标路径
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -IconPath "my_icon.ico"
```

**图标要求**：

- 格式：ICO
- 尺寸：建议包含 16, 32, 48, 256
- 创建工具：见 ICON_GUIDE.md

### 多语言支持

**安装器**：

- 中文（简体）
- English

**应用**：

- 中文（简体）
- English
- Français

## 📊 输出文件

### 便携版（仅打包）

```
dist\CONTER\
├── CONTER.exe          # 主程序（~50MB）
├── assets\             # 资源文件
│   └── fonts\          # 字体
├── data\               # 数据目录（自动创建）
└── [依赖库...]         # Python 库
```

大小：约 100-150 MB

### 安装器

```
installer_output\
└── CONTER_Setup_2.0.0.exe  # 安装程序（~30-50MB）
```

压缩率：约 60-70%

## 🔧 高级配置

### 修改安装器设置

编辑 `installer.iss`：

```inno
; 应用信息
#define MyAppVersion "2.0.0"

; 安装选项
DefaultDirName={autopf}\{#MyAppName}
PrivilegesRequired=lowest

; 文件包含
[Files]
Source: "dist\CONTER\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
```

### 添加更多快捷方式

```inno
[Icons]
Name: "{group}\新快捷方式"; Filename: "{app}\myfile.exe"
```

### 自定义卸载逻辑

编辑 `[Code]` 部分的 `CurUninstallStepChanged` 函数。

## ✨ 对比旧方案

| 特性         | 旧方案（build.ps1） | 新方案（build_installer.ps1） |
| ------------ | ------------------- | ----------------------------- |
| 打包应用     | ✅                  | ✅                            |
| 生成安装器   | ❌                  | ✅                            |
| 选择安装位置 | ❌                  | ✅                            |
| 创建桌面图标 | ❌                  | ✅                            |
| 卸载程序     | ❌                  | ✅                            |
| 数据管理     | ❌                  | ✅                            |
| 自定义图标   | ✅                  | ✅                            |
| 多语言界面   | ❌                  | ✅                            |
| 开始菜单     | ❌                  | ✅                            |

## 🎓 学习资源

- **Inno Setup 官方文档**：https://jrsoftware.org/ishelp/
- **示例脚本**：Inno Setup 安装目录的 Examples 文件夹
- **本项目文档**：
  - [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) - 详细指南
  - [ICON_GUIDE.md](ICON_GUIDE.md) - 图标制作
  - [BUILD.md](BUILD.md) - 基础打包
  - [DATA_STORAGE.md](DATA_STORAGE.md) - 数据存储

## 🆘 故障排除

### 问题 1：找不到 Inno Setup

**解决**：

1. 下载：https://jrsoftware.org/isdl.php
2. 安装到默认路径
3. 重新运行脚本

### 问题 2：图标不显示

**解决**：

1. 检查图标格式（必须是 ICO）
2. 检查图标路径（默认 assets\app.ico）
3. 使用 `-Clean` 重新构建

### 问题 3：安装器生成失败

**解决**：

1. 检查 `dist\CONTER\` 目录是否存在
2. 检查 `installer.iss` 语法
3. 查看 Inno Setup 编译器输出

### 问题 4：卸载后数据未保留

**检查**：

- 卸载时选择"否"（不删除数据）
- 数据位置：安装目录的 data 子目录

## 🎉 总结

现在您拥有：

- ✅ 专业的 Windows 安装程序
- ✅ 用户友好的安装/卸载体验
- ✅ 完整的图标支持
- ✅ 灵活的数据管理
- ✅ 一键构建流程
- ✅ 完整的文档体系

开始构建您的安装器吧！

```powershell
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1
```

---

**需要帮助？** 查看 [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) 获取详细说明。
