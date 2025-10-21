# 数据存储说明

## 存储位置

### 开发模式（运行 Python 脚本）

数据文件存储在：

```
项目根目录/data/data.json
```

例如：

```
F:\Projets\CONTER\data\data.json
```

### 打包后（可执行文件）

数据文件存储在：

```
可执行文件所在目录/data/data.json
```

例如，如果可执行文件在：

```
C:\Program Files\CONTER\CONTER.exe
```

则数据文件在：

```
C:\Program Files\CONTER\data\data.json
```

## 优势

✅ **便携性**：所有数据与应用在同一目录，方便整体移动或备份
✅ **多用户隔离**：不同用户可以有独立的应用副本和数据
✅ **无需管理员权限**：不需要访问系统目录或用户主目录
✅ **数据可见**：用户可以直接访问和备份数据文件

## 数据文件结构

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

## 数据管理

### 备份数据

```bash
# 复制 data 目录即可
cp -r data data_backup_20251021
```

### 恢复数据

```bash
# 替换 data 目录
cp data_backup_20251021/data.json data/data.json
```

### 迁移数据

直接复制整个应用目录（包含 data 子目录）到新位置即可。

### 重置数据

删除 `data/data.json` 文件，应用会自动创建新的空数据文件。

## 自动创建

- 应用首次运行时会自动创建 `data` 目录
- 如果 `data.json` 不存在，会自动创建空的数据文件
- 无需手动创建任何目录或文件

## 权限说明

### Windows

- 如果应用安装在 `C:\Program Files\` 下，写入数据可能需要管理员权限
- 建议安装在用户目录下（如 `C:\Users\用户名\AppData\Local\CONTER\`）

### macOS/Linux

- 确保应用目录有写入权限
- 建议权限设置：`chmod 755 应用目录`

## 技术实现

```python
# utils.py 中的实现
def get_app_data_dir() -> str:
    """获取数据存储目录"""
    # 判断是否为打包后的可执行文件
    if getattr(sys, 'frozen', False):
        # 打包后：使用可执行文件所在目录
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发模式：使用脚本所在目录
        app_dir = os.path.dirname(os.path.abspath(__file__))

    # 在应用目录下创建 data 子目录
    data_dir = os.path.join(app_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return data_dir
```

## 常见问题

### Q: 为什么不使用用户主目录（如 ~/.conter）？

A:

- 便携性：应用和数据在一起，方便移动
- 可见性：用户可以直接看到和管理数据
- 多实例：可以运行多个独立的应用副本

### Q: 数据会丢失吗？

A:

- 只要不删除应用目录，数据就会保留
- 建议定期备份 `data` 目录
- 可以通过 Excel 导出功能备份学生名单

### Q: 可以更改数据存储位置吗？

A:
可以，修改 `utils.py` 中的 `get_app_data_dir()` 函数：

```python
def get_app_data_dir() -> str:
    # 自定义路径
    data_dir = r"D:\MyData\CONTER"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir
```

### Q: 如何在多台电脑间同步数据？

A:

1. 将应用安装在云盘同步目录（如 OneDrive、百度网盘）
2. 或者定期复制 `data` 目录
3. 或者使用 Excel 导入/导出功能

## 安全建议

- ✅ 定期备份 `data` 目录
- ✅ 不要在应用运行时手动编辑 `data.json`
- ✅ 使用应用内的导入/导出功能管理数据
- ⚠️ 数据文件包含明文信息，注意访问权限
