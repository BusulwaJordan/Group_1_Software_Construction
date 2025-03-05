from widgets.regular_widget import RegularNoteWidget
from widgets.todo_widget import TodoNoteWidget

class NoteWidgetFactory:
    @staticmethod
    def create_note_widget(note_id, title, content, bg_color, note_type):
        if note_type == "regular":
            return RegularNoteWidget(note_id, title, content, bg_color)
        elif note_type == "todo":
            return TodoNoteWidget(note_id, title, content, bg_color)
        else:
            raise ValueError(f"Unknown note type: {note_type}")