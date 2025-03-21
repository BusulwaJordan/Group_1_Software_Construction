from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonIcon, MDButtonText
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.core.audio import SoundLoader
import time
from utils.storage import NoteStorage
import random

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

class NoteInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = NoteStorage()
        layout = BoxLayout(orientation='vertical', padding=dp(5), spacing=dp(5))  # Adjusted padding

        # Top bar with back button
        top_bar = BoxLayout(size_hint_y=None, height=dp(40))
        back_btn = MDButton(
            MDButtonIcon(icon="arrow-left"),
            MDButtonText(text="Back"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(30)),
            md_bg_color=COLORS["Coral"],
            on_release=self.go_back
        )
        top_bar.add_widget(back_btn)
        layout.add_widget(top_bar)

        # Title input
        self.title_input = TextInput(hint_text="Enter title", size_hint_y=None, height=dp(40), multiline=False)
        layout.add_widget(self.title_input)

        # Content input
        self.text_input = TextInput(hint_text="Enter your note here", multiline=True)
        layout.add_widget(self.text_input)

        # Save button
        save_btn = MDIconButton(
            icon="check",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            md_bg_color=COLORS["Fern Green"],
            pos_hint={'center_x': 0.5},
            on_release=self.save_note
        )
        layout.add_widget(save_btn)

        self.add_widget(layout)

    def save_note(self, instance):
        title = self.title_input.text.strip()
        content = self.text_input.text.strip()
        if content:
            note_id = str(time.time())
            color = random.choice(list(COLORS.values()))
            self.storage.save_note(note_id, content, color, title=title)
            sound = SoundLoader.load('assets/save_sound.mp3')
            if sound:
                sound.play()
            self.title_input.text = ""
            self.text_input.text = ""
            main_screen = self.manager.get_screen('main')
            main_screen.load_notes()
            self.manager.current = 'main'

    def go_back(self, instance):
        self.title_input.text = ""  # Clear inputs on back
        self.text_input.text = ""
        self.manager.current = 'main'