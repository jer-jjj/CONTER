# -*- coding: utf-8 -*-
"""
Reusable UI components
"""
import flet as ft


class StudentCard(ft.Container):
    """Student card component"""
    
    def __init__(self, student, on_delete=None, on_edit=None, i18n=None):
        self.student = student
        self.on_delete_callback = on_delete
        self.on_edit_callback = on_edit
        self.i18n = i18n
        
        id_text = i18n.t('id') if i18n else 'ID'
        weight_text = i18n.t('weight') if i18n else 'Weight'
        picked_text = i18n.t('picked_times', count=student.picked_count) if i18n else f'Picked: {student.picked_count} times'
        edit_tooltip = i18n.t('edit') if i18n else 'Edit'
        delete_tooltip = i18n.t('delete') if i18n else 'Delete'
        
        content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PERSON, color=ft.Colors.PRIMARY),
                ft.Text(student.name, size=18, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    icon_color=ft.Colors.BLUE,
                    on_click=self._on_edit,
                    tooltip=edit_tooltip
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED,
                    on_click=self._on_delete,
                    tooltip=delete_tooltip
                ),
            ]),
            ft.Divider(height=1),
            ft.Row([
                ft.Text(f"{id_text}: {student.id if student.id else 'N/A'}", size=14),
                ft.Container(expand=True),
                ft.Text(f"{weight_text}: {student.weight}", size=14),
            ]),
            ft.Row([
                ft.Text(picked_text, size=14, color=ft.Colors.BLUE_GREY),
            ]),
        ], spacing=10)
        
        super().__init__(
            content=content,
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
            border=ft.border.all(1, ft.Colors.GREY_400),
        )
    
    def _on_delete(self, e):
        if self.on_delete_callback:
            self.on_delete_callback(self.student)
    
    def _on_edit(self, e):
        if self.on_edit_callback:
            self.on_edit_callback(self.student)


class PickResultCard(ft.Container):
    """Pick result card"""
    
    def __init__(self, name: str, animate_in: bool = True):
        content = ft.Column([
            ft.Icon(ft.Icons.EMOJI_EVENTS, size=48, color=ft.Colors.AMBER),
            ft.Text(name, size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        
        super().__init__(
            content=content,
            padding=40,
            border_radius=20,
            bgcolor=ft.Colors.SURFACE,
            alignment=ft.alignment.center,
                animate_scale=500 if animate_in else None,
            animate_opacity=300,
        )
        
        if animate_in:
            self.scale = 0
            self.opacity = 0


class StatisticsPanel(ft.Container):
    """Statistics panel"""
    
    def __init__(self, stats: dict, i18n=None):
        total_label = i18n.t('total') if i18n else 'Total'
        picked_label = i18n.t('picked') if i18n else 'Picked'
        unpicked_label = i18n.t('unpicked') if i18n else 'Unpicked'
        total_picks_label = i18n.t('total_picks') if i18n else 'Total Picks'
        stats_title = i18n.t('statistics') if i18n else 'Statistics'
        
        content = ft.Column([
            ft.Text(stats_title, size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            self._create_stat_row(total_label, str(stats.get('total_students', 0)), ft.Icons.PEOPLE),
            self._create_stat_row(picked_label, str(stats.get('picked_count', 0)), ft.Icons.CHECK_CIRCLE),
            self._create_stat_row(unpicked_label, str(stats.get('unpicked_count', 0)), ft.Icons.RADIO_BUTTON_UNCHECKED),
            self._create_stat_row(total_picks_label, str(stats.get('total_picks', 0)), ft.Icons.NUMBERS),
        ], spacing=15)
        
        super().__init__(
            content=content,
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
            border=ft.border.all(2, ft.Colors.PRIMARY),
        )
    
    def _create_stat_row(self, label: str, value: str, icon):
        return ft.Row([
            ft.Icon(icon, color=ft.Colors.PRIMARY),
            ft.Text(f"{label}:", size=16),
            ft.Container(expand=True),
            ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY),
        ])
