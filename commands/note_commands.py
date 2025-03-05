from model.note_model import NoteModel

class Command:
    def execute(self):
        pass

    def undo(self):
        pass

class UpdateNoteCommand(Command):
    def __init__(self, model: NoteModel, note_id, new_content, old_content):
        self.model = model
        self.note_id = note_id
        self.new_content = new_content
        self.old_content = old_content

    def execute(self):
        self.model.update_note(self.note_id, self.new_content)

    def undo(self):
        self.model.update_note(self.note_id, self.old_content)