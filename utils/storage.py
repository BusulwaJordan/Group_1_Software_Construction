from kivy.storage.jsonstore import JsonStore
import time

class NoteStorage:
    def __init__(self):
        self.store = JsonStore('notes.json')
    
    def save_note(self, note_id, content, color, title="Untitled"):
        self.store.put(note_id, content=content, color=color, timestamp=time.time(), title=title, pinned=False)
    
    def delete_note(self, note_id):
        if note_id in self.store:
            self.store.delete(note_id)
    
    def pin_note(self, note_id):
        if note_id in self.store:
            data = self.store.get(note_id)
            data['pinned'] = not data.get('pinned', False)
            self.store.put(note_id, **data)