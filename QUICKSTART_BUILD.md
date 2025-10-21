# 快速打包指南

## 一键打包（推荐）

在项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

等待几分钟后，可执行文件将生成在 `dist\CONTER\` 目录下。

## 参数选项

```powershell
# 清理旧文件后打包
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Clean

# 自定义应用名称
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Name "MyApp"

# 组合使用
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Clean -Name "CONTER"
```

注意：脚本统一使用 PyInstaller 打包，无需额外参数指定。

## 运行打包后的应用

```powershell
cd dist\CONTER
.\CONTER.exe
```

## 常见问题

### 1. 提示无法加载脚本文件

```powershell
# 临时允许执行脚本
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\build.ps1
```

### 2. 打包失败

- 检查网络连接（需下载依赖）
- 确保项目路径不包含中文或特殊字符
- 查看终端错误信息

### 3. 字体未生效

确保字体文件已放入：`assets\fonts\MiSans-Regular.ttf`

### 4. 缺少依赖

手动安装：

```powershell
.venv\Scripts\python.exe -m pip install flet openpyxl pandas
```

## 详细文档

完整打包说明请参考：[BUILD.md](BUILD.md)
