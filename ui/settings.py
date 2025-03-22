from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.uix.switch import Switch
from kivy.metrics import dp

class SettingsScreen(Screen):
    def __init__(self, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        layout.add_widget(MDLabel(text="Settings", theme_text_color="Primary", font_size=dp(20)))
        
        theme_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        theme_layout.add_widget(MDLabel(text="Dark Mode"))
        self.theme_switch = Switch(active=False)
        self.theme_switch.bind(active=self.toggle_theme)
        theme_layout.add_widget(self.theme_switch)
        layout.add_widget(theme_layout)
        
        sync_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        sync_layout.add_widget(MDLabel(text="Sync with Google Drive"))
        self.sync_switch = Switch(active=False)
        self.sync_switch.bind(active=self.toggle_sync)
        sync_layout.add_widget(self.sync_switch)
        layout.add_widget(sync_layout)
        
        back_btn = MDButton(
            MDButtonText(text="Back"),
            style="elevated",
            md_bg_color='#FF6F61',
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def toggle_theme(self, instance, value):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = "Dark" if value else "Light"
    
    def toggle_sync(self, instance, value):
        if self.main_screen:
            self.main_screen.sync_enabled = value
            if value and not self.main_screen.drive:
                self.main_screen.setup_drive()
            elif not value and self.main_screen.drive:
                self.main_screen.drive = None  # Clear drive when disabled
    
    def go_back(self, instance):
        self.manager.current = 'main'