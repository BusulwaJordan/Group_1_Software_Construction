from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
import kivy.utils
from abc import abstractmethod

class BaseNoteWidget(BoxLayout):
    note_id = StringProperty("")
    title = StringProperty("")
    content = StringProperty("")
    bg_color = StringProperty("#FFFFFF")

    def __init__(self, note_id, title, content, bg_color="#FFFFFF", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = 150
        self.note_id = note_id
        self.title = title
        self.content = content[:100] + "..." if len(content) > 100 else content
        self.bg_color = bg_color
        self.canvas.before.clear()
        with self.canvas.before:
            self.color = Color(*kivy.utils.get_color_from_hex(self.bg_color))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.color.rgba = kivy.utils.get_color_from_hex(self.bg_color)

    @abstractmethod
    def build_layout(self):
        pass