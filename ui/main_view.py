# -*- coding: utf-8 -*-
"""
Main view
"""
import flet as ft
import asyncio
from typing import List
from models import Student, DataManager
from services import PickerService, ExcelService, StatisticsService
from ui.components import StudentCard, PickResultCard, StatisticsPanel
import os
import random


class MainView:
    """Main view"""
    
    def __init__(self, page: ft.Page, data_manager: DataManager, i18n):
        self.page = page
        self.data_manager = data_manager
        self.i18n = i18n
        self.picker_service = PickerService(data_manager)
        self.is_picking = False
        
        self.students_grid = ft.GridView(
            expand=True,
            runs_count=3,
            spacing=10,
            run_spacing=10,
            child_aspect_ratio=2.5,
        )
        
        self.result_container = ft.Container(
            height=300,
            alignment=ft.alignment.center,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
        )
        
        self.stats_panel = ft.Container()
        
        self.rule_dropdown = ft.Dropdown(
            label=self.i18n.t('pick_rule'),
            options=[
                ft.dropdown.Option("random", self.i18n.t('random_pick')),
                ft.dropdown.Option("weighted", self.i18n.t('weighted_pick')),
                ft.dropdown.Option("least", self.i18n.t('least_pick')),
            ],
            value="random",
            width=200,
        )
        
        self.count_field = ft.TextField(
            label=self.i18n.t('count'),
            value="1",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.exclude_picked_checkbox = ft.Checkbox(
            label=self.i18n.t('exclude_picked'),
            value=False,
        )
        
        # Language selector
        self.language_dropdown = ft.Dropdown(
            label=self.i18n.t('language'),
            options=[
                ft.dropdown.Option("zh_CN", "中文"),
                ft.dropdown.Option("en", "English"),
                ft.dropdown.Option("fr", "Français"),
            ],
            value="zh_CN",
            width=150,
            on_change=self._on_language_change,
        )
        
        self.file_picker = ft.FilePicker(on_result=self._on_file_picked)
        self.page.overlay.append(self.file_picker)
        
    def build(self):
        """Build UI"""
        toolbar = ft.Row([
            ft.Text(self.i18n.t('app_title'), size=28, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            self.language_dropdown,
            ft.ElevatedButton(self.i18n.t('import_excel'), icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["xlsx", "xls"])),
            ft.ElevatedButton(self.i18n.t('export_excel'), icon=ft.Icons.DOWNLOAD, on_click=self._export_excel),
            ft.ElevatedButton(self.i18n.t('add_student'), icon=ft.Icons.PERSON_ADD, on_click=self._show_add_dialog),
            ft.ElevatedButton(self.i18n.t('reset_records'), icon=ft.Icons.REFRESH, on_click=self._reset_records, bgcolor=ft.Colors.ORANGE),
            ft.IconButton(icon=ft.Icons.DELETE_FOREVER, icon_color=ft.Colors.RED, tooltip=self.i18n.t('clear_all'), on_click=self._clear_all),
        ], spacing=10)
        
        pick_controls = ft.Container(
            content=ft.Column([
                ft.Text(self.i18n.t('pick_settings'), size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.rule_dropdown,
                    self.count_field,
                    self.exclude_picked_checkbox,
                    ft.Container(expand=True),
                    ft.ElevatedButton(self.i18n.t('start_pick'), icon=ft.Icons.PLAY_ARROW, on_click=self._start_picking,
                        bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE, height=50, width=150),
                ], spacing=20),
            ], spacing=10),
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
        )
        
        result_section = ft.Container(
            content=ft.Column([
                ft.Text(self.i18n.t('pick_result'), size=20, weight=ft.FontWeight.BOLD),
                self.result_container,
            ], spacing=10),
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
        )
        
        students_section = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(self.i18n.t('student_list'), size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text(f"{self.i18n.t('total')} {len(self.data_manager.students)}", size=16, color=ft.Colors.BLUE_GREY),
                ]),
                ft.Divider(),
                ft.Container(content=self.students_grid, height=400),
            ], spacing=10),
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
            expand=True,
        )
        
        main_layout = ft.Column([
            toolbar,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Row([
                ft.Column([pick_controls, ft.Container(height=20), result_section], expand=2),
                ft.Container(width=20),
                ft.Column([self.stats_panel], expand=1),
            ], expand=True),
            ft.Container(height=20),
            students_section,
        ], spacing=0, expand=True)
        
        self._refresh_students_list()
        self._refresh_statistics()
        
        return ft.Container(content=main_layout, padding=20, expand=True)
    
    def _on_language_change(self, e):
        """Handle language change"""
        self.i18n.set_language(e.control.value)
        self.page.title = self.i18n.t('app_title')
        # Rebuild the entire UI with new language
        self.page.clean()
        self.page.add(self.build())
        self.page.update()
    
    def _refresh_students_list(self):
        """Refresh student list"""
        self.students_grid.controls.clear()
        for student in self.data_manager.students:
            card = StudentCard(student, on_delete=self._delete_student, on_edit=self._edit_student, i18n=self.i18n)
            self.students_grid.controls.append(card)
        self.page.update()
    
    def _refresh_statistics(self):
        """Refresh statistics"""
        stats = StatisticsService.get_statistics(self.data_manager)
        self.stats_panel.content = StatisticsPanel(stats, i18n=self.i18n)
        self.page.update()
    
    def _on_file_picked(self, e: ft.FilePickerResultEvent):
        """File picker callback"""
        if e.files:
            # Use page.run_task to run async function
            self.page.run_task(self._import_excel_async, e.files[0].path)
    
    async def _import_excel_async(self, file_path):
        """Import Excel file asynchronously"""
        try:
            loading = ft.Column([
                ft.ProgressRing(),
                ft.Text(self.i18n.t('importing'), size=18),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            self.result_container.content = loading
            self.page.update()
            
            students = await ExcelService.import_from_excel(file_path)
            for student in students:
                if not self.data_manager.get_student(student.name):
                    self.data_manager.add_student(student)
            
            self._refresh_students_list()
            self._refresh_statistics()
            
            self.result_container.content = ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=80, color=ft.Colors.GREEN),
                ft.Text(self.i18n.t('imported_students', count=len(students)), size=24),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            self.page.update()
            
            await asyncio.sleep(3)
            self.result_container.content = None
            self.page.update()
        except Exception as ex:
            self._show_error(self.i18n.t('import_failed', error=str(ex)))
    
    def _export_excel(self, e):
        """Export to Excel"""
        self.page.run_task(self._export_excel_async)
    
    async def _export_excel_async(self):
        """Export Excel file asynchronously"""
        try:
            file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'students.xlsx')
            await ExcelService.export_to_excel(self.data_manager.students, file_path)
            self._show_success(self.i18n.t('exported_to', path=file_path))
        except Exception as ex:
            self._show_error(self.i18n.t('export_failed', error=str(ex)))
    
    def _show_add_dialog(self, e):
        """Show add student dialog"""
        name_field = ft.TextField(label=self.i18n.t('name'), autofocus=True)
        id_field = ft.TextField(label=self.i18n.t('id_optional'))
        weight_field = ft.TextField(label=self.i18n.t('weight_optional'), value="1.0", keyboard_type=ft.KeyboardType.NUMBER)
        
        def add_student():
            if not name_field.value:
                name_field.error_text = self.i18n.t('name_required')
                self.page.update()
                return
            
            try:
                weight = float(weight_field.value) if weight_field.value else 1.0
                if weight <= 0:
                    weight = 1.0
            except:
                weight = 1.0
            
            student = Student(name=name_field.value, id=id_field.value if id_field.value else None, weight=weight)
            self.data_manager.add_student(student)
            self._refresh_students_list()
            self._refresh_statistics()
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.i18n.t('add_student')),
            content=ft.Column([name_field, id_field, weight_field], tight=True, spacing=20),
            actions=[
                ft.TextButton(self.i18n.t('cancel'), on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(self.i18n.t('add'), on_click=lambda _: add_student()),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _delete_student(self, student: Student):
        """Delete student"""
        def confirm():
            self.data_manager.remove_student(student.name)
            self._refresh_students_list()
            self._refresh_statistics()
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.i18n.t('confirm_delete')),
            content=ft.Text(self.i18n.t('delete_student_msg', name=student.name)),
            actions=[
                ft.TextButton(self.i18n.t('cancel'), on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(self.i18n.t('delete'), on_click=lambda _: confirm(), bgcolor=ft.Colors.RED),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _edit_student(self, student: Student):
        """Edit student"""
        name_field = ft.TextField(label=self.i18n.t('name'), value=student.name)
        id_field = ft.TextField(label=self.i18n.t('id'), value=student.id if student.id else "")
        weight_field = ft.TextField(label=self.i18n.t('weight'), value=str(student.weight))
        
        def save():
            if not name_field.value:
                return
            
            try:
                weight = float(weight_field.value) if weight_field.value else 1.0
            except:
                weight = 1.0
            
            if name_field.value != student.name:
                self.data_manager.remove_student(student.name)
                new_student = Student(name=name_field.value, id=id_field.value if id_field.value else None,
                    weight=weight, picked_count=student.picked_count, last_picked=student.last_picked)
                self.data_manager.add_student(new_student)
            else:
                self.data_manager.update_student(student.name, id=id_field.value if id_field.value else None, weight=weight)
            
            self._refresh_students_list()
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.i18n.t('edit_student')),
            content=ft.Column([name_field, id_field, weight_field], tight=True, spacing=20),
            actions=[
                ft.TextButton(self.i18n.t('cancel'), on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(self.i18n.t('save'), on_click=lambda _: save()),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _start_picking(self, e):
        """Start picking"""
        if self.is_picking:
            return
        
        if not self.data_manager.students:
            self._show_error(self.i18n.t('add_students_first'))
            return
        
        # Use page.run_task to run async function
        self.page.run_task(self._pick_async)
    
    async def _pick_async(self):
        """Pick students asynchronously"""
        self.is_picking = True
        
        try:
            count = int(self.count_field.value) if self.count_field.value else 1
            rule = self.rule_dropdown.value
            exclude_picked = self.exclude_picked_checkbox.value
            
            animation_text = ft.Text("???", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, animate_opacity=300)
            self.result_container.content = ft.Column([
                 ft.Icon(ft.Icons.SHUFFLE, size=80, color=ft.Colors.BLUE, animate_rotation=1000),
                animation_text,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            self.page.update()
            
            # Animation
            for i in range(20):
                random_student = random.choice(self.data_manager.students)
                animation_text.value = random_student.name
                self.page.update()
                await asyncio.sleep(0.1)
            
            # Pick
            if rule == "random":
                picked = await self.picker_service.pick_random(count, exclude_picked)
            elif rule == "weighted":
                picked = await self.picker_service.pick_weighted(count)
            else:
                picked = await self.picker_service.pick_least_picked(count)
            
            if not picked:
                self._show_error(self.i18n.t('no_students'))
                self.is_picking = False
                return
            
            # Show result
            result_cards = [PickResultCard(student.name, animate_in=True) for student in picked]
            
            if len(result_cards) == 1:
                self.result_container.content = result_cards[0]
            else:
                self.result_container.content = ft.Row(
                    result_cards,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                )
            
            self.page.update()
            
            await asyncio.sleep(0.1)
            for card in result_cards:
                card.scale = 1
                card.opacity = 1
            self.page.update()
            
            self._refresh_students_list()
            self._refresh_statistics()
            
        except Exception as ex:
            self._show_error(self.i18n.t('pick_failed', error=str(ex)))
        finally:
            self.is_picking = False
    
    def _reset_records(self, e):
        """Reset records"""
        def confirm():
            self.data_manager.reset_pick_counts()
            self._refresh_students_list()
            self._refresh_statistics()
            dialog.open = False
            self.result_container.content = None
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.i18n.t('confirm_reset')),
            content=ft.Text(self.i18n.t('reset_records_msg')),
            actions=[
                ft.TextButton(self.i18n.t('cancel'), on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(self.i18n.t('reset_records'), on_click=lambda _: confirm(), bgcolor=ft.Colors.ORANGE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _clear_all(self, e):
        """Clear all data"""
        def confirm():
            self.data_manager.clear_all_students()
            self._refresh_students_list()
            self._refresh_statistics()
            dialog.open = False
            self.result_container.content = None
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(self.i18n.t('warning')),
            content=ft.Text(self.i18n.t('clear_all_msg')),
            actions=[
                ft.TextButton(self.i18n.t('cancel'), on_click=lambda _: self._close_dialog(dialog)),
                ft.ElevatedButton(self.i18n.t('clear_all'), on_click=lambda _: confirm(), bgcolor=ft.Colors.RED),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _close_dialog(self, dialog):
        """Close dialog"""
        dialog.open = False
        self.page.update()
    
    def _show_error(self, message: str):
        """Show error message"""
        self.result_container.content = ft.Column([
            ft.Icon(ft.Icons.ERROR, size=80, color=ft.Colors.RED),
            ft.Text(message, size=20, color=ft.Colors.RED),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        self.page.update()
    
    def _show_success(self, message: str):
        """Show success message"""
        snack = ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.GREEN)
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()
