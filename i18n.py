# -*- coding: utf-8 -*-
"""
Internationalization (i18n) support
"""

class Language:
    """Language configuration"""
    
    # English
    EN = {
        'app_title': 'Name Picker',
        'import_excel': 'Import Excel',
        'export_excel': 'Export Excel',
        'add_student': 'Add Student',
        'reset_records': 'Reset Records',
        'clear_all': 'Clear All',
        'pick_settings': 'Pick Settings',
        'pick_rule': 'Pick Rule',
        'count': 'Count',
        'exclude_picked': 'Exclude Picked',
        'start_pick': 'Start Pick',
        'pick_result': 'Pick Result',
        'statistics': 'Statistics',
        'student_list': 'Student List',
        'total': 'Total',
        'picked': 'Picked',
        'unpicked': 'Unpicked',
        'total_picks': 'Total Picks',
        'name': 'Name',
        'id': 'ID',
        'weight': 'Weight',
        'edit': 'Edit',
        'delete': 'Delete',
        'cancel': 'Cancel',
        'save': 'Save',
        'add': 'Add',
        'confirm_delete': 'Confirm Delete',
        'confirm_reset': 'Confirm Reset',
        'warning': 'Warning',
        'delete_student_msg': 'Delete {name}?',
        'reset_records_msg': 'Reset all pick records?',
        'clear_all_msg': 'Clear all student data? This cannot be undone!',
        'name_required': 'Name required',
        'importing': 'Importing...',
        'imported_students': 'Imported {count} students',
        'import_failed': 'Import failed: {error}',
        'export_failed': 'Export failed: {error}',
        'exported_to': 'Exported to: {path}',
        'pick_failed': 'Pick failed: {error}',
        'no_students': 'No students to pick',
        'add_students_first': 'Please add students first',
        'picked_times': 'Picked: {count} times',
        'id_optional': 'ID (optional)',
        'weight_optional': 'Weight',
        'edit_student': 'Edit Student',
        'random_pick': 'Random',
        'weighted_pick': 'Weighted',
        'least_pick': 'Least Picked',
        'language': 'Language',
    }
    
    # Chinese Simplified
    ZH_CN = {
        'app_title': '点名器',
        'import_excel': '导入Excel',
        'export_excel': '导出Excel',
        'add_student': '添加学生',
        'reset_records': '重置记录',
        'clear_all': '清空数据',
        'pick_settings': '抽取设置',
        'pick_rule': '抽取规则',
        'count': '抽取人数',
        'exclude_picked': '排除已抽取',
        'start_pick': '开始点名',
        'pick_result': '抽取结果',
        'statistics': '统计信息',
        'student_list': '学生列表',
        'total': '总人数',
        'picked': '已抽取',
        'unpicked': '未抽取',
        'total_picks': '总抽取次数',
        'name': '姓名',
        'id': '学号',
        'weight': '权重',
        'edit': '编辑',
        'delete': '删除',
        'cancel': '取消',
        'save': '保存',
        'add': '添加',
        'confirm_delete': '确认删除',
        'confirm_reset': '确认重置',
        'warning': '⚠️ 警告',
        'delete_student_msg': '确定要删除 {name} 吗？',
        'reset_records_msg': '确定要重置所有抽取记录吗？',
        'clear_all_msg': '确定要清空所有学生数据吗？此操作不可恢复！',
        'name_required': '请输入姓名',
        'importing': '正在导入...',
        'imported_students': '成功导入 {count} 名学生',
        'import_failed': '导入失败: {error}',
        'export_failed': '导出失败: {error}',
        'exported_to': '导出成功: {path}',
        'pick_failed': '抽取失败: {error}',
        'no_students': '没有可抽取的学生',
        'add_students_first': '请先添加学生',
        'picked_times': '被抽取: {count}次',
        'id_optional': '学号（可选）',
        'weight_optional': '权重',
        'edit_student': '编辑学生',
        'random_pick': '随机抽取',
        'weighted_pick': '权重抽取',
        'least_pick': '最少抽取',
        'language': '语言',
    }
    
    # French
    FR = {
        'app_title': 'Sélecteur de Noms',
        'import_excel': 'Importer Excel',
        'export_excel': 'Exporter Excel',
        'add_student': 'Ajouter Étudiant',
        'reset_records': 'Réinitialiser',
        'clear_all': 'Tout Effacer',
        'pick_settings': 'Paramètres',
        'pick_rule': 'Règle',
        'count': 'Nombre',
        'exclude_picked': 'Exclure Sélectionnés',
        'start_pick': 'Commencer',
        'pick_result': 'Résultat',
        'statistics': 'Statistiques',
        'student_list': 'Liste des Étudiants',
        'total': 'Total',
        'picked': 'Sélectionnés',
        'unpicked': 'Non Sélectionnés',
        'total_picks': 'Total Sélections',
        'name': 'Nom',
        'id': 'ID',
        'weight': 'Poids',
        'edit': 'Modifier',
        'delete': 'Supprimer',
        'cancel': 'Annuler',
        'save': 'Enregistrer',
        'add': 'Ajouter',
        'confirm_delete': 'Confirmer Suppression',
        'confirm_reset': 'Confirmer Réinitialisation',
        'warning': 'Attention',
        'delete_student_msg': 'Supprimer {name}?',
        'reset_records_msg': 'Réinitialiser tous les enregistrements?',
        'clear_all_msg': 'Effacer toutes les données? Cette action est irréversible!',
        'name_required': 'Nom requis',
        'importing': 'Importation...',
        'imported_students': '{count} étudiants importés',
        'import_failed': 'Échec importation: {error}',
        'export_failed': 'Échec exportation: {error}',
        'exported_to': 'Exporté vers: {path}',
        'pick_failed': 'Échec sélection: {error}',
        'no_students': 'Aucun étudiant à sélectionner',
        'add_students_first': 'Veuillez ajouter des étudiants',
        'picked_times': 'Sélectionné: {count} fois',
        'id_optional': 'ID (optionnel)',
        'weight_optional': 'Poids',
        'edit_student': 'Modifier Étudiant',
        'random_pick': 'Aléatoire',
        'weighted_pick': 'Pondéré',
        'least_pick': 'Moins Sélectionné',
        'language': 'Langue',
    }


class I18n:
    """Internationalization manager"""
    
    def __init__(self, lang_code='zh_CN'):
        self.current_lang = lang_code
        self.translations = {
            'en': Language.EN,
            'zh_CN': Language.ZH_CN,
            'fr': Language.FR,
        }
    
    def set_language(self, lang_code):
        """Set current language"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False
    
    def t(self, key, **kwargs):
        """Translate key with optional parameters"""
        lang_dict = self.translations.get(self.current_lang, Language.EN)
        text = lang_dict.get(key, key)
        
        # Replace placeholders
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text
    
    def get_available_languages(self):
        """Get list of available languages"""
        return [
            ('en', 'English'),
            ('zh_CN', '中文'),
            ('fr', 'Français'),
        ]
