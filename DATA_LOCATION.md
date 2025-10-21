# 数据存储功能说明

## ✅ 功能实现

用户名单和缓存文件现在存储在**可执行文件所在目录**，而非用户主目录。

## 📁 存储位置

### 开发模式

```
F:\Projets\CONTER\data\data.json
```

### 打包后

```
可执行文件目录\data\data.json
```

例如：

- 如果应用在：`C:\Apps\CONTER\CONTER.exe`
- 数据文件在：`C:\Apps\CONTER\data\data.json`

## 🎯 优势

| 特性              | 说明                             |
| ----------------- | -------------------------------- |
| ✅ **便携性**     | 应用和数据在同一目录，可整体移动 |
| ✅ **可见性**     | 用户可直接查看和备份数据文件     |
| ✅ **多实例**     | 支持运行多个独立的应用副本       |
| ✅ **无权限问题** | 不需要访问系统目录或用户主目录   |
| ✅ **易于备份**   | 复制整个应用目录即可完整备份     |

## 📝 自动创建

- ✅ 首次运行自动创建 `data` 目录
- ✅ 自动创建空的 `data.json` 文件
- ✅ 无需手动配置

## 💾 数据文件格式

```json
{
  "students": [
    {
      "name": "张三",
      "id": "001",
      "weight": 1.0,
      "picked_count": 5,
      "last_picked": "2025-10-21T14:30:00"
    }
  ],
  "records": [
    {
      "student_name": "张三",
      "timestamp": "2025-10-21T14:30:00",
      "rule_type": "Random Pick"
    }
  ]
}
```

## 🔄 数据管理

### 备份数据

复制 `data` 目录：

```bash
cp -r data data_backup
```

### 恢复数据

替换 `data.json` 文件：

```bash
cp data_backup/data.json data/data.json
```

### 迁移应用

直接复制整个应用目录到新位置。

### 重置数据

删除 `data/data.json`，应用会自动创建空文件。

## 🔧 技术实现

### utils.py

```python
def get_app_data_dir() -> str:
    """获取数据存储目录"""
    if getattr(sys, 'frozen', False):
        # 打包后：可执行文件目录
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发模式：脚本目录
        app_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(app_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_dir
```

### models.py

```python
class DataManager:
    def __init__(self, data_file: str = 'data.json'):
        self.data_file = data_file
        self.students = []
        self.records = []
        self.load_data()
        # 自动创建空文件
        if not os.path.exists(self.data_file):
            self.save_data()
```

## 📚 相关文档

- 详细说明：[DATA_STORAGE.md](DATA_STORAGE.md)
- 开发指南：[DEVELOPMENT.md](DEVELOPMENT.md)
- 用户手册：[USER_GUIDE.md](USER_GUIDE.md)

## ✨ 使用示例

### 运行应用

```bash
# 开发模式
python main.py
# 数据文件：项目目录/data/data.json

# 打包后
.\CONTER.exe
# 数据文件：可执行文件目录/data/data.json
```

### 查看数据

```bash
# Windows
type data\data.json

# Linux/macOS
cat data/data.json
```

### 编程访问

```python
from utils import get_app_data_dir
import os

data_dir = get_app_data_dir()
data_file = os.path.join(data_dir, 'data.json')
print(f"数据文件位置: {data_file}")
```

## ⚠️ 注意事项

1. **权限**：确保应用目录有写入权限
2. **备份**：定期备份 `data` 目录
3. **手动编辑**：不建议在应用运行时手动编辑数据文件
4. **云同步**：可将应用放在云盘目录实现多设备同步

## 🆚 与旧版本对比

| 项目     | 旧版本       | 新版本           |
| -------- | ------------ | ---------------- |
| 存储位置 | `~/.conter/` | `应用目录/data/` |
| 可见性   | 隐藏目录     | 明确子目录       |
| 便携性   | ❌ 分离      | ✅ 集成          |
| 备份     | 需单独备份   | 整体备份         |
| 多实例   | ❌ 共享数据  | ✅ 独立数据      |

---

**功能已完成！** 🎉

现在用户名单和缓存都存储在可执行文件目录的 `data` 子目录中。
