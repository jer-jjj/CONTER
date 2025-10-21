# 应用图标说明

## 📍 图标位置

将应用图标放置在：

```
assets/app.ico
```

## 📐 图标规格

### 格式要求

- **文件格式**：ICO（Windows 图标格式）
- **文件名**：app.ico
- **位置**：assets 目录

### 尺寸建议

图标文件应包含多个尺寸，以适应不同显示需求：

| 尺寸    | 用途                |
| ------- | ------------------- |
| 16×16   | 小图标、任务栏      |
| 32×32   | 标准图标            |
| 48×48   | 中等图标            |
| 256×256 | 高清图标、Win 10/11 |

## 🎨 创建图标

### 方式一：在线转换（推荐）

1. 准备一张 PNG 图片（推荐 512×512 或更大）
2. 访问在线转换工具：

   - https://www.icoconverter.com/
   - https://convertio.co/zh/png-ico/
   - https://onlineconvertfree.com/zh/convert-format/png-to-ico/

3. 上传 PNG 文件
4. 选择包含多个尺寸（16, 32, 48, 256）
5. 下载生成的 ICO 文件
6. 重命名为 `app.ico` 并放入 `assets` 目录

### 方式二：使用桌面软件

#### Windows

- **IcoFX**：专业图标编辑器
- **GIMP**：免费图像编辑器（支持 ICO 插件）
- **Paint.NET**：配合 ICO 插件

#### macOS

- **Icon Slate**
- **Image2icon**

#### Linux

- **GIMP**（内置 ICO 支持）
- **ImageMagick**（命令行）

### 方式三：使用 Python 脚本

```python
from PIL import Image

# 加载 PNG 图片
img = Image.open('your_image.png')

# 调整大小并保存为多尺寸 ICO
img.save('assets/app.ico', format='ICO',
         sizes=[(16,16), (32,32), (48,48), (256,256)])
```

需要安装：`pip install Pillow`

## 🖼️ 设计建议

### 图标设计原则

- ✅ 简洁明了，易于识别
- ✅ 在小尺寸下仍然清晰
- ✅ 使用鲜明的颜色
- ✅ 避免过多细节
- ✅ 考虑深色和浅色背景

### 主题建议

对于点名器应用，可以考虑：

- 📋 名单图标
- 🎲 骰子图标
- 👥 人群图标
- ✓ 选中标记
- 📊 统计图表

### 颜色建议

- 主色：蓝色（专业、信任）
- 辅色：绿色（成功、正面）
- 强调：橙色/黄色（活力、醒目）

## 📂 示例图标资源

### 免费图标网站

- **Flaticon**：https://www.flaticon.com/
- **Icons8**：https://icons8.com/
- **IconArchive**：https://www.iconarchive.com/
- **IconFinder**：https://www.iconfinder.com/

### 搜索关键词

- "random picker"
- "name picker"
- "list"
- "dice"
- "people select"

## 🔧 使用图标

### 开发模式

```powershell
# 直接运行，图标会自动加载
python main.py
```

### 打包时

```powershell
# 指定图标路径
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -IconPath "assets\app.ico"

# 或使用默认路径（会自动查找 assets\app.ico）
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1
```

### 如果没有图标

- ❌ 不影响应用功能
- ℹ️ 使用 Windows 默认图标
- ⚠️ 显示效果较差
- 💡 建议添加自定义图标

## ✅ 验证图标

### 方法一：在 Windows 中查看

1. 右键点击 `app.ico`
2. 选择"属性"
3. 查看"预览"标签

### 方法二：使用 IrfanView

1. 下载 IrfanView（免费）
2. 打开 `app.ico`
3. 查看所有尺寸

### 方法三：在线预览

1. 上传到：https://www.icoconverter.com/
2. 查看所有内嵌尺寸

## 🎯 快速开始

如果你现在没有图标：

1. **临时方案**：使用默认图标，应用仍可正常使用
2. **快速方案**：从免费图标网站下载并转换
3. **专业方案**：设计师制作或使用专业软件

## 📝 图标检查清单

打包前确认：

- [ ] 图标文件为 ICO 格式
- [ ] 文件名为 `app.ico`
- [ ] 位于 `assets` 目录
- [ ] 包含多个尺寸（16, 32, 48, 256）
- [ ] 在小尺寸下仍然清晰
- [ ] 在深色背景下可见
- [ ] 在浅色背景下可见

## 🔄 更新图标

更新图标后需要：

1. 清理旧构建：`-Clean`
2. 重新打包应用
3. 重新生成安装器

```powershell
powershell -ExecutionPolicy Bypass -File .\build_installer.ps1 -Clean
```

---

**提示**：一个好的图标能显著提升应用的专业形象！
