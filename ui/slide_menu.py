import threading
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivy.metrics import dp
from kivy.properties import ObjectProperty

class SlideMenu(BoxLayout):
    main_screen = ObjectProperty(None)
    
    def __init__(self, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.orientation = 'vertical'
        self.size_hint_x = 0.7
        self.pos_hint = {'x': -0.7}
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # Note Actions
        self.add_widget(MDButton(
            MDButtonIcon(icon="image"),
            MDButtonText(text="Add Image"),
            style="elevated",
            md_bg_color='#92A8D1',
            on_release=self.main_screen.add_image
        ))
        self.add_widget(MDButton(
            MDButtonIcon(icon="clock"),
            MDButtonText(text="Set Reminder"),
            style="elevated",
            md_bg_color='#92A8D1',
            on_release=self.main_screen.set_reminder
        ))
        
        # Sync Option
        self.add_widget(MDButton(
            MDButtonIcon(icon="cloud-sync"),
            MDButtonText(text="Force Drive Sync"),
            style="elevated",
            md_bg_color='#3498DB',
            on_release=self.force_sync
        ))
        
        # View Options
        self.add_widget(MDButton(
            MDButtonIcon(icon="view-list"),
            MDButtonText(text="Sort by Date"),
            style="elevated",
            md_bg_color='#2980B9',
            on_release=lambda x: self.main_screen.load_notes()
        ))
    
    def force_sync(self, instance):
        if self.main_screen and self.main_screen.drive and self.main_screen.sync_enabled:
            for key in self.main_screen.storage.store:
                threading.Thread(target=self.main_screen.sync_to_drive, args=(key, "update")).start()