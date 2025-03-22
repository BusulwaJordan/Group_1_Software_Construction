from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivy.metrics import dp

class SlideMenu(BoxLayout):
    def __init__(self, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.orientation = 'vertical'
        self.size_hint_x = 0.7
        self.pos_hint = {'x': -0.7}
        self.padding = dp(10)
        self.spacing = dp(10)
        
        for text, icon, action in [
            ("Add Image", "image", self.main_screen.add_image),
            ("Share", "share", self.main_screen.share_email),
            ("Set Reminder", "bell", self.main_screen.set_reminder)
        ]:
            btn = MDButton(
                MDButtonIcon(icon=icon),
                MDButtonText(text=text),
                style="elevated",
                size_hint_y=None,
                height=dp(50),
                on_release=action
            )
            self.add_widget(btn)