# 构建与发布指南

本项目支持将 Flet 应用打包为可执行文件（Windows）。推荐使用 `flet pack`（底层使用 PyInstaller）。

## 1. 准备工作

- 已安装 Python 3.10+（项目使用 3.13 也可）
- 已创建虚拟环境并安装依赖：`flet openpyxl pandas`
- 将字体文件放入 `assets/fonts/`（例如 `MiSans-Regular.ttf`）

## 2. 本地运行（验证字体与功能）

```powershell
# 启动（确保使用虚拟环境）
.venv\Scripts\python.exe main.py
```

## 3. 安装打包工具

```powershell
# 安装 flet 的打包子命令
.venv\Scripts\python.exe -m pip install flet[all]
```

> 若公司网络限制，请预先配置 pip 源或离线安装。

## 4. 打包为 EXE（推荐）

```powershell
# 方式一：使用 flet pack（自动处理 PyInstaller 细节）
.venv\Scripts\python.exe -m flet pack main.py `
  --name "CONTER" `
  --icon assets/app.ico `
  --add-data "assets;assets" `
  --windowed
```

说明：

- `--add-data "assets;assets"` 会把 `assets` 目录一起打进包里（字体、图标等资源）
- `--windowed` 表示不弹出控制台窗口
- `--icon` 可选，若无图标可移除该参数

> 如果遇到中文路径或空格问题，可将项目移动到无空格、无中文路径下。

## 5. 使用 PyInstaller（可选）

```powershell
.venv\Scripts\python.exe -m pip install pyinstaller
.venv\Scripts\pyinstaller.exe main.py `
  --name CONTER `
  --noconsole `
  --add-data "assets;assets" `
  --icon assets/app.ico
```

生成的可执行文件在 `dist/CONTER/` 下。

## 6. 常见问题

- 字体不生效：
  - 确认字体文件已放在 `assets/fonts/MiSans-Regular.ttf`
  - `main.py` 中 `page.fonts = {"MiSans": "fonts/MiSans-Regular.ttf"}`，且启动 `ft.app(..., assets_dir="assets")`
  - 打包时记得 `--add-data "assets;assets"`
- 资源未打入包：
  - 检查 `--add-data` 的分隔符在 Windows 下是 `;`（形如 `源;目标`）
- 启动白屏：
  - 尝试升级 flet 到最新稳定版
  - 删除 `.venv` 重新安装依赖

## 7. 一键脚本（Windows PowerShell）

项目已包含自动化打包脚本 `build.ps1`，具有以下功能：

- ✅ 自动创建和激活虚拟环境
- ✅ 自动安装所有依赖
- ✅ 自动检查 Python 和资源文件
- ✅ 支持两种打包方式（flet pack / PyInstaller）
- ✅ 彩色输出和详细进度提示
- ✅ 自动清理旧构建（可选）
- ✅ 错误处理和友好提示

### 使用方法

```powershell
# 方式一：使用 flet pack（推荐，默认）
powershell -ExecutionPolicy Bypass -File .\build.ps1

# 方式二：使用 PyInstaller
powershell -ExecutionPolicy Bypass -File .\build.ps1 -UsePyInstaller

# 方式三：自定义应用名称
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Name "MyNamePicker"

# 方式四：先清理再打包
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Clean

# 组合参数
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Name "CONTER" -UsePyInstaller -Clean
```

### 脚本参数说明

| 参数              | 类型   | 默认值   | 说明                            |
| ----------------- | ------ | -------- | ------------------------------- |
| `-Name`           | String | "CONTER" | 生成的可执行文件名称            |
| `-UsePyInstaller` | Switch | False    | 使用 PyInstaller 而非 flet pack |
| `-Clean`          | Switch | False    | 打包前清理旧的构建文件          |

### 打包流程

脚本会自动执行以下步骤：

1. 检查 Python 安装
2. 创建/激活虚拟环境
3. 升级 pip
4. 安装依赖（flet、openpyxl、pandas）
5. 检查资源目录（自动创建如不存在）
6. 安装打包工具（flet[all] 或 pyinstaller）
7. 执行打包命令
8. 显示打包结果和可执行文件位置

### 输出位置

打包完成后，可执行文件在：

```
dist/
└── CONTER/
    ├── CONTER.exe          # 主程序
    ├── assets/             # 资源文件（字体、图标）
    └── [其他依赖文件]
```

### 运行打包后的应用

```powershell
cd dist\CONTER
.\CONTER.exe
```

### 脚本特性

- **彩色输出**：不同类型的消息用不同颜色标识
  - 🔵 信息 - 青色
  - 🟢 成功 - 绿色
  - 🟡 警告 - 黄色
  - 🔴 错误 - 红色
- **错误处理**：自动检测并提示错误原因

- **进度提示**：每一步都有清晰的提示信息

- **资源检查**：自动检测图标文件并应用
