from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from utils.storage import NoteStorage
import time
import random
from ui.main_screen import COLORS

class NoteInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = NoteStorage()
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.title_input = MDTextField(
            hint_text="Title",
            mode="outlined",
            size_hint_y=None,
            height=dp(40)
        )
        self.content_input = MDTextField(
            hint_text="Content",
            mode="outlined",
            multiline=True,
            size_hint_y=None,
            height=dp(200)
        )
        save_btn = MDButton(
            MDButtonText(text="Save"),
            style="elevated",
            md_bg_color="#88B04B",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5},
            on_release=self.save_note
        )
        
        layout.add_widget(self.title_input)
        layout.add_widget(self.content_input)
        layout.add_widget(save_btn)
        
        self.add_widget(layout)

    def save_note(self, instance):
        title = self.title_input.text or "Untitled"
        content = self.content_input.text
        if content:
            note_id = str(time.time())
            self.storage.save_note(note_id, content, random.choice(list(COLORS.values())), title=title)
            self.title_input.text = ""
            self.content_input.text = ""
            self.manager.get_screen('main').load_notes()
            self.manager.current = 'main'