from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        self.logo = Label(
            text="Q-NOTE",
            font_size=sp(48),
            color=(0, 0, 0, 1),
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(60)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.logo)
        
        Clock.schedule_once(self.switch_to_main, 3)

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def switch_to_main(self, dt):
        if self.manager:
            self.manager.current = 'main'