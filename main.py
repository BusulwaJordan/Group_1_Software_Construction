from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ui.main_screen import MainScreen
from ui.note_input import NoteInputScreen
from ui.note_tile import NoteViewScreen
from ui.settings import SettingsScreen
from ui.slide_menu import SlideMenu
from kivy.graphics import Color, Rectangle

class NoteApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Light theme base
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"
        
        sm = ScreenManager()
        # Set grey background
        with sm.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light grey (#E6E6E6)
            self.bg_rect = Rectangle(pos=sm.pos, size=sm.size)
        sm.bind(pos=self.update_bg_rect, size=self.update_bg_rect)
        
        main_screen = MainScreen(name='main')
        sm.add_widget(main_screen)
        sm.add_widget(NoteInputScreen(name='note_input'))
        sm.add_widget(NoteViewScreen(main_screen=main_screen, name='note_view'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'main'  # Explicitly set initial screen
        
        return sm

    def update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

if __name__ == '__main__':
    NoteApp().run()