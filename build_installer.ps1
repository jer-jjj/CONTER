# =============================================================================
# CONTER 应用完整构建脚本 (Windows PowerShell)
# =============================================================================
# 功能：
#   1. 打包应用为可执行文件
#   2. 生成安装程序（可选）
#   3. 支持自定义图标
#   4. 包含所有资源文件
#
# 使用方法：
#   powershell -ExecutionPolicy Bypass -File .\build_installer.ps1
#   powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -IconPath "my_icon.ico"
#   powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -SkipInstaller
# =============================================================================

param(
    [string]$Name = "CONTER",
    [string]$IconPath = "assets\app.ico",
    [switch]$Clean,
    [switch]$SkipInstaller,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"


# 校验 ICO 是否有效（检查 ICO 头/数量/偏移/长度）
function Test-ValidIco {
    param([string]$Path)
    try {
        if (-not (Test-Path $Path)) { return $false }
        $bytes = [System.IO.File]::ReadAllBytes($Path)
        if ($bytes.Length -lt 22) { return $false }
        $ms = New-Object System.IO.MemoryStream($bytes)
        $br = New-Object System.IO.BinaryReader($ms)
        $reserved = $br.ReadUInt16()
        $type = $br.ReadUInt16()
        $count = $br.ReadUInt16()
        if ($reserved -ne 0 -or $type -ne 1 -or $count -lt 1) { $br.Close(); $ms.Close(); return $false }
        for ($i=0; $i -lt $count; $i++) {
            [void]$br.ReadByte()   # width
            [void]$br.ReadByte()   # height
            [void]$br.ReadByte()   # colorCount
            [void]$br.ReadByte()   # reserved
            [void]$br.ReadUInt16() # planes
            [void]$br.ReadUInt16() # bitCount
            $bytesInRes = $br.ReadUInt32()
            $imageOffset = $br.ReadUInt32()
            if ($imageOffset -lt 0 -or $bytesInRes -lt 1) { $br.Close(); $ms.Close(); return $false }
            if (($imageOffset + $bytesInRes) -gt $bytes.Length) { $br.Close(); $ms.Close(); return $false }
        }
        $br.Close(); $ms.Close();
        return $true
    } catch { return $false }
}



Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  CONTER 应用完整构建工具" -ForegroundColor Cyan
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
    if (Test-Path "installer_output") { Remove-Item -Path "installer_output" -Recurse -Force }
    if (Test-Path "*.spec") { Remove-Item -Path "*.spec" -Force }
    Write-Host "[清理] 清理完成" -ForegroundColor Green
}

# 2) 检查 Python
if (-not $SkipBuild) {
    Write-Host "[检查] 检查 Python 安装..." -ForegroundColor Yellow
    try {
        $PythonVersion = & python --version 2>&1
        Write-Host "[检查] 找到 Python: $PythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "[错误] 未找到 Python" -ForegroundColor Red
        exit 1
    }

    # 3) 虚拟环境
    Write-Host "[虚拟环境] 检查虚拟环境..." -ForegroundColor Yellow
    if (-not (Test-Path ".venv")) {
        Write-Host "[虚拟环境] 创建虚拟环境..." -ForegroundColor Yellow
        python -m venv .venv
    }
    & .\.venv\Scripts\Activate.ps1

    # 3.5) 清理旧的 .spec 和 build 目录（PyInstaller 工作目录）
    Write-Host "[清理] 清理旧的 PyInstaller 文件..." -ForegroundColor Yellow
    if (Test-Path "CONTER.spec") { Remove-Item -Path "CONTER.spec" -Force }
    if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }

    # 4) 安装依赖
    Write-Host "[依赖] 升级 pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip --quiet
    
    Write-Host "[依赖] 安装基础依赖..." -ForegroundColor Yellow
    python -m pip install flet openpyxl pandas --quiet
    
    Write-Host "[依赖] 安装 PyInstaller..." -ForegroundColor Yellow
    python -m pip install pyinstaller --quiet

    # 5) 检查资源
    Write-Host "[资源] 检查资源文件..." -ForegroundColor Yellow
    if (-not (Test-Path "assets")) {
        New-Item -ItemType Directory -Path "assets" | Out-Null
    }
    if (-not (Test-Path "assets\fonts")) {
        New-Item -ItemType Directory -Path "assets\fonts" | Out-Null
    }

    # 6) 检查图标（仅在有效时启用）
    $UseIcon = $false
    if ((Test-Path $IconPath) -and ($IconPath -ne "assets\app.ico")) {
        if (Test-ValidIco -Path $IconPath) {
            Write-Host "[图标] 使用自定义图标: $IconPath" -ForegroundColor Green
            Copy-Item $IconPath "assets\app.ico" -Force
            $UseIcon = $true
        } else {
            Write-Host "[图标] 提供的图标无效，已忽略: $IconPath" -ForegroundColor Yellow
        }
    } elseif (Test-Path "assets\app.ico") {
        if (Test-ValidIco -Path "assets\app.ico") {
            Write-Host "[图标] 使用现有图标: assets\app.ico" -ForegroundColor Green
            $UseIcon = $true
        } else {
            Write-Host "[图标] 发现无效图标 assets\\app.ico，已删除以避免打包失败" -ForegroundColor Yellow
            Remove-Item -Path "assets\app.ico" -Force -ErrorAction SilentlyContinue
            $UseIcon = $false
        }
    } else {
        Write-Host "[图标] 未找到图标文件，将使用默认图标" -ForegroundColor Yellow
        Write-Host "[提示] 您可以准备一个 app.ico 文件到 assets 目录以使用自定义图标" -ForegroundColor Gray
    }

    # 7) 打包
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  开始打包应用..." -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""

    # 清理旧的输出目录
    if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }
    if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }
    if (Test-Path "CONTER.spec") { Remove-Item -Path "CONTER.spec" -Force }

    $PackArgs = @(
        "main.py",
        "--name", $Name,
        "--add-data", "assets;assets",
        "--noconsole",
        "--onedir",
        "--noconfirm",
        "--clean"
    )

    if ($UseIcon -and (Test-ValidIco -Path "assets\app.ico")) {
        Write-Host "[图标] PyInstaller 将使用: assets\app.ico" -ForegroundColor Green
        $PackArgs += "--icon"
        $PackArgs += "assets\app.ico"
    } else {
        Write-Host "[图标] 未指定或图标无效，PyInstaller 将使用默认图标" -ForegroundColor Yellow
    }

    Write-Host "[打包] 执行 PyInstaller..." -ForegroundColor Yellow
    & pyinstaller $PackArgs

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Red
        Write-Host "  打包失败" -ForegroundColor Red
        Write-Host "================================================" -ForegroundColor Red
        exit 1
    }

    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  打包成功！" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "[成功] 可执行文件位置: dist\$Name\" -ForegroundColor Green

    # 7.5) 自动补齐 installer.iss 所需文件
    Write-Host "[补齐] 检查并补齐 installer.iss 所需文件..." -ForegroundColor Yellow

    # 补齐字体文件
    $fontSrc = "MiSans-Regular.ttf"
    $fontDst = "assets\fonts\MiSans-Regular.ttf"
    if (Test-Path $fontSrc) {
        Copy-Item $fontSrc $fontDst -Force
    }

    # 补齐 app.ico（仅在有效时拷贝，避免安装器失败）
    if ((Test-Path "app.ico") -and (-not (Test-Path "assets\app.ico"))) {
        if (Test-ValidIco -Path "app.ico") {
            Copy-Item "app.ico" "assets\app.ico" -Force
        } else {
            Write-Host "[补齐] 根目录 app.ico 无效，已忽略" -ForegroundColor Yellow
        }
    }

    # 补齐 README.txt
    if ((Test-Path "README.txt") -and (-not (Test-Path "dist\$Name\README.txt"))) {
        Copy-Item "README.txt" "dist\$Name\README.txt" -Force
    }

    # 补齐 LICENSE.txt
    if ((Test-Path "LICENSE.txt") -and (-not (Test-Path "dist\$Name\LICENSE.txt"))) {
        Copy-Item "LICENSE.txt" "dist\$Name\LICENSE.txt" -Force
    }

    # 补齐 data 目录和空 data.json
    $dataDir = "dist\$Name\data"
    if (-not (Test-Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir | Out-Null
    }
    $dataFile = "$dataDir\data.json"
    if (-not (Test-Path $dataFile)) {
        '{}' | Out-File -Encoding UTF8 $dataFile
    }

    Write-Host "[补齐] 文件补齐完成" -ForegroundColor Green

    # 7.6) 确保 dist 顶层包含 assets（避免仅在 _internal 下导致运行时找不到字体）
    $distDir = "dist\$Name"
    $distAssets = Join-Path $distDir "assets"
    $distInternalAssets = Join-Path $distDir "_internal\assets"
    if (-not (Test-Path $distAssets)) { New-Item -ItemType Directory -Path $distAssets | Out-Null }

    $copiedFrom = $null
    if (Test-Path $distInternalAssets) {
        Write-Host "[资源] 发现 _internal\\assets，复制到顶层 assets..." -ForegroundColor Yellow
        Copy-Item -Path (Join-Path $distInternalAssets '*') -Destination $distAssets -Recurse -Force -ErrorAction SilentlyContinue
        $copiedFrom = $distInternalAssets
    } elseif (Test-Path "assets") {
        Write-Host "[资源] 复制项目根 assets 到 dist 顶层..." -ForegroundColor Yellow
        Copy-Item -Path (Join-Path "assets" '*') -Destination $distAssets -Recurse -Force -ErrorAction SilentlyContinue
        $copiedFrom = (Join-Path $ScriptDir "assets")
    }

    # 确保字体存在于 dist 顶层 assets\fonts
    $distFontsDir = Join-Path $distAssets "fonts"
    if (-not (Test-Path $distFontsDir)) { New-Item -ItemType Directory -Path $distFontsDir | Out-Null }
    $miSansSrc = "assets\fonts\MiSans-Regular.ttf"
    $miSansDst = Join-Path $distFontsDir "MiSans-Regular.ttf"
    if (-not (Test-Path $miSansDst)) {
        if (Test-Path $miSansSrc) {
            Copy-Item $miSansSrc $miSansDst -Force
            Write-Host "[字体] 已补齐 MiSans-Regular.ttf 到 dist 顶层 assets\\fonts" -ForegroundColor Green
        } else {
            Write-Host "[字体] 警告：未找到 MiSans-Regular.ttf，字体可能无法生效" -ForegroundColor Yellow
        }
    }

    if ($copiedFrom) {
        Write-Host "[资源] 顶层 assets 就绪（来源：$copiedFrom）" -ForegroundColor Green
    } else {
        Write-Host "[资源] 提示：未找到可复制的 assets 源，若需要自定义字体/图标，请添加到项目根 assets 目录" -ForegroundColor Yellow
    }
}

# 8) 生成安装程序
if (-not $SkipInstaller) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  生成安装程序..." -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""

    # 检查 Inno Setup
    $InnoSetupPaths = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe"
    )

    $ISCC = $null
    foreach ($path in $InnoSetupPaths) {
        if (Test-Path $path) {
            $ISCC = $path
            break
        }
    }

    if ($null -eq $ISCC) {
        Write-Host "[警告] 未找到 Inno Setup" -ForegroundColor Yellow
        Write-Host "[提示] 请安装 Inno Setup 6: https://jrsoftware.org/isinfo.php" -ForegroundColor Yellow
        Write-Host "[提示] 安装后重新运行脚本以生成安装程序" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "您仍然可以使用 dist\$Name 目录中的文件" -ForegroundColor Cyan
    } else {
        Write-Host "[信息] 找到 Inno Setup: $ISCC" -ForegroundColor Green
        
        # 检查 installer.iss
        if (-not (Test-Path "installer.iss")) {
            Write-Host "[错误] 未找到 installer.iss 文件" -ForegroundColor Red
            exit 1
        }

        # 生成安装程序
        Write-Host "[安装器] 执行 Inno Setup 编译..." -ForegroundColor Yellow

        # 智能启用中文语言：若系统存在 ChineseSimplified.isl，则传入 /DUseZh=1
        $isccDir = Split-Path -Path $ISCC -Parent
        $candidate1 = "$isccDir\Languages\ChineseSimplified.isl"
        $candidate2 = "${env:ProgramFiles(x86)}\Inno Setup 6\Languages\ChineseSimplified.isl"
        $candidate3 = "${env:ProgramFiles}\Inno Setup 6\Languages\ChineseSimplified.isl"
        $LangFileCandidates = @($candidate1, $candidate2, $candidate3)
        $EnableZh = $false
        foreach ($lf in $LangFileCandidates) { if (Test-Path $lf) { $EnableZh = $true; break } }

        if ($EnableZh) {
            Write-Host "[安装器] 检测到中文语言包，将启用中英文界面" -ForegroundColor Green
            & $ISCC "/DUseZh=1" "installer.iss"
        } else {
            Write-Host "[安装器] 未检测到中文语言包，将仅生成英文界面" -ForegroundColor Yellow
            & $ISCC "installer.iss"
        }

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "================================================" -ForegroundColor Green
            Write-Host "  安装程序生成成功！" -ForegroundColor Green
            Write-Host "================================================" -ForegroundColor Green
            Write-Host ""
            
            if (Test-Path "installer_output") {
                Write-Host "安装程序位置:" -ForegroundColor Cyan
                Get-ChildItem -Path "installer_output" -Filter "*.exe" | ForEach-Object {
                    Write-Host "  - $($_.FullName)" -ForegroundColor Yellow
                    Write-Host "  - 大小: $([math]::Round($_.Length / 1MB, 2)) MB" -ForegroundColor Gray
                }
            }
        } else {
            Write-Host ""
            Write-Host "================================================" -ForegroundColor Red
            Write-Host "  安装程序生成失败" -ForegroundColor Red
            Write-Host "================================================" -ForegroundColor Red
            Write-Host ""
            Write-Host "[提示] 请检查 installer.iss 配置" -ForegroundColor Yellow
        }
    }
}

# 9) 总结
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  构建完成" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "输出文件:" -ForegroundColor Cyan
Write-Host "  1. 可执行文件: dist\$Name\" -ForegroundColor Yellow
if (-not $SkipInstaller -and (Test-Path "installer_output")) {
    Write-Host "  2. 安装程序: installer_output\" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "提示:" -ForegroundColor Cyan
Write-Host "  - 可直接运行: dist\$Name\$Name.exe" -ForegroundColor Gray
Write-Host "  - 或分发安装程序给用户安装" -ForegroundColor Gray
Write-Host ""
