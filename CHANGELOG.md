# 更新日志 (Changelog)

## v2.0.0 - 2025-10-21

### 🌍 新功能 (New Features)

#### 多语言支持 (Multi-language Support)

- ✅ 添加了完整的国际化（i18n）支持
- ✅ 支持三种语言：
  - 🇨🇳 中文（简体）- Chinese Simplified
  - 🇬🇧 英语 - English
  - 🇫🇷 法语 - Français
- ✅ 在应用顶部工具栏添加语言选择器
- ✅ 支持实时语言切换，无需重启应用
- ✅ 所有 UI 元素都已翻译（按钮、标签、对话框、消息等）
- ✅ 创建了独立的 `i18n.py` 模块管理翻译
- ✅ 易于扩展支持更多语言

### 🐛 Bug 修复 (Bug Fixes)

#### 异步编程问题

- ✅ 修复了点名失败的 bug
- ✅ 将 `main()` 函数从 `async def` 改为普通 `def`
- ✅ 使用 `page.run_task()` 正确处理异步函数调用
- ✅ 修复了 `_on_file_picked` 的异步问题
- ✅ 修复了 `_export_excel` 的异步问题
- ✅ 修复了 `_start_picking` 的异步问题
- ✅ 所有异步操作现在都能正常工作

#### 颜色常量问题

- ✅ 修复了 Flet 颜色 API 的使用问题
- ✅ 将 `ft.Colors.SURFACE_VARIANT` 改为 `ft.Colors.SURFACE`
- ✅ 将 `ft.Colors.ON_PRIMARY` 改为 `ft.Colors.WHITE`
- ✅ 将 `ft.Colors.SECONDARY` 改为 `ft.Colors.BLUE_GREY`
- ✅ 所有颜色现在都正确显示

### ⚡ 性能优化 (Performance Improvements)

- ✅ 优化了 UI 刷新逻辑
- ✅ 改进了异步任务的执行方式
- ✅ 减少了不必要的页面更新
- ✅ 提高了语言切换的速度

### 📝 文档更新 (Documentation Updates)

- ✅ 创建了 `MULTILANGUAGE.md` - 多语言支持详细说明
- ✅ 更新了 `README.md` - 添加多语言功能介绍
- ✅ 创建了 `CHANGELOG.md` - 版本更新日志（本文件）
- ✅ 所有文档都包含中英文说明

### 🔧 技术改进 (Technical Improvements)

#### 代码结构

- ✅ 添加了 `i18n.py` 模块
- ✅ 更新了 `main.py` 以支持 i18n
- ✅ 重构了 `ui/main_view.py` 的多个方法
- ✅ 更新了 `ui/components.py` 以接受 i18n 参数

#### 异步编程

- ✅ 创建了独立的异步方法：
  - `_import_excel_async()`
  - `_export_excel_async()`
  - `_pick_async()`
- ✅ 使用 `page.run_task()` 正确调度异步任务
- ✅ 改进了错误处理

### 📦 依赖更新 (Dependencies)

无变化，仍然使用：

- flet >= 0.24.0
- openpyxl >= 3.1.2
- pandas >= 2.0.0

---

## v1.0.0 - 2025-10-21 (Initial Release)

### ✨ 初始功能 (Initial Features)

- ✅ Excel 导入导出功能
- ✅ 多样化抽取规则（随机、权重、最少抽取）
- ✅ 学生信息管理（增删改查）
- ✅ 数据持久化（JSON 存储）
- ✅ 统计信息面板
- ✅ 动画效果
- ✅ Material Design 3 界面
- ✅ 跨平台支持

---

## 升级指南 (Upgrade Guide)

### 从 v1.0 升级到 v2.0

1. **备份数据**：

   ```bash
   # Windows
   copy %USERPROFILE%\.conter\data.json data_backup.json

   # macOS/Linux
   cp ~/.conter/data.json data_backup.json
   ```

2. **更新代码**：

   - 下载最新版本的代码
   - 确保所有文件都已更新

3. **无需额外操作**：

   - 数据格式完全兼容
   - 应用会自动使用现有数据
   - 默认语言为中文

4. **开始使用新功能**：
   - 启动应用
   - 在顶部工具栏选择您喜欢的语言
   - 享受改进后的体验！

---

## 已知问题 (Known Issues)

### v2.0.0

- 无已知问题

如发现任何问题，请及时反馈！

---

## 未来计划 (Future Plans)

### v2.1.0 (计划中)

- [ ] 添加更多语言（西班牙语、德语、日语）
- [ ] 深色模式支持
- [ ] 自定义主题颜色
- [ ] 历史记录查看界面

### v3.0.0 (规划中)

- [ ] 云端数据同步
- [ ] 多用户支持
- [ ] 移动端优化
- [ ] PDF 报告导出
- [ ] 语音播报功能

---

**感谢使用点名器！** 🎉  
**Thank you for using Name Picker!** 🎉  
**Merci d'utiliser le Sélecteur de Noms!** 🎉
