from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout as KivyBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from ui.slide_menu import SlideMenu
from ui.note_tile import NoteTile
from utils.storage import NoteStorage
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
import random
import os
from kivy.clock import Clock
import time
import threading

COLORS = {
    "Coral": '#FF6F61', "Slate Blue": '#6B5B95', "Fern Green": '#88B04B',
    "Misty Rose": '#F7CAC9', "Light Steel Blue": '#92A8D1', "Orange Peel": '#FF9F1C',
    "Pale Red": '#D4A5A5', "Amethyst": '#9B59B6', "Sky Blue": '#3498DB',
    "Alizarin Crimson": '#E74C3C', "Emerald": '#2ECC71', "Sunflower": '#F1C40F',
    "Carrot": '#E67E22', "Turquoise": '#1ABC9C', "Midnight Blue": '#34495E',
    "Wisteria": '#8E44AD', "Pumpkin": '#D35400', "Gray": '#7F8C8D',
    "Pomegranate": '#C0392B', "Silver": '#BDC3C7', "Sea Green": '#16A085',
    "Lime Green": '#27AE60', "Denim": '#2980B9', "Taupe": '#8F7A66', "Amber": '#F39C12'
}

class MainScreen(Screen):
    menu = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = NoteStorage()
        self.layout = FloatLayout()
        self.drive_service = None
        self.sync_enabled = False
        
        # Set white background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Main content area
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        self.search_bar = MDTextField(
            hint_text="Search notes...",
            size_hint=(None, None),
            width=dp(200),
            height=dp(25),
            mode="outlined",
            pos_hint={'center_x': 0.5},
            on_text=self.filter_notes
        )
        main_layout.add_widget(self.search_bar)
        
        self.scroll_view = ScrollView()
        self.notes_stack = KivyBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.notes_stack.bind(minimum_height=self.notes_stack.setter('height'))
        self.scroll_view.add_widget(self.notes_stack)
        main_layout.add_widget(self.scroll_view)
        
        self.layout.add_widget(main_layout)
        
        # Bottom navigation bar
        self.bottom_nav = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            padding=dp(10),
            spacing=dp(10),
            pos_hint={'bottom': 1}
        )
        nav_items = [
            ("Home", "home", lambda x: self.load_notes()),
            ("New Note", "plus", self.go_to_note_input),
            ("Settings", "cog", self.go_to_settings),
            ("Menu", "menu", self.toggle_menu)
        ]
        for text, icon, action in nav_items:
            btn = MDButton(
                MDButtonIcon(icon=icon),
                MDButtonText(text=text),
                style="elevated",
                size_hint=(None, None),
                size=(dp(80), dp(40)),
                md_bg_color=COLORS["Fern Green"] if icon == "plus" else COLORS["Slate Blue"],
                on_release=action
            )
            self.bottom_nav.add_widget(btn)
        self.layout.add_widget(self.bottom_nav)
        
        self.menu = SlideMenu(main_screen=self)
        self.layout.add_widget(self.menu)
        
        self.add_widget(self.layout)
        Clock.schedule_once(lambda dt: self.load_notes(), 0)
    
    def update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def toggle_menu(self, instance):
        if self.menu.pos_hint['x'] < 0:
            anim = Animation(pos_hint={'x': 0}, duration=0.3)
        else:
            anim = Animation(pos_hint={'x': -0.7}, duration=0.3)
        anim.start(self.menu)
    
    def load_notes(self):
        search_query = self.search_bar.text
        self.notes_stack.clear_widgets()
        for key in sorted(self.storage.store, key=lambda x: self.storage.store.get(x)['timestamp'], reverse=True):
            data = self.storage.store.get(key)
            content = data['content']
            title = data.get('title', 'Untitled')
            if not search_query or search_query.lower() in title.lower():
                color = data.get('color', random.choice(list(COLORS.values())))
                timestamp = data['timestamp']
                tags = data.get('tags', [])
                tile = NoteTile(content, key, color, timestamp, title, tags)
                tile.screen = self
                self.notes_stack.add_widget(tile)
    
    def filter_notes(self, instance, value):
        self.load_notes()
    
    def delete_note(self, key):
        self.storage.delete_note(key)
        self.load_notes()
        if self.sync_enabled and self.drive_service:
            threading.Thread(target=self.sync_to_drive, args=(key, "delete")).start()
    
    def pin_note(self, key):
        self.storage.pin_note(key)
        self.load_notes()
    
    def edit_note(self, key, new_content, new_title, new_tags):
        if key in self.storage.store:
            data = self.storage.store.get(key)
            data['content'] = new_content
            data['title'] = new_title
            data['tags'] = new_tags
            data['timestamp'] = time.time()
            self.storage.store[key] = data
            self.storage.store.sync()
            self.load_notes()
            if self.sync_enabled and self.drive_service:
                threading.Thread(target=self.sync_to_drive, args=(key, "update")).start()
    
    def save_note(self, content, title, color, tags):
        note_id = str(time.time())
        self.storage.save_note(note_id, content, color, title=title, tags=tags)
        self.load_notes()
        if self.sync_enabled and self.drive_service:
            threading.Thread(target=self.sync_to_drive, args=(note_id, "create")).start()
    
    def setup_drive(self):
        try:
            # Load service account credentials
            creds = Credentials.from_service_account_file('qnote-service-account.json', scopes=['https://www.googleapis.com/auth/drive'])
            self.drive_service = build('drive', 'v3', credentials=creds)
            print("Google Drive API initialized with service account.")
        except Exception as e:
            Popup(title="Drive Error", content=Label(text=f"Failed to initialize Drive: {e}"), size_hint=(0.8, 0.4)).open()
            self.drive_service = None
    
    def sync_to_drive(self, note_id, action):
        if not self.drive_service or not self.sync_enabled:
            return
        try:
            folder_id = self.get_drive_folder()
            if action in ("create", "update"):
                data = self.storage.store.get(note_id)
                if not data:
                    return
                content = f"{data['title']}\n\n{data['content']}\n\nTags: {', '.join(data.get('tags', []))}".encode('utf-8')
                file_name = f"{data['title']}_{note_id}.txt"
                # Check if file exists
                query = f"'{folder_id}' in parents name='{file_name}' trashed=false"
                response = self.drive_service.files().list(q=query, fields="files(id)").execute()
                files = response.get('files', [])
                if files:
                    file_id = files[0]['id']
                    media = MediaInMemoryUpload(content, mimetype='text/plain')
                    self.drive_service.files().update(fileId=file_id, media_body=media).execute()
                    print(f"Note {note_id} updated on Drive.")
                else:
                    metadata = {'name': file_name, 'parents': [folder_id], 'mimeType': 'text/plain'}
                    media = MediaInMemoryUpload(content, mimetype='text/plain')
                    self.drive_service.files().create(body=metadata, media_body=media).execute()
                    print(f"Note {note_id} created on Drive.")
            elif action == "delete":
                query = f"'{folder_id}' in parents name contains '{note_id}' trashed=false"
                response = self.drive_service.files().list(q=query, fields="files(id)").execute()
                for file in response.get('files', []):
                    self.drive_service.files().delete(fileId=file['id']).execute()
                    print(f"Note {note_id} deleted from Drive.")
        except Exception as e:
            Popup(title="Sync Error", content=Label(text=f"Sync failed: {e}"), size_hint=(0.8, 0.4)).open()
            print(f"Drive sync failed: {e}")
    
    def get_drive_folder(self):
        try:
            query = "name='Q-NOTE' mimeType='application/vnd.google-apps.folder' trashed=false"
            response = self.drive_service.files().list(q=query, fields="files(id)").execute()
            folders = response.get('files', [])
            if not folders:
                folder_metadata = {'name': 'Q-NOTE', 'mimeType': 'application/vnd.google-apps.folder'}
                folder = self.drive_service.files().create(body=folder_metadata).execute()
                return folder['id']
            return folders[0]['id']
        except Exception as e:
            Popup(title="Folder Error", content=Label(text=f"Failed to access Q-NOTE folder: {e}"), size_hint=(0.8, 0.4)).open()
            raise
    
    def add_image(self, instance):
        popup = Popup(title="Select Image", size_hint=(0.9, 0.9))
        file_chooser = FileChooserIconView()
        select_btn = MDIconButton(
            icon="check",
            size_hint_y=None,
            height=dp(50),
            md_bg_color=COLORS["Light Steel Blue"],
            on_press=lambda x: self.embed_image(file_chooser.selection, popup)
        )
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(select_btn)
        popup.content = layout
        popup.open()

    def embed_image(self, selection, popup):
        if selection:
            img_path = selection[0]
            note_id = str(time.time())
            self.storage.save_note(note_id, f"Image: {img_path}", random.choice(list(COLORS.values())), title="Image Note", tags=[])
            self.load_notes()
            if self.sync_enabled and self.drive_service:
                threading.Thread(target=self.sync_to_drive, args=(note_id, "create")).start()
        popup.dismiss()
    
    def set_reminder(self, instance):
        popup = Popup(title="Set Reminder", size_hint=(0.8, 0.4))
        layout = BoxLayout(orientation='vertical')
        time_input = MDTextField(hint_text="Time in minutes", mode="outlined")
        set_btn = MDIconButton(
            icon="check",
            md_bg_color=COLORS["Fern Green"],
            on_press=lambda x: self.schedule_reminder(time_input.text, popup)
        )
        layout.add_widget(time_input)
        layout.add_widget(set_btn)
        popup.content = layout
        popup.open()
    
    def schedule_reminder(self, minutes, popup):
        try:
            Clock.schedule_once(lambda dt: self.show_reminder_popup(), float(minutes) * 60)
            popup.dismiss()
        except ValueError:
            Popup(title="Error", content=Label(text="Invalid time input"), size_hint=(0.8, 0.4)).open()
    
    def show_reminder_popup(self):
        Popup(title="Reminder!", content=Label(text="Time's up!"), size_hint=(0.5, 0.3)).open()
    
    def go_to_note_input(self, instance):
        self.manager.current = 'note_input'
    
    def go_to_settings(self, instance):
        self.manager.current = 'settings'