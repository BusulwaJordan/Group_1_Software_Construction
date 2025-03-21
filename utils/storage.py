import shelve
import os
import time

class NoteStorage:
    def __init__(self, db_path='notes.db'):
        self.db_path = db_path
        if not os.path.exists(os.path.dirname(db_path)) and os.path.dirname(db_path):
            os.makedirs(os.path.dirname(db_path))
        self.store = shelve.open(db_path)

    def save_note(self, note_id, content, color, title="Untitled", pinned=False):
        self.store[note_id] = {
            'content': content,
            'color': color,
            'title': title,  # Added title field
            'timestamp': time.time(),
            'pinned': pinned
        }
        self.store.sync()

    def save_image_note(self, note_id, img_path, color):
        self.store[note_id] = {
            'content': img_path,
            'color': color,
            'title': "Image Note",  # Default title for images
            'timestamp': time.time(),
            'pinned': False,
            'is_image': True
        }
        self.store.sync()

    def delete_note(self, note_id):
        if note_id in self.store:
            del self.store[note_id]
            self.store.sync()

    def pin_note(self, note_id):
        if note_id in self.store:
            note = self.store[note_id]
            note['pinned'] = not note.get('pinned', False)
            self.store[note_id] = note
            self.store.sync()

    def __del__(self):
        self.store.close()