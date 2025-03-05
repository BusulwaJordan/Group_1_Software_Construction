import json
import os
from datetime import datetime
from threading import Timer, Lock
import threading

class NoteModel:
    _instance = None
    _lock = Lock()  # Class-level lock for singleton creation

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NoteModel, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        """Initialize instance variables."""
        self.notes = {}
        self.archived_notes = {}
        self.last_deleted = None
        self.autosave_enabled = True
        self.autosave_interval = 30  # Seconds
        self.lock = Lock()  # Instance-level lock for thread safety
        self._autosave_timer = None
        self._running = False  # Flag to track if autosave is running
        self.load_notes()
        if self.autosave_enabled:
            self._start_autosave_thread()

    def load_notes(self):
        """Load active and archived notes from files with thread safety."""
        with self.lock:
            for file_name, target_dict in [("notes.json", self.notes), ("archived_notes.json", self.archived_notes)]:
                if os.path.exists(file_name):
                    try:
                        with open(file_name, "r", encoding="utf-8") as f:
                            loaded_data = json.load(f)
                            if isinstance(loaded_data, dict):
                                target_dict.clear()
                                target_dict.update({str(k): v for k, v in loaded_data.items()})
                            else:
                                print(f"Invalid data in {file_name}, resetting to empty")
                                target_dict.clear()
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Error loading {file_name}: {e}")
                        target_dict.clear()

    def save_notes(self):
        """Save active notes to file with thread safety."""
        with self.lock:
            try:
                with open("notes.json", "w", encoding="utf-8") as f:
                    json.dump(self.notes, f, indent=4)
                return True
            except IOError as e:
                print(f"Error saving notes to notes.json: {e}")
                return False

    def save_archived_notes(self):
        """Save archived notes to file with thread safety."""
        with self.lock:
            try:
                with open("archived_notes.json", "w", encoding="utf-8") as f:
                    json.dump(self.archived_notes, f, indent=4)
                return True
            except IOError as e:
                print(f"Error saving archived notes to archived_notes.json: {e}")
                return False

    def _start_autosave_thread(self):
        """Start or restart the autosave timer."""
        with self.lock:
            if not self.autosave_enabled or self._running:
                return
            self._running = True
            self._schedule_autosave()

    def _schedule_autosave(self):
        """Schedule the next autosave."""
        if self.autosave_enabled:
            self.save_notes()
            self.save_archived_notes()
            self._autosave_timer = Timer(self.autosave_interval, self._schedule_autosave)
            self._autosave_timer.daemon = True
            self._autosave_timer.start()

    def set_autosave(self, enabled):
        """Enable or disable autosave with proper cleanup."""
        with self.lock:
            if self.autosave_enabled == enabled:
                return
            self.autosave_enabled = enabled
            if not enabled and self._autosave_timer:
                self._autosave_timer.cancel()
                self._autosave_timer = None
                self._running = False
            elif enabled and not self._running:
                self._start_autosave_thread()

    def create_note(self, title, content, labels=None, bg_color="#FFFFFF", note_type="regular"):
        """Create a new note and return its ID."""
        with self.lock:
            existing_ids = set(self.notes.keys()).union(self.archived_notes.keys())
            note_id = str(max([int(id) for id in existing_ids] + [0]) + 1)
            timestamp = str(datetime.now())
            bg_color_hex = bg_color if bg_color.startswith("#") else "#FFFFFF"
            note_data = {
                "title": title or "Untitled",
                "content": content or "",
                "labels": labels or [],
                "bg_color": bg_color_hex,
                "history": [{"timestamp": timestamp, "title": title or "Untitled", "content": content or ""}],
                "todos": [],
                "type": note_type,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            self.notes[note_id] = note_data
            success = self.save_notes()
            return note_id if success else None

    def update_note(self, note_id, content, title=None):
        """Update note content, title, and history, return success status."""
        with self.lock:
            if note_id in self.notes:
                timestamp = str(datetime.now())
                note = self.notes[note_id]
                old_title = note["title"]
                new_title = title if title is not None else old_title
                note["content"] = content or ""
                note["title"] = new_title
                note["history"].append({"timestamp": timestamp, "title": new_title, "content": content or ""})
                note["updated_at"] = timestamp
                return self.save_notes()
            return False

    def delete_note(self, note_id):
        """Delete a note and store it for undo, return success status."""
        with self.lock:
            if note_id in self.notes:
                self.last_deleted = (note_id, self.notes[note_id].copy())
                del self.notes[note_id]
                return self.save_notes()
            return False

    def archive_note(self, note_id):
        """Archive a note, return success status."""
        with self.lock:
            if note_id in self.notes:
                self.archived_notes[note_id] = self.notes[note_id].copy()
                del self.notes[note_id]
                save_active = self.save_notes()
                save_archived = self.save_archived_notes()
                return save_active and save_archived
            return False

    def unarchive_note(self, note_id):
        """Unarchive a note, return success status."""
        with self.lock:
            if note_id in self.archived_notes:
                self.notes[note_id] = self.archived_notes[note_id].copy()
                del self.archived_notes[note_id]
                save_active = self.save_notes()
                save_archived = self.save_archived_notes()
                return save_active and save_archived
            return False

    def undo_delete(self):
        """Restore the last deleted note, return its ID or None."""
        with self.lock:
            if self.last_deleted:
                note_id, note_data = self.last_deleted
                self.notes[note_id] = note_data.copy()
                self.last_deleted = None
                if self.save_notes():
                    return note_id
            return None

    def add_label(self, note_id, label):
        """Add a label to a note, return success status."""
        with self.lock:
            if note_id in self.notes and label and label not in self.notes[note_id]["labels"]:
                self.notes[note_id]["labels"].append(label)
                return self.save_notes()
            return False

    def remove_label(self, note_id, label):
        """Remove a label from a note, return success status."""
        with self.lock:
            if note_id in self.notes and label in self.notes[note_id]["labels"]:
                self.notes[note_id]["labels"].remove(label)
                return self.save_notes()
            return False

    def search_notes(self, query, include_archived=False):
        """Search notes by content, title, or labels."""
        with self.lock:
            if not query:
                return self.notes.copy() if not include_archived else {**self.notes, **self.archived_notes}
            search_results = {}
            target_dicts = [self.notes] if not include_archived else [self.notes, self.archived_notes]
            for notes_dict in target_dicts:
                for note_id, note in notes_dict.items():
                    if (query.lower() in note["content"].lower() or 
                        query.lower() in note["title"].lower() or 
                        any(query.lower() in label.lower() for label in note["labels"])):
                        search_results[note_id] = note
            return search_results

    def get_all_titles(self, include_archived=False):
        """Get all note titles and creation times."""
        with self.lock:
            target_dict = self.notes if not include_archived else {**self.notes, **self.archived_notes}
            return {
                note_id: {"title": note["title"], "created_at": note["created_at"]}
                for note_id, note in target_dict.items()
            }

    def get_note_history(self, note_id):
        """Retrieve the history of a note."""
        with self.lock:
            if note_id in self.notes:
                return self.notes[note_id]["history"].copy()
            return []