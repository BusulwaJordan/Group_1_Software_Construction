from widgets.base_widget import BaseNoteWidget
from kivy.uix.label import Label
from kivy.uix.button import Button
from widgets.widget_utils import add_note_widget_methods  # Import the utility to add shared methods

class RegularNoteWidget(BaseNoteWidget):
    def __init__(self, note_id, title, content, bg_color="#FFFFFF", **kwargs):
        super().__init__(note_id, title, content, bg_color, **kwargs)
        self.build_layout()

    def build_layout(self):
        self.add_widget(Label(text=f"[b]{self.title}[/b]", markup=True, size_hint_y=0.3, color=(0, 0, 0, 1)))
        self.add_widget(Label(text=self.content, size_hint_y=0.5, color=(0.2, 0.2, 0.2, 1)))
        options_btn = Button(text="Options", size_hint_y=0.2, background_color=(0.1, 0.6, 0.9, 1))
        options_btn.bind(on_press=self.show_options)  # show_options will be added by add_note_widget_methods
        self.add_widget(options_btn)

# Apply shared methods to RegularNoteWidget
RegularNoteWidget = add_note_widget_methods(RegularNoteWidget)