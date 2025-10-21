# -*- coding: utf-8 -*-
"""
Name Picker - Main Program
Multi-platform name picker application based on Flet framework
"""
import flet as ft
from models import DataManager
from ui.main_view import MainView
from i18n import I18n
import os
from utils import get_app_data_dir


def main(page: ft.Page):
    """Main entry point"""
    # Initialize i18n
    i18n = I18n('zh_CN')  # Default language: Chinese
    
    # Configure page
    page.title = i18n.t('app_title')
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1400
    page.window.height = 900
    page.window.min_width = 1000
    page.window.min_height = 700
    
    # Register fonts (MiSans for Chinese & English)
    # Place font files under assets/fonts/
    # If font files are missing, Flet will fallback to default fonts silently.
    page.fonts = {
        # Use only regular to keep mapping simple; bold is emulated by weight
        "MiSans": "fonts/MiSans-Regular.ttf",
    }
    
    # Set theme
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        use_material3=True,
        font_family="MiSans",
    )
    
    # Initialize data manager
    data_file = os.path.join(get_app_data_dir(), 'data.json')
    data_manager = DataManager(data_file)
    
    # Create main view
    main_view = MainView(page, data_manager, i18n)
    
    # Add to page
    page.add(main_view.build())


if __name__ == "__main__":
    # Run application
    ft.app(target=main, assets_dir="assets")
