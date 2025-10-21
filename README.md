# 点名器应用 (Name Picker)# 点名器应用 (Name Picker)# 点名器应用

一个基于 Flet 框架开发的多平台点名器应用，支持 Windows、macOS、Linux、Web 和移动平台。一个基于 Flet 框架开发的多平台点名器应用，支持 Windows、macOS、Linux、Web 和移动平台。一个基于 Flet 框架开发的多平台点名器应用，支持 Windows、macOS、Linux、Web 和移动平台。

## ✨ 功能特点## ✨ 功能特点## 功能特点

- 🌍 **多语言支持**: 支持中文、英文、法文，可在应用内实时切换- 📋 **Excel 导入导出**: 支持从 Excel 文件导入/导出学生名单- 📋 **Excel 导入**: 支持从 Excel 文件导入名单

- 📋 **Excel 导入导出**: 支持从 Excel 文件导入/导出学生名单

- 🎲 **多样化抽取规则**: - 🎲 **多样化抽取规则**: - 🎲 **多样化抽取规则**:

  - 随机抽取 (Random Pick)

  - 权重抽取 (Weighted Pick) - 可设置不同权重值 - 随机抽取 (Random Pick) - 随机抽取

  - 最少抽取 (Least Picked) - 优先抽取被点名次数最少的学生

  - 排除已抽取 - 只从未被抽取的学生中选择 - 权重抽取 (Weighted Pick) - 可设置不同权重值 - 权重抽取

- 🎨 **美观的 UI**: 基于 Material Design 3 的现代化界面

- ⚡ **高性能**: 使用异步编程（async/await），保证界面流畅不卡顿 - 最少抽取 (Least Picked) - 优先抽取被点名次数最少的学生 - 排除已抽取

- 🎬 **动画效果**: 点名过程带有流畅的动画效果和视觉反馈

- 💾 **数据持久化**: 自动保存名单和抽取历史到本地 - 排除已抽取 - 只从未被抽取的学生中选择 - 指定抽取人数

- 📊 **统计信息**: 实时显示抽取统计数据

- ✏️ **完整的 CRUD 操作**: 支持添加、编辑、删除学生信息- 🎨 **美观的 UI**: 基于 Material Design 3 的现代化界面- 🎨 **美观的 UI**: 基于 Material Design 的现代化界面

## 🚀 快速开始- ⚡ **高性能**: 使用异步编程（async/await），保证界面流畅不卡顿- ⚡ **高性能**: 使用异步编程，保证界面流畅

### 1. 环境要求- 🎬 **动画效果**: 点名过程带有流畅的动画效果和视觉反馈- 🎬 **动画效果**: 点名过程带有动画效果

- Python 3.8 或更高版本- 💾 **数据持久化**: 自动保存名单和抽取历史到本地- 💾 **数据持久化**: 自动保存名单和抽取历史

### 2. 安装依赖- 📊 **统计信息**: 实时显示抽取统计数据

````bash- ✏️ **完整的 CRUD 操作**: 支持添加、编辑、删除学生信息## 安装依赖

pip install -r requirements.txt

```## 🚀 快速开始```bash



或者手动安装：pip install -r requirements.txt



```bash### 1. 环境要求```

pip install flet openpyxl pandas

```- Python 3.8 或更高版本## 运行应用



### 3. 运行应用### 2. 安装依赖### 桌面应用



#### 方式一：直接运行Python脚本`bash`bash

```bash

python main.pypip install -r requirements.txtflet run main.py

````

````

#### 方式二：使用批处理文件（Windows）

双击 `run.bat` 文件



#### 方式三：作为Web应用运行或者手动安装：### Web 应用

```bash

flet run --web main.py

```

```bash```bash

## 🌍 多语言支持

pip install flet openpyxl pandasflet run --web main.py

### 切换语言

````

应用启动后，在顶部工具栏找到"语言"下拉菜单，选择您想要的语言：

### 3. 运行应用## 使用说明

- 🇨🇳 中文 (Chinese)

- 🇬🇧 English#### 方式一：直接运行 Python 脚本 1. 点击"导入 Excel"按钮导入名单（Excel 格式：姓名列）

- 🇫🇷 Français

`````bash2. 选择抽取规则和参数

语言切换是实时的，无需重启应用。详细信息请查看 [MULTILANGUAGE.md](MULTILANGUAGE.md)

python main.py3. 点击"开始点名"按钮进行抽取

## 📖 使用指南

```4. 查看抽取历史和统计信息

### Excel导入格式



Excel文件应包含以下列（第一行为表头）：

#### 方式二：使用批处理文件（Windows）## 项目结构

| 姓名 (必需) | 学号 (可选) | 权重 (可选) |

|------------|------------|------------|双击 `run.bat` 文件

| 张三       | 2024001    | 1.0        |

| 李四       | 2024002    | 1.5        |````



- **第一列**: 学生姓名（必需）#### 方式三：作为 Web 应用运行 CONTER/

- **第二列**: 学号或ID（可选）

- **第三列**: 权重值（可选，默认1.0，用于权重抽取）````bash├── main.py              # 主程序入口



### 创建示例Excel文件flet run --web main.py├── models.py            # 数据模型



```bash```├── services.py          # 业务逻辑

python create_sample.py

```├── ui/                  # UI组件



这会在当前目录生成 `sample_students.xlsx` 文件。## 📖 使用指南│   ├── __init__.py



### 操作步骤│   ├── main_view.py     # 主界面



1. **导入名单**: 点击"导入Excel"按钮，选择Excel文件### Excel导入格式│   └── components.py    # UI组件

2. **添加学生**: 点击"添加学生"按钮，手动添加学生信息

3. **设置抽取规则**:├── utils.py             # 工具函数

   - 选择抽取规则（随机/权重/最少抽取）

   - 设置抽取人数Excel文件应包含以下列（第一行为表头）：├── requirements.txt     # 依赖包

   - 可选择"排除已抽取"

4. **开始点名**: 点击"开始点名"按钮└── README.md           # 说明文档

5. **查看结果**: 抽取结果会以动画形式显示

6. **管理数据**:| 姓名 (必需) | 学号 (可选) | 权重 (可选) |```

   - 编辑学生信息：点击学生卡片的编辑按钮

   - 删除学生：点击学生卡片的删除按钮|------------|------------|------------|

   - 重置记录：点击"重置记录"清空抽取历史| 张三       | 2024001    | 1.0        |

   - 导出Excel：点击"导出Excel"导出完整数据到桌面| 李四       | 2024002    | 1.5        |



## 📁 项目结构- **第一列**: 学生姓名（必需）

- **第二列**: 学号或ID（可选）

```- **第三列**: 权重值（可选，默认1.0，用于权重抽取）

CONTER/

├── main.py              # 主程序入口### 创建示例Excel文件

├── models.py            # 数据模型（Student, DataManager等）

├── services.py          # 业务逻辑（PickerService, ExcelService等）```bash

├── utils.py             # 工具函数python create_sample.py

├── i18n.py              # 多语言支持模块````

├── ui/                  # UI组件目录

│   ├── __init__.py这会在当前目录生成 `sample_students.xlsx` 文件。

│   ├── main_view.py     # 主界面视图

│   └── components.py    # 可复用UI组件### 操作步骤

├── create_sample.py     # 创建示例Excel文件的脚本

├── requirements.txt     # Python依赖包列表1. **导入名单**: 点击"Import Excel"按钮，选择 Excel 文件

├── run.bat             # Windows启动脚本2. **添加学生**: 点击"Add Student"按钮，手动添加学生信息

├── run.sh              # Linux/macOS启动脚本3. **设置抽取规则**:

├── .gitignore          # Git忽略文件配置   - 选择抽取规则（Random/Weighted/Least Picked）

├── README.md           # 项目说明文档（本文件）   - 设置抽取人数

├── MULTILANGUAGE.md    # 多语言支持说明   - 可选择"Exclude Picked"排除已抽取的学生

├── USER_GUIDE.md       # 详细使用指南4. **开始点名**: 点击"Start Pick"按钮

├── EXCEL_FORMAT.md     # Excel格式说明5. **查看结果**: 抽取结果会以动画形式显示

├── PROJECT_SUMMARY.md  # 技术总结6. **管理数据**:

└── DEMO_GUIDE.md       # 演示指南   - 编辑学生信息：点击学生卡片的编辑按钮

```   - 删除学生：点击学生卡片的删除按钮

   - 重置记录：点击"Reset Records"清空抽取历史

## 🔧 技术特性   - 导出 Excel：点击"Export Excel"导出完整数据到桌面



### 异步编程## 📁 项目结构

- 使用`async/await`处理耗时操作（Excel导入、点名动画等）

- 使用`page.run_task()`运行异步任务```

- 避免UI阻塞，保证界面响应流畅CONTER/

- 所有耗时操作都在后台执行├── main.py              # 主程序入口

├── models.py            # 数据模型（Student, DataManager等）

### 多语言支持├── services.py          # 业务逻辑（PickerService, ExcelService等）

- 自定义i18n模块├── utils.py             # 工具函数

- 支持中文、英文、法文├── ui/                  # UI组件目录

- 实时语言切换│   ├── __init__.py

- 易于扩展新语言│   ├── main_view.py     # 主界面视图

│   └── components.py    # 可复用UI组件

### 数据持久化├── create_sample.py     # 创建示例Excel文件的脚本

- 使用JSON格式存储├── requirements.txt     # Python依赖包列表

- Windows: `C:\Users\<用户名>\.conter\data.json`├── run.bat             # Windows启动脚本

- macOS/Linux: `~/.conter/data.json`├── run.sh              # Linux/macOS启动脚本

- 自动加载和保存，无需手动操作├── .gitignore          # Git忽略文件配置

├── README.md           # 项目说明文档（本文件）

### 多平台支持├── USER_GUIDE.md       # 详细使用指南

- 基于Flet框架，支持跨平台运行└── EXCEL_FORMAT.md     # Excel格式说明

- ✅ 桌面应用（Windows、macOS、Linux）```

- ✅ Web应用（浏览器访问）

- ✅ 可打包为独立应用## 🔧 技术特性



## 💡 抽取规则说明### 异步编程



### 1. 随机抽取 (Random Pick)- 使用`async/await`处理耗时操作（Excel 导入、点名动画等）

- 每个学生被抽中的概率完全相等- 避免 UI 阻塞，保证界面响应流畅

- 适合公平性要求高的场景- 所有耗时操作都在后台执行

- 可配合"排除已抽取"使用

### 数据持久化

### 2. 权重抽取 (Weighted Pick)

- 根据权重值决定被抽中概率- 使用 JSON 格式存储数据

- 权重越高，被抽中概率越大- Windows: `C:\Users\<用户名>\.conter\data.json`

- 适合需要重点关注某些学生的场景- macOS/Linux: `~/.conter/data.json`

- 权重值必须大于0- 自动加载和保存，无需手动操作



### 3. 最少抽取 (Least Picked)### 多平台支持

- 优先抽取被点名次数最少的学生

- 确保每个学生被抽取的机会相对均等- 基于 Flet 框架，支持跨平台运行

- 适合长期使用的场景- ✅ 桌面应用（Windows、macOS、Linux）

- ✅ Web 应用（浏览器访问）

### 4. 排除已抽取 (Exclude Picked)- ✅ 可打包为独立应用

- 仅在随机抽取模式下可用

- 只从未被抽取的学生中选择## 💡 抽取规则说明

- 适合需要遍历所有学生的场景

### 1. 随机抽取 (Random Pick)

## 📊 统计功能

- 每个学生被抽中的概率完全相等

右侧统计面板实时显示：- 适合公平性要求高的场景

- 总人数 (Total)- 可配合"Exclude Picked"使用

- 已抽取人数 (Picked)

- 未抽取人数 (Unpicked)### 2. 权重抽取 (Weighted Pick)

- 总抽取次数 (Total Picks)

- 根据权重值决定被抽中概率

## 🎨 界面特点- 权重越高，被抽中概率越大

- 适合需要重点关注某些学生的场景

- Material Design 3 设计规范- 权重值必须大于 0

- 现代化的卡片式布局

- 流畅的动画效果（缩放、淡入淡出）### 3. 最少抽取 (Least Picked)

- 响应式设计

- 直观的操作界面- 优先抽取被点名次数最少的学生

- 悬停效果和视觉反馈- 确保每个学生被抽取的机会相对均等

- 多语言界面支持- 适合长期使用的场景



## 📝 开发说明### 4. 排除已抽取 (Exclude Picked)



### 核心依赖- 仅在随机抽取模式下可用

- `flet >= 0.24.0`: 跨平台UI框架- 只从未被抽取的学生中选择

- `pandas >= 2.0.0`: Excel文件读写- 适合需要遍历所有学生的场景

- `openpyxl >= 3.1.2`: Excel文件操作

## 📊 统计功能

### 代码结构

- **models.py**: 数据模型（Student, PickRecord, DataManager）右侧统计面板实时显示：

- **services.py**: 业务逻辑服务（抽取、导入导出、统计）

- **i18n.py**: 国际化支持（多语言翻译）- 总人数 (Total)

- **ui/components.py**: 可复用的UI组件- 已抽取人数 (Picked)

- **ui/main_view.py**: 主界面逻辑和事件处理- 未抽取人数 (Unpicked)

- 总抽取次数 (Total Picks)

### 设计模式

- MVC架构：模型-视图分离## 🎨 界面特点

- 服务层：业务逻辑封装

- 组件化：UI组件可复用- Material Design 3 设计规范

- i18n模式：多语言支持- 现代化的卡片式布局

- 流畅的动画效果（缩放、淡入淡出）

## ⚠️ 注意事项- 响应式设计

- 直观的操作界面

1. Excel文件第一列必须是姓名- 悬停效果和视觉反馈

2. 权重值必须为正数

3. 清空数据操作不可恢复，操作前请确认## 📝 开发说明

4. 数据自动保存在用户目录，建议定期备份

5. 切换语言不会影响数据### 核心依赖



## 🐛 Bug修复- `flet >= 0.24.0`: 跨平台 UI 框架

- `pandas >= 2.0.0`: Excel 文件读写

### v2.0 更新- `openpyxl >= 3.1.2`: Excel 文件操作

- ✅ 修复了异步函数调用问题

- ✅ 使用`page.run_task()`正确处理async函数### 代码结构

- ✅ 修复了点名失败的bug

- ✅ 添加了完整的多语言支持- **models.py**: 数据模型（Student, PickRecord, DataManager）

- ✅ 优化了UI响应速度- **services.py**: 业务逻辑服务（抽取、导入导出、统计）

- **ui/components.py**: 可复用的 UI 组件

## 🆕 新功能- **ui/main_view.py**: 主界面逻辑和事件处理



### v2.0 新增### 设计模式

- 🌍 多语言支持（中文、英文、法文）

- 🔄 实时语言切换- MVC 架构：模型-视图分离

- 🐛 修复异步编程问题- 服务层：业务逻辑封装

- ⚡ 性能优化- 组件化：UI 组件可复用



## 🚀 未来计划## ⚠️ 注意事项



- 添加更多语言支持（西班牙语、日语等）1. Excel 文件第一列必须是姓名

- 历史记录可视化2. 权重值必须为正数

- 导出PDF报告3. 清空数据操作不可恢复，操作前请确认

- 自定义主题和深色模式4. 数据自动保存在用户目录，建议定期备份

- 云端数据同步

## 🐛 故障排除

## 📚 更多文档

### 问题：无法导入 Excel 文件

- [详细使用指南](USER_GUIDE.md)

- [Excel格式说明](EXCEL_FORMAT.md)- 检查文件格式是否为 `.xlsx` 或 `.xls`

- [多语言支持说明](MULTILANGUAGE.md)- 确保第一列包含姓名数据

- [项目技术总结](PROJECT_SUMMARY.md)- 尝试用 Excel 重新保存文件

- [演示指南](DEMO_GUIDE.md)

### 问题：点名无反应

## 🤝 贡献

- 确保已添加学生

欢迎提交Issue和Pull Request！- 检查抽取人数设置是否合理

- 如果勾选了"Exclude Picked"，确保还有未抽取的学生

## 📄 许可证

### 问题：应用无法启动

MIT License

- 确保已安装所有依赖：`pip install -r requirements.txt`

---- 检查 Python 版本是否 >= 3.8



**享受点名的乐趣！** 🎉  ## 📚 更多文档

**Enjoy the fun of name picking!** 🎉

**Profitez du plaisir de sélection!** 🎉- [详细使用指南](USER_GUIDE.md)

- [Excel 格式说明](EXCEL_FORMAT.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**享受点名的乐趣！** 🎉
`````
