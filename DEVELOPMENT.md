# 开发文档 (Development Guide)

## 📋 目录

- [项目概览](#项目概览)
- [技术栈](#技术栈)
- [项目架构](#项目架构)
- [开发环境搭建](#开发环境搭建)
- [代码结构说明](#代码结构说明)
- [核心模块详解](#核心模块详解)
- [开发规范](#开发规范)
- [调试指南](#调试指南)
- [测试指南](#测试指南)
- [性能优化](#性能优化)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)

---

## 项目概览

**CONTER** 是一个基于 Flet 框架开发的跨平台点名器应用，支持多种抽取规则、数据持久化和多语言界面。

### 核心功能

- 🎲 多样化抽取规则（随机、权重、最少抽取）
- 📊 Excel 导入导出
- 💾 数据持久化（JSON）
- 🌍 多语言支持（中文、英文、法语）
- ⚡ 异步编程保证界面流畅
- 🎨 Material Design 3 界面

### 技术特点

- **跨平台**：Windows / macOS / Linux / Web / Mobile
- **现代化**：使用 Python 3.10+ 与 Flet 0.24+
- **响应式**：异步编程（async/await）
- **模块化**：MVC 架构，代码清晰易维护

---

## 技术栈

| 技术     | 版本    | 用途                    |
| -------- | ------- | ----------------------- |
| Python   | 3.10+   | 主要编程语言            |
| Flet     | 0.24.0+ | UI 框架（基于 Flutter） |
| Pandas   | 2.0.0+  | Excel 数据处理          |
| OpenPyXL | 3.1.2+  | Excel 文件读写          |

### 可选工具

- **PyInstaller** / **flet pack**：打包为可执行文件
- **Git**：版本控制

---

## 项目架构

### 架构模式：MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────────┐
│                     Flet Page                        │
│                   (ft.app)                           │
└──────────────────┬──────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │     main.py       │
         │  (Entry Point)    │
         └─────────┬─────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
┌─────▼─────┐ ┌───▼────┐ ┌─────▼──────┐
│   View    │ │ Model  │ │  Service   │
│ (ui/*.py) │ │(models)│ │(services)  │
└───────────┘ └────────┘ └────────────┘
      │            │            │
      └────────────┼────────────┘
                   │
            ┌──────▼──────┐
            │   i18n.py   │
            │   utils.py  │
            └─────────────┘
```

### 目录结构

```
CONTER/
├── main.py                 # 应用入口
├── models.py              # 数据模型（Student、DataManager）
├── services.py            # 业务逻辑（PickerService、ExcelService）
├── i18n.py                # 国际化（多语言支持）
├── utils.py               # 工具函数
├── ui/                    # UI 层
│   ├── main_view.py       # 主界面
│   └── components.py      # 可复用组件
├── assets/                # 资源文件
│   └── fonts/             # 字体文件（MiSans）
├── .venv/                 # 虚拟环境
├── requirements.txt       # 依赖清单
├── build.ps1              # 打包脚本（Windows）
├── BUILD.md               # 打包文档
├── DEVELOPMENT.md         # 开发文档（本文件）
├── README.md              # 项目说明
├── CHANGELOG.md           # 更新日志
├── MULTILANGUAGE.md       # 多语言说明
└── USER_GUIDE.md          # 用户手册
```

---

## 开发环境搭建

### 1. 克隆项目

```bash
git clone <repository-url>
cd CONTER
```

### 2. 创建虚拟环境

```bash
# Windows
py -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install flet>=0.24.0 openpyxl>=3.1.2 pandas>=2.0.0
```

### 4. 准备字体文件（可选）

将 MiSans 字体放入：

```
assets/fonts/MiSans-Regular.ttf
```

### 5. 运行应用

```bash
python main.py
```

---

## 代码结构说明

### main.py - 应用入口

```python
def main(page: ft.Page):
    # 1. 初始化国际化
    i18n = I18n('zh_CN')

    # 2. 配置页面（窗口大小、主题、字体）
    page.title = i18n.t('app_title')
    page.fonts = {"MiSans": "fonts/MiSans-Regular.ttf"}
    page.theme = ft.Theme(font_family="MiSans")

    # 3. 初始化数据管理器
    data_manager = DataManager(data_file)

    # 4. 创建主视图
    main_view = MainView(page, data_manager, i18n)
    page.add(main_view.build())
```

### models.py - 数据模型

#### Student 类

```python
@dataclass
class Student:
    name: str              # 学生姓名
    id: Optional[str]      # 学号（可选）
    weight: float = 1.0    # 权重值
    picked_count: int = 0  # 被抽取次数
    last_picked: Optional[datetime] = None  # 最后抽取时间
```

#### DataManager 类

- 数据持久化管理
- 学生增删改查
- JSON 序列化/反序列化

### services.py - 业务逻辑

#### PickerService

- `pick_random(count, exclude_picked)`：随机抽取
- `pick_weighted(count)`：权重抽取（无放回）
- `pick_least_picked(count)`：最少抽取（逐层填充）

#### ExcelService

- `import_from_excel(file_path)`：从 Excel 导入
- `export_to_excel(students, file_path)`：导出到 Excel

#### StatisticsService

- `get_statistics(data_manager)`：获取统计信息

### ui/main_view.py - 主界面

#### MainView 类

- `build()`：构建界面布局
- `_start_picking()`：启动抽取流程
- `_pick_async()`：异步抽取逻辑
- `_refresh_students_list()`：刷新学生列表
- `_refresh_statistics()`：刷新统计面板

### ui/components.py - UI 组件

#### StudentCard

- 学生信息卡片
- 包含编辑/删除按钮

#### PickResultCard

- 抽取结果卡片
- 支持入场动画

#### StatisticsPanel

- 统计信息面板

### i18n.py - 国际化

```python
class I18n:
    def __init__(self, language='zh_CN')
    def t(self, key: str, **kwargs) -> str  # 翻译函数
    def set_language(self, language: str)   # 切换语言
```

支持的语言：

- `zh_CN`：简体中文
- `en`：English
- `fr`：Français

---

## 核心模块详解

### 异步编程模式

Flet 事件处理器**不能**直接使用 `async def`，需通过 `page.run_task()` 调度：

```python
# ❌ 错误示例
async def _on_button_click(e):
    result = await some_async_function()

# ✅ 正确示例
def _on_button_click(e):
    self.page.run_task(self._do_async_work)

async def _do_async_work(self):
    result = await some_async_function()
    self.page.update()
```

### 数据持久化流程

```
用户操作 → DataManager 修改内存数据 → save_data() → 写入 JSON 文件
         ↓
    启动应用 → load_data() → 从 JSON 文件读取 → 恢复内存数据
```

数据存储位置：

**开发模式**：

- `项目根目录/data/data.json`

**打包后**：

- `可执行文件目录/data/data.json`

优势：

- ✅ 便携性：数据与应用在同一目录
- ✅ 可见性：用户可直接访问数据文件
- ✅ 多实例：支持运行多个独立应用副本

详见：[DATA_STORAGE.md](DATA_STORAGE.md)

### 抽取算法详解

#### 1. 随机抽取（Random Pick）

```python
# 无放回抽取
picked = random.sample(candidates, count)

# 排除已抽取
if exclude_picked:
    candidates = [s for s in candidates if s.picked_count == 0]
```

#### 2. 权重抽取（Weighted Pick）

```python
# 无放回加权抽取（避免重复）
while len(picked) < count and working_pool:
    weights = [max(0.000001, s.weight) for s in working_pool]
    chosen = random.choices(working_pool, weights=weights, k=1)[0]
    picked.append(chosen)
    working_pool.remove(chosen)  # 从池中移除
```

#### 3. 最少抽取（Least Picked）

```python
# 按被抽取次数升序分组，逐层填充
candidates.sort(key=lambda s: (s.picked_count, s.name))
while remaining > 0 and i < n:
    current_count = candidates[i].picked_count
    group = [所有 picked_count == current_count 的学生]
    take = min(remaining, len(group))
    picked.extend(random.sample(group, take))
    remaining -= take
```

### UI 更新机制

```python
# 修改控件属性后必须调用 update()
self.text.value = "新内容"
self.page.update()

# 批量修改可减少 update() 次数
self.text1.value = "A"
self.text2.value = "B"
self.text3.value = "C"
self.page.update()  # 一次更新
```

---

## 开发规范

### 代码风格

#### 命名规范

- **类名**：PascalCase（如 `StudentCard`）
- **函数/方法**：snake_case（如 `pick_random`）
- **常量**：UPPER_CASE（如 `MAX_COUNT`）
- **私有方法**：`_`前缀（如 `_refresh_ui`）

#### 文档字符串

```python
def pick_weighted(self, count: int = 1) -> List[Student]:
    """
    权重抽取 - 权重越高概率越大
    :param count: 抽取人数
    :return: 被抽取的学生列表
    """
```

#### 类型注解

```python
def get_student(self, name: str) -> Optional[Student]:
    # 明确返回类型
```

### 文件编码

所有 Python 文件开头加入：

```python
# -*- coding: utf-8 -*-
```

### 导入顺序

```python
# 1. 标准库
import os
import json
from datetime import datetime

# 2. 第三方库
import flet as ft
import pandas as pd

# 3. 本地模块
from models import Student
from services import PickerService
```

### Git 提交规范

```
<type>: <subject>

<body>

<footer>
```

**Type 类型：**

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链

**示例：**

```
feat: 添加权重抽取无放回功能

- 修改 PickerService.pick_weighted 为逐个抽取
- 确保不会重复选中同一学生
- 更新相关单元测试

Closes #42
```

---

## 调试指南

### 打印调试

```python
# 使用 print 输出到控制台
print(f"选中学生: {student.name}")

# 查看对象内容
import pprint
pprint.pprint(data_manager.students)
```

### Flet 调试模式

```python
# 在 main.py 中启用
ft.app(target=main, view=ft.AppView.FLET_APP)  # 调试模式
```

### 日志记录

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告")
logger.error("错误")
```

### 常见断点位置

1. **抽取逻辑**：`services.py` 中的 `pick_*` 方法
2. **UI 更新**：`main_view.py` 中的 `_refresh_*` 方法
3. **数据保存**：`models.py` 中的 `save_data()`
4. **Excel 导入**：`services.py` 中的 `import_from_excel()`

---

## 测试指南

### 手动测试清单

#### 基础功能

- [ ] 添加学生
- [ ] 编辑学生
- [ ] 删除学生
- [ ] Excel 导入
- [ ] Excel 导出

#### 抽取功能

- [ ] 随机抽取（单人）
- [ ] 随机抽取（多人）
- [ ] 随机抽取（排除已抽取）
- [ ] 权重抽取（验证权重影响）
- [ ] 最少抽取（验证均衡性）

#### 边界测试

- [ ] 学生数为 0 时抽取
- [ ] 抽取人数 > 学生总数
- [ ] 排除已抽取后无可选学生
- [ ] 权重为 0 或负数
- [ ] Excel 文件格式错误
- [ ] 中文/特殊字符姓名

#### 多语言

- [ ] 切换到英文
- [ ] 切换到法语
- [ ] 切换后所有 UI 正确显示

#### 数据持久化

- [ ] 添加数据后关闭应用
- [ ] 重新打开应用验证数据存在
- [ ] 重置记录功能
- [ ] 清空所有数据功能

### 单元测试（示例）

创建 `tests/test_services.py`：

```python
import pytest
from models import Student, DataManager
from services import PickerService

def test_pick_random():
    dm = DataManager(':memory:')
    dm.students = [
        Student(name="张三"),
        Student(name="李四"),
        Student(name="王五"),
    ]

    service = PickerService(dm)
    picked = await service.pick_random(count=2, exclude_picked=False)

    assert len(picked) == 2
    assert picked[0] != picked[1]
```

---

## 性能优化

### UI 优化

#### 减少 update() 调用

```python
# ❌ 多次更新
for student in students:
    grid.controls.append(StudentCard(student))
    page.update()  # 每次都更新

# ✅ 批量更新
for student in students:
    grid.controls.append(StudentCard(student))
page.update()  # 一次更新
```

#### 使用虚拟滚动（大列表）

```python
# 当学生数量 > 100 时
grid = ft.GridView(
    expand=True,
    max_extent=300,  # 控制单元格大小
    child_aspect_ratio=2.5,
)
```

### 异步优化

```python
# 长时间操作使用异步
async def import_large_excel(file_path):
    await asyncio.sleep(0)  # 让出控制权
    # ... 处理数据
```

### 数据优化

```python
# 避免频繁保存
# ❌ 每次修改都保存
for student in students:
    dm.add_student(student)  # 内部调用 save_data()

# ✅ 批量添加后保存
for student in students:
    dm.students.append(student)
dm.save_data()  # 一次保存
```

---

## 常见问题

### Q1: 字体不显示 MiSans？

**A:** 检查以下步骤：

1. 字体文件是否在 `assets/fonts/MiSans-Regular.ttf`
2. `main.py` 中是否注册字体
3. `ft.app(target=main, assets_dir="assets")` 是否设置
4. 打包时是否包含 `--add-data "assets;assets"`

### Q2: 多人抽取只显示一个？

**A:** 已在 v2.0 修复，确保使用最新版本代码。

### Q3: Excel 导入失败？

**A:** 检查：

1. Excel 格式是否为 `.xlsx` 或 `.xls`
2. 第一列是否为姓名（必填）
3. 文件是否被其他程序占用
4. 路径是否包含特殊字符

### Q4: 打包后运行白屏？

**A:** 尝试：

1. 升级 flet 到最新版本
2. 检查终端是否有错误信息
3. 使用 `--noconsole` 改为不带该参数调试
4. 确认资源文件已打包

### Q5: 动画不流畅？

**A:**

1. 减少同时播放的动画数量
2. 降低动画时长（如 500ms → 300ms）
3. 使用 `page.run_task()` 确保异步执行

---

## 贡献指南

### 开发流程

1. **Fork 项目**
2. **创建功能分支**
   ```bash
   git checkout -b feature/new-feature
   ```
3. **编写代码**
   - 遵循代码规范
   - 添加必要的注释
   - 更新相关文档
4. **提交代码**
   ```bash
   git commit -m "feat: 添加新功能"
   ```
5. **推送分支**
   ```bash
   git push origin feature/new-feature
   ```
6. **创建 Pull Request**

### 代码审查标准

- ✅ 代码符合规范
- ✅ 有必要的注释和文档
- ✅ 功能正常工作
- ✅ 没有明显的性能问题
- ✅ 通过手动测试
- ✅ 不引入新的依赖（或已说明必要性）

### 需要帮助的领域

- [ ] 单元测试覆盖
- [ ] UI 自动化测试
- [ ] 英文/法语文档完善
- [ ] 更多语言支持
- [ ] macOS/Linux 打包脚本
- [ ] 深色模式支持
- [ ] 移动端适配

---

## 联系方式

- 项目仓库：`<repository-url>`
- 问题反馈：`<issues-url>`
- 开发者：`<developer-contact>`

---

**感谢你对 CONTER 项目的贡献！** 🎉

如有任何问题，欢迎在 Issues 中提出。
