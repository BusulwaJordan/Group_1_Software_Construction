from widgets.base_widget import BaseNoteWidget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout

class TodoNoteWidget(BaseNoteWidget):
    def __init__(self, note_id, title, content, bg_color="#FFFFFF", **kwargs):
        super().__init__(note_id, title, content, bg_color, **kwargs)
        self.build_layout()

    def build_layout(self):
        self.add_widget(Label(text=f"[b]{self.title} (To-Do)[/b]", markup=True, size_hint_y=0.3, color=(0, 0, 0, 1)))
        todo_layout = BoxLayout(orientation="horizontal", size_hint_y=0.5)
        todo_layout.add_widget(CheckBox(size_hint_x=0.2))
        todo_layout.add_widget(Label(text=self.content, color=(0.2, 0.2, 0.2, 1)))
        self.add_widget(todo_layout)
        options_btn = Button(text="Options", size_hint_y=0.2, background_color=(0.1, 0.6, 0.9, 1))
        options_btn.bind(on_press=self.show_options)
        self.add_widget(options_btn)