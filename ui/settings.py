from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.metrics import dp
from kivymd.app import MDApp

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Settings title
        self.title_label = Label(
            text="Settings",
            font_size=36,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(60),
            halign='center',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        layout.add_widget(self.title_label)

        # Theme selection
        theme_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=[dp(20), 0, dp(20), 0],
            spacing=dp(10)
        )
        theme_label = Label(text="Theme:", size_hint_x=None, width=dp(80))
        self.theme_button = MDButton(
            MDButtonText(text="Gray"),
            size_hint=(None, None),
            size=(dp(120), dp(35)),
            pos_hint={'center_y': 0.5},
            on_release=self.open_theme_menu
        )
        theme_layout.add_widget(theme_label)
        theme_layout.add_widget(self.theme_button)
        layout.add_widget(theme_layout)

        # Theme menu
        themes = ["Gray", "Blue", "Green", "Red", "Purple"]
        self.theme_menu = MDDropdownMenu(
            caller=self.theme_button,
            items=[{"text": theme, "on_release": lambda x=theme: self.set_theme(x)} for theme in themes],
            width_mult=4,
            max_height=dp(200)
        )

        # Font size slider
        font_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100))
        font_label = Label(text="Font Size:", size_hint_y=None, height=dp(30))
        self.font_slider = Slider(min=10, max=30, value=16, step=1, size_hint_y=None, height=dp(50))
        self.font_slider.bind(value=self.update_font_size)
        font_layout.add_widget(font_label)
        font_layout.add_widget(self.font_slider)
        layout.add_widget(font_layout)

        # Back button
        back_btn = MDButton(
            MDButtonText(text="Back"),
            style="elevated",
            md_bg_color="#FF6F61",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def open_theme_menu(self, instance):
        self.theme_menu.open()

    def set_theme(self, theme):
        self.theme_button.children[0].text = theme
        app = MDApp.get_running_app()
        app.theme_cls.primary_palette = theme
        app.theme_cls.primary_hue = "500"
        # Update all widgets to reflect theme
        for screen in app.root.screens:
            for widget in screen.walk():
                if hasattr(widget, 'md_bg_color') and widget.md_bg_color != [1, 0, 0, 1]:  # Exclude custom colors
                    widget.md_bg_color = app.theme_cls.primary_color
        self.theme_menu.dismiss()

    def update_font_size(self, instance, value):
        app = MDApp.get_running_app()
        for screen in app.root.screens:
            for widget in screen.walk():
                if hasattr(widget, 'font_size'):
                    widget.font_size = value

    def go_back(self, instance):
        self.manager.current = 'main'