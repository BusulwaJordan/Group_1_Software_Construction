from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ui.main_screen import MainScreen
from ui.note_tile import NoteViewScreen
from ui.settings import SettingsScreen
from ui.note_input import NoteInputScreen

class QNoteApp(MDApp):
    def build(self):
        print("Available font styles before fix:", self.theme_cls.font_styles)
        # Restore default font styles if missing
        expected_styles = {
            'H1': ['Roboto', 96, False, -1.5],
            'H2': ['Roboto', 60, False, -0.5],
            'H3': ['Roboto', 48, False, 0],
            'H4': ['Roboto', 34, False, 0.25],
            'H5': ['Roboto', 24, False, 0.15],
            'H6': ['Roboto', 20, False, 0.15],
            'Subtitle1': ['Roboto', 16, False, 0.15],
            'Subtitle2': ['Roboto', 14, False, 0.1],
            'Body1': ['Roboto', 16, False, 0.5],
            'Body2': ['Roboto', 14, False, 0.25],
            'Button': ['Roboto', 14, True, 0.25],
            'Caption': ['Roboto', 12, False, 0.4],
            'Overline': ['Roboto', 10, False, 1.5]
        }
        for style, value in expected_styles.items():
            if style not in self.theme_cls.font_styles:
                self.theme_cls.font_styles[style] = value
        print("Available font styles after fix:", self.theme_cls.font_styles)
        
        sm = ScreenManager()
        main_screen = MainScreen(name='main')
        sm.add_widget(main_screen)
        sm.add_widget(NoteViewScreen(main_screen=main_screen, name='note_view'))
        sm.add_widget(SettingsScreen(main_screen=main_screen, name='settings'))
        sm.add_widget(NoteInputScreen(main_screen=main_screen, name='note_input'))
        return sm

if __name__ == '__main__':
    QNoteApp().run()