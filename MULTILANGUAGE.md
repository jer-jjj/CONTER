# 多语言支持说明 / Multi-language Support

## 概述 / Overview

点名器应用现在支持多语言界面，可以在中文、英文和法文之间切换。

The Name Picker application now supports multiple language interfaces, allowing switching between Chinese, English, and French.

## 支持的语言 / Supported Languages

1. **中文 (Chinese Simplified)** - zh_CN
2. **English** - en
3. **Français (French)** - fr

## 如何切换语言 / How to Switch Language

### 方法 1：在应用界面切换 / Method 1: Switch in App Interface

1. 启动应用 / Launch the application
2. 在顶部工具栏找到"语言"下拉菜单 / Find the "Language" dropdown menu in the top toolbar
3. 选择您想要的语言 / Select your desired language
4. 界面会立即切换到所选语言 / The interface will immediately switch to the selected language

### 方法 2：修改代码默认语言 / Method 2: Modify Default Language in Code

在 `main.py` 文件中，找到以下行：

In the `main.py` file, find the following line:

```python
i18n = I18n('zh_CN')  # Default language: Chinese
```

可以将其修改为：

You can modify it to:

```python
i18n = I18n('en')  # English
# or
i18n = I18n('fr')  # French
```

## 功能说明 / Features

### 已翻译的界面元素 / Translated UI Elements

- 应用标题 / Application title
- 所有按钮标签 / All button labels
- 菜单选项 / Menu options
- 对话框标题和内容 / Dialog titles and content
- 输入框标签 / Input field labels
- 错误和成功消息 / Error and success messages
- 统计信息标签 / Statistics labels
- 学生卡片信息 / Student card information

### 动态语言切换 / Dynamic Language Switching

- ✅ 无需重启应用 / No application restart required
- ✅ 即时更新所有界面文本 / Instant update of all interface text
- ✅ 保持当前数据状态 / Maintains current data state
- ✅ 重建整个 UI 以反映新语言 / Rebuilds entire UI to reflect new language

## 技术实现 / Technical Implementation

### i18n 模块 / i18n Module

应用使用自定义的 `i18n.py` 模块实现国际化支持：

The application uses a custom `i18n.py` module for internationalization support:

```python
from i18n import I18n

# Initialize with default language
i18n = I18n('zh_CN')

# Translate a key
text = i18n.t('app_title')

# Translate with parameters
text = i18n.t('imported_students', count=10)
# Result: "成功导入 10 名学生" (Chinese)
# Result: "Imported 10 students" (English)
```

### 翻译键 / Translation Keys

所有翻译文本都通过键值对存储：

All translation texts are stored as key-value pairs:

| Key         | 中文     | English     | Français          |
| ----------- | -------- | ----------- | ----------------- |
| app_title   | 点名器   | Name Picker | Sélecteur de Noms |
| add_student | 添加学生 | Add Student | Ajouter Étudiant  |
| start_pick  | 开始点名 | Start Pick  | Commencer         |
| ...         | ...      | ...         | ...               |

## 添加新语言 / Adding New Languages

如果您想添加新的语言支持：

If you want to add new language support:

### 步骤 / Steps

1. **打开 `i18n.py` 文件** / Open `i18n.py` file

2. **添加新语言字典** / Add new language dictionary

```python
# Example: Spanish
ES = {
    'app_title': 'Selector de Nombres',
    'import_excel': 'Importar Excel',
    # ... add all keys
}
```

3. **在 I18n 类中注册** / Register in I18n class

```python
def __init__(self, lang_code='zh_CN'):
    self.translations = {
        'en': Language.EN,
        'zh_CN': Language.ZH_CN,
        'fr': Language.FR,
        'es': Language.ES,  # Add new language
    }
```

4. **更新语言选择器** / Update language selector

在 `ui/main_view.py` 中：

In `ui/main_view.py`:

```python
self.language_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("zh_CN", "中文"),
        ft.dropdown.Option("en", "English"),
        ft.dropdown.Option("fr", "Français"),
        ft.dropdown.Option("es", "Español"),  # Add new option
    ],
    # ...
)
```

## 翻译质量 / Translation Quality

### 当前状态 / Current Status

- ✅ 中文：原生语言，完全准确 / Chinese: Native language, fully accurate
- ✅ 英文：专业翻译 / English: Professional translation
- ✅ 法文：标准翻译 / French: Standard translation

### 改进建议 / Improvement Suggestions

如果您发现翻译不当或有更好的建议，请：

If you find inappropriate translations or have better suggestions:

1. 打开 `i18n.py` 文件 / Open `i18n.py` file
2. 修改相应的翻译文本 / Modify the corresponding translation text
3. 保存并重启应用 / Save and restart the application

## 示例用法 / Example Usage

### 中文界面 / Chinese Interface

- 点击"导入 Excel" / Click "导入 Excel"
- 选择"添加学生" / Select "添加学生"
- 使用"随机抽取"规则 / Use "随机抽取" rule

### English Interface

- Click "Import Excel"
- Select "Add Student"
- Use "Random" rule

### Interface Française

- Cliquer "Importer Excel"
- Sélectionner "Ajouter Étudiant"
- Utiliser règle "Aléatoire"

## 常见问题 / FAQ

### Q: 切换语言后数据会丢失吗？

A: 不会。数据完全保留，只是界面语言改变。

### Q: Will data be lost after switching languages?

A: No. Data is fully preserved, only the interface language changes.

### Q: Les données seront-elles perdues après le changement de langue?

A: Non. Les données sont entièrement préservées, seule la langue de l'interface change.

---

### Q: 可以添加更多语言吗？

A: 可以！按照上面的步骤添加新语言支持。

### Q: Can more languages be added?

A: Yes! Follow the steps above to add new language support.

### Q: Peut-on ajouter plus de langues?

A: Oui! Suivez les étapes ci-dessus pour ajouter le support de nouvelles langues.

---

### Q: 默认语言是什么？

A: 默认是中文（zh_CN），可以在代码中修改。

### Q: What is the default language?

A: Default is Chinese (zh_CN), can be modified in code.

### Q: Quelle est la langue par défaut?

A: Le défaut est le chinois (zh_CN), peut être modifié dans le code.

## 技术支持 / Technical Support

如有问题或建议，欢迎反馈！

For questions or suggestions, feedback is welcome!

Pour toute question ou suggestion, les commentaires sont les bienvenus!

---

**享受多语言的便利！ / Enjoy multilingual convenience! / Profitez de la commodité multilingue!** 🌍
