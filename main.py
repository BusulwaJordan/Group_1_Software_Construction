from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from ui.main_screen import MainScreen
from ui.note_input import NoteInputScreen
from ui.note_tile import NoteViewScreen
from ui.settings import SettingsScreen
from ui.splash_screen import SplashScreen
from ui.slide_menu import SlideMenu
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp

class QNoteApp(MDApp):  # Renamed class
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"
        
        # Ensure resizability
        Window.size = (dp(360), dp(640))  # Default mobile size, but resizable
        Window.bind(on_resize=self.on_window_resize)
        
        sm = ScreenManager(transition=FadeTransition())
        # Set grey background
        with sm.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light grey
            self.bg_rect = Rectangle(pos=sm.pos, size=sm.size)
        sm.bind(pos=self.update_bg_rect, size=self.update_bg_rect)
        
        main_screen = MainScreen(name='main')
        sm.add_widget(SplashScreen(name='splash'))  # Add splash first
        sm.add_widget(main_screen)
        sm.add_widget(NoteInputScreen(name='note_input'))
        sm.add_widget(NoteViewScreen(main_screen=main_screen, name='note_view'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'splash'  # Start with splash
        
        return sm

    def update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_window_resize(self, window, width, height):
        # Update layouts dynamically (already handled by dp/sp)
        pass

if __name__ == '__main__':
    QNoteApp().run()