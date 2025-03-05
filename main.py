from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window
from model.note_model import NoteModel
from screens.splash_screen import SplashScreen
from screens.home_screen import HomeScreen
from screens.edit_screen import EditScreen
from screens.settings_screen import SettingsScreen
import kivy.utils
from kivymd.app import MDApp
from kivymd.theming import ThemeManager

class NotebookApp(MDApp):
    note_model = ObjectProperty(None)
    command_stack = ListProperty([])

    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Light"  # or "Dark" based on preference
        self.theme_cls.primary_palette = "Teal"  # Primary color for buttons/icons
        self.note_model = NoteModel()
        Window.clearcolor = kivy.utils.get_color_from_hex("#FF6F61")  # Coral background color
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EditScreen(name="edit"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.current = "splash"
        return sm

    def create_new_note(self):
        self.root.current = "edit"
        self.root.get_screen("edit").note_id = ""
        self.root.get_screen("edit").title_input.text = ""
        self.root.get_screen("edit").content_input.text = ""
        self.root.get_screen("edit").type_field.text = "regular"  # Updated to type_field

    def on_stop(self):
        self.note_model.save_notes()
        print("Notes saved on app shutdown.")

if __name__ == "__main__":
    NotebookApp().run()