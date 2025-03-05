from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        splash_label = Label(
            text="[b]Notebook App[/b]",
            markup=True,
            font_size='40sp',
            color=(0.2, 0.7, 0.3, 1)
        )
        layout.add_widget(splash_label)
        self.add_widget(layout)
        Clock.schedule_once(self.switch_to_home, 3)

    def switch_to_home(self, dt):
        self.manager.current = "home"