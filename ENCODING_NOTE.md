# 重要提示：PowerShell 脚本编码说明

## 问题说明

如果你在编辑 `build.ps1` 后遇到类似错误：

```
数组索引表达式丢失或无效
参数列表中缺少参量
语句块或类型定义中缺少右"}"
```

这是因为 **PowerShell 脚本文件中的中文字符需要使用 UTF-8 with BOM 编码**。

## 解决方法

### 方法一：使用 PowerShell 命令修复

```powershell
# 在项目根目录运行
$content = Get-Content .\build.ps1 -Raw -Encoding UTF8
[System.IO.File]::WriteAllText("$PWD\build.ps1", $content, (New-Object System.Text.UTF8Encoding $true))
```

### 方法二：使用 VS Code 修复

1. 在 VS Code 中打开 `build.ps1`
2. 点击右下角的编码（显示为 `UTF-8`）
3. 选择 "Save with Encoding"（使用编码保存）
4. 选择 "UTF-8 with BOM"
5. 保存文件

### 方法三：使用记事本修复

1. 用记事本打开 `build.ps1`
2. 点击"文件" → "另存为"
3. 编码选择 "UTF-8"（Windows 记事本默认 UTF-8 就带 BOM）
4. 保存

## 验证编码

运行以下命令验证文件是否有 BOM：

```powershell
[System.IO.File]::ReadAllBytes('.\build.ps1')[0..2] -join ','
```

正确的输出应该是：`239,187,191`（这是 UTF-8 BOM 的标记）

如果输出不是这个，说明编码不正确，需要按上述方法修复。

## 预防措施

如果你需要编辑 `build.ps1`：

1. 使用支持 UTF-8 BOM 的编辑器（VS Code、Notepad++、记事本）
2. 不要使用某些默认 UTF-8 without BOM 的编辑器
3. 保存时确保选择 "UTF-8 with BOM" 编码

## 当前状态

✅ `build.ps1` 已修复为正确的 UTF-8 with BOM 编码
✅ 所有中文字符现在可以正确显示
✅ 脚本可以正常运行

## 测试脚本

运行以下命令测试脚本是否正常：

```powershell
# 显示前 10 行（测试中文显示）
powershell -ExecutionPolicy Bypass -Command "Get-Content .\build.ps1 | Select-Object -First 10"

# 显示帮助信息
powershell -ExecutionPolicy Bypass -File .\build.ps1 -?
```

如果中文正常显示，说明编码正确！
