from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
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
from ui.slide_menu import SlideMenu
from ui.note_tile import NoteTile
from utils.storage import NoteStorage
import random
import os
import webbrowser
from urllib.parse import quote

COLORS = {
    "Coral": '#FF6F61',
    "Slate Blue": '#6B5B95',
    "Fern Green": '#88B04B',
    "Misty Rose": '#F7CAC9',
    "Light Steel Blue": '#92A8D1',
    "Orange Peel": '#FF9F1C',
    "Pale Red": '#D4A5A5',
    "Amethyst": '#9B59B6',
    "Sky Blue": '#3498DB',
    "Alizarin Crimson": '#E74C3C',
    "Emerald": '#2ECC71',
    "Sunflower": '#F1C40F',
    "Carrot": '#E67E22',
    "Turquoise": '#1ABC9C',
    "Midnight Blue": '#34495E',
    "Wisteria": '#8E44AD',
    "Pumpkin": '#D35400',
    "Gray": '#7F8C8D',
    "Pomegranate": '#C0392B',
    "Silver": '#BDC3C7',
    "Sea Green": '#16A085',
    "Lime Green": '#27AE60',
    "Denim": '#2980B9',
    "Taupe": '#8F7A66',
    "Amber": '#F39C12'
}

class MainScreen(Screen):
    menu = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = NoteStorage()
        self.layout = FloatLayout()
        
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(5))
        menu_btn = MDIconButton(
            icon="menu",
            md_bg_color=COLORS["Coral"],
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_y': 0.5},
            on_press=self.toggle_menu
        )
        header.add_widget(menu_btn)
        header.add_widget(Label(text="Q-NOTE", font_size=28, color=(0,0,0,1)))
        settings_btn = MDIconButton(
            icon="cog",
            md_bg_color=COLORS["Slate Blue"],
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_y': 0.5},
            on_press=self.go_to_settings
        )
        header.add_widget(settings_btn)
        main_layout.add_widget(header)
        
        # Search bar
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
        
        # Scrollable notes
        self.scroll_view = ScrollView()
        self.notes_stack = KivyBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.notes_stack.bind(minimum_height=self.notes_stack.setter('height'))
        self.scroll_view.add_widget(self.notes_stack)
        main_layout.add_widget(self.scroll_view)
        
        # Plus button
        plus_btn = MDIconButton(
            icon="plus",
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            pos_hint={'right': 0.95, 'bottom': 0.95},
            md_bg_color=COLORS["Fern Green"],
            on_press=self.go_to_note_input
        )
        self.layout.add_widget(main_layout)
        self.layout.add_widget(plus_btn)
        
        self.menu = SlideMenu(main_screen=self)
        self.layout.add_widget(self.menu)
        
        self.add_widget(self.layout)
        self.load_notes()
    
    def toggle_menu(self, instance):
        anim = Animation(pos_hint={'x': 0 if self.menu.pos_hint['x'] < 0 else -0.7}, duration=0.3)
        anim.start(self.menu)
    
    def load_notes(self, search_query=""):
        self.notes_stack.clear_widgets()
        for key in sorted(self.storage.store, key=lambda x: self.storage.store.get(x)['timestamp'], reverse=True):
            data = self.storage.store.get(key)
            content = data['content']
            title = data.get('title', 'Untitled')
            if not search_query or search_query.lower() in title.lower():
                color = data.get('color', random.choice(list(COLORS.values())))
                timestamp = data['timestamp']
                tile = NoteTile(content, key, color, timestamp, title)
                tile.screen = self
                self.notes_stack.add_widget(tile)
    
    def filter_notes(self, instance, value):
        self.load_notes(value)
    
    def delete_note(self, key):
        self.storage.delete_note(key)
        self.load_notes()
    
    def pin_note(self, key):
        self.storage.pin_note(key)
        self.load_notes()
    
    def edit_note(self, key, new_content, new_title):
        if key in self.storage.store:
            data = self.storage.store.get(key)
            data['content'] = new_content
            data['title'] = new_title
            self.storage.store[key] = data
            self.storage.store.sync()
            self.load_notes()
    
    def go_to_note_input(self, instance):
        self.manager.current = 'note_input'
    
    def go_to_settings(self, instance):
        self.manager.current = 'settings'