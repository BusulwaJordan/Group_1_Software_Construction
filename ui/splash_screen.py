from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Background
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light grey
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=dp(20))
        
        # Logo (simple text-based for now)
        logo = Label(
            text="Q-NOTE",
            font_size=sp(48),  # Scalable font size
            color=(0, 0, 0, 1),
            bold=True,
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        logo.bind(size=logo.setter('text_size'))
        layout.add_widget(logo)
        
        self.add_widget(layout)
        
        # Transition to main screen after 2 seconds
        Clock.schedule_once(self.switch_to_main, 2)

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def switch_to_main(self, dt):
        self.manager.current = 'main'