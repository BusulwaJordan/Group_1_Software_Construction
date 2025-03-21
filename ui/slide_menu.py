from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivy.metrics import dp
import json
import os
from kivy.graphics import Color, Rectangle
from ui.note_tile import NoteTile

class SlideMenu(BoxLayout):
    def __init__(self, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.orientation = 'vertical'
        self.size_hint_x = 0.7
        self.pos_hint = {'x': -0.7}
        with self.canvas.before:
            Color(rgb=[0.2, 0.2, 0.2, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        menu_items = [
            ("export", "Export All", self.export_notes),
            ("import", "Import Notes", self.import_notes),
            ("palette", "Change Theme", self.change_theme),
            ("delete-sweep", "Clear All", self.clear_all),
            ("sort-variant", "Sort by Date", self.sort_by_date),
            ("sort-alphabetical", "Sort by Title", self.sort_by_title),
            ("backup", "Backup Notes", self.backup_notes),
            ("chart-bar", "Statistics", self.show_stats),
        ]
        for icon, text, callback in menu_items:
            btn = MDButton(
                MDButtonIcon(icon=icon),
                MDButtonText(text=text),
                style="elevated",
                md_bg_color='#444444',
                size_hint_y=None,
                height=dp(50),
                on_press=callback
            )
            self.add_widget(btn)
        
        back_btn = MDButton(
            MDButtonIcon(icon="arrow-left"),
            MDButtonText(text="Back"),
            style="elevated",
            md_bg_color='#FF6F61',
            size_hint_y=None,
            height=dp(50),
            on_press=self.close_menu
        )
        self.add_widget(back_btn)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def close_menu(self, instance):
        from kivy.animation import Animation
        anim = Animation(pos_hint={'x': -0.7}, duration=0.3)
        anim.start(self)

    def export_notes(self, *args):
        if self.main_screen and self.main_screen.storage:
            with open('notes_export.json', 'w') as f:
                json.dump(dict(self.main_screen.storage.store), f)  # Fixed: Use dict()
            print("Notes exported to notes_export.json")
    
    def import_notes(self, *args):
        if self.main_screen and self.main_screen.storage and os.path.exists('notes_export.json'):
            with open('notes_export.json', 'r') as f:
                data = json.load(f)
            for key, value in data.items():
                self.main_screen.storage.store.put(key, **value)  # Update store directly
            self.main_screen.load_notes()
            print("Notes imported from notes_export.json")
    
    def change_theme(self, *args):
        self.main_screen.manager.current = 'settings'
    
    def clear_all(self, *args):
        if self.main_screen and self.main_screen.storage:
            self.main_screen.storage.store.clear()
            self.main_screen.load_notes()
            print("All notes cleared!")
    
    def sort_by_date(self, *args):
        if self.main_screen and self.main_screen.storage:
            self.main_screen.notes_stack.clear_widgets()
            for key in sorted(self.main_screen.storage.store, key=lambda x: self.storage.store.get(x)['timestamp'], reverse=True):
                content = self.main_screen.storage.store.get(key)['content']
                color = self.main_screen.storage.store.get(key).get('color', '#FF6F61')
                tile = NoteTile(content, key, color)
                tile.screen = self.main_screen
                self.main_screen.notes_stack.add_widget(tile)
            print("Sorted by date")
    
    def sort_by_title(self, *args):
        if self.main_screen and self.main_screen.storage:
            self.main_screen.notes_stack.clear_widgets()
            for key in sorted(self.main_screen.storage.store, key=lambda x: self.main_screen.storage.store.get(x)['content']):
                content = self.main_screen.storage.store.get(key)['content']
                color = self.main_screen.storage.store.get(key).get('color', '#FF6F61')
                tile = NoteTile(content, key, color)
                tile.screen = self.main_screen
                self.main_screen.notes_stack.add_widget(tile)
            print("Sorted by title")
    
    def backup_notes(self, *args):
        if self.main_screen and self.main_screen.storage:
            with open('notes_backup.json', 'w') as f:
                json.dump(dict(self.main_screen.storage.store), f)  # Fixed: Use dict()
            print("Notes backed up to notes_backup.json")
    
    def show_stats(self, *args):
        if self.main_screen and self.main_screen.storage:
            total_notes = len(self.main_screen.storage.store)
            pinned = sum(1 for k in self.main_screen.storage.store if self.main_screen.storage.store.get(k).get('pinned', False))
            print(f"Total Notes: {total_notes}, Pinned: {pinned}")