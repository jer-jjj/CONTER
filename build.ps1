# =============================================================================
# CONTER 应用打包脚本 (Windows PowerShell)
# =============================================================================
# 功能：
#   1. 自动创建并激活虚拟环境
#   2. 安装所有依赖
#   3. 使用 PyInstaller 打包为 Windows 可执行文件
#
# 使用方法：
#   powershell -ExecutionPolicy Bypass -File .\build.ps1
#   powershell -ExecutionPolicy Bypass -File .\build.ps1 -Name "MyApp"
#   powershell -ExecutionPolicy Bypass -File .\build.ps1 -Clean
# =============================================================================

param(
    [string]$Name = "CONTER",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"  # 加速下载

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  CONTER 应用打包工具" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 0) 进入脚本所在目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $ScriptDir
Write-Host "[信息] 工作目录: $ScriptDir" -ForegroundColor Green

# 1) 清理构建（可选）
if ($Clean) {
    Write-Host "[清理] 删除旧的构建文件..." -ForegroundColor Yellow
    if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }
    if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }
    if (Test-Path "*.spec") { Remove-Item -Path "*.spec" -Force }
    Write-Host "[清理] 清理完成" -ForegroundColor Green
}

# 2) 检查 Python
Write-Host "[检查] 检查 Python 安装..." -ForegroundColor Yellow
try {
    $PythonVersion = & python --version 2>&1
    Write-Host "[检查] 找到 Python: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未找到 Python，请先安装 Python 3.10 或更高版本" -ForegroundColor Red
    exit 1
}

# 3) 创建/激活虚拟环境
Write-Host "[虚拟环境] 检查虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "[虚拟环境] 创建虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 创建虚拟环境失败" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[虚拟环境] 激活虚拟环境..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 激活虚拟环境失败，尝试继续..." -ForegroundColor Yellow
}

# 4) 升级 pip
Write-Host "[依赖] 升级 pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 升级 pip 失败，继续..." -ForegroundColor Yellow
}

# 5) 安装基础依赖
Write-Host "[依赖] 安装基础依赖 (flet, openpyxl, pandas)..." -ForegroundColor Yellow
python -m pip install flet openpyxl pandas --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 安装基础依赖失败" -ForegroundColor Red
    exit 1
}

# 6) 确保资源目录存在
Write-Host "[资源] 检查资源目录..." -ForegroundColor Yellow
if (-not (Test-Path "assets")) { 
    New-Item -ItemType Directory -Path "assets" | Out-Null 
    Write-Host "[资源] 创建 assets 目录" -ForegroundColor Green
}
if (-not (Test-Path "assets\fonts")) { 
    New-Item -ItemType Directory -Path "assets\fonts" | Out-Null 
    Write-Host "[资源] 创建 assets\fonts 目录" -ForegroundColor Green
}

# 7) 检查主文件
if (-not (Test-Path "main.py")) {
    Write-Host "[错误] 未找到 main.py 文件" -ForegroundColor Red
    exit 1
}

# 8) 打包
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  开始打包..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[打包] 使用 PyInstaller 打包..." -ForegroundColor Yellow

# 安装 PyInstaller
Write-Host "[打包] 安装 PyInstaller..." -ForegroundColor Yellow
python -m pip install pyinstaller --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 安装 PyInstaller 失败" -ForegroundColor Red
    exit 1
}

# 构建命令
$PackArgs = @(
    "main.py",
    "--name", $Name,
    "--add-data", "assets;assets",
    "--noconsole",
    "--onedir",
    "--noconfirm"
)

# 如果有图标文件
if (Test-Path "assets\app.ico") {
    $PackArgs += "--icon"
    $PackArgs += "assets\app.ico"
    Write-Host "[打包] 使用图标: assets\app.ico" -ForegroundColor Green
}

Write-Host "[打包] 执行 PyInstaller..." -ForegroundColor Yellow
& pyinstaller $PackArgs

# 9) 检查打包结果
Write-Host ""
if ($LASTEXITCODE -eq 0) {
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  打包成功！" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    
    if (Test-Path "dist\$Name") {
        Write-Host "[成功] 可执行文件位置: dist\$Name\" -ForegroundColor Green
        Write-Host ""
        Write-Host "可执行文件列表:" -ForegroundColor Cyan
        Get-ChildItem -Path "dist\$Name" -Filter "*.exe" | ForEach-Object {
            Write-Host "  - $($_.Name)" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "运行应用:" -ForegroundColor Cyan
        Write-Host "  cd dist\$Name" -ForegroundColor Yellow
        Write-Host "  .\$Name.exe" -ForegroundColor Yellow
    } else {
        Write-Host "[警告] 未找到 dist\$Name 目录，请检查打包日志" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "  打包失败" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "[错误] 退出码: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "[提示] 请检查上方错误信息" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "提示: 打包后的应用需要包含 assets 目录才能正常运行" -ForegroundColor Cyan
Write-Host ""