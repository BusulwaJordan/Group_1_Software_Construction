from kivy.uix.label import Label
from kivy.uix.button import Button

class NoteDecorator:
    def __init__(self, note_widget):
        self._note_widget = note_widget

    @property
    def note_id(self):
        return self._note_widget.note_id

    def show_options(self, instance):
        self._note_widget.show_options(instance)

    def perform_action(self, action):
        self._note_widget.perform_action(action)

class FormattedNoteDecorator(NoteDecorator):
    def build_layout(self):
        self._note_widget.clear_widgets()
        self._note_widget.add_widget(Label(text=f"[b]{self._note_widget.title}[/b]", markup=True, size_hint_y=0.3, color=(0, 0, 0, 1)))
        self._note_widget.add_widget(Label(text=f"[i]{self._note_widget.content}[/i]", markup=True, size_hint_y=0.5, color=(0.2, 0.2, 0.2, 1)))
        options_btn = Button(text="Options", size_hint_y=0.2, background_color=(0.1, 0.6, 0.9, 1))
        options_btn.bind(on_press=self.show_options)
        self._note_widget.add_widget(options_btn)