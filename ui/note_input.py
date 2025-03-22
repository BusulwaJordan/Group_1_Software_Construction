import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from .main_screen import COLORS

class NoteInputScreen(Screen):
    def __init__(self, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Title
        self.title_input = MDTextField(
            hint_text="Title",
            mode="outlined",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.title_input)
        
        # Content
        self.content_input = MDTextField(
            hint_text="Note content (Markdown supported)",
            mode="outlined",
            multiline=True
        )
        layout.add_widget(self.content_input)
        
        # Tags
        self.tags_input = MDTextField(
            hint_text="Tags (comma-separated)",
            mode="outlined",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.tags_input)
        
        # Toolbar
        toolbar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))
        toolbar.add_widget(MDIconButton(icon="format-bold", on_release=lambda x: self.add_formatting("**")))
        toolbar.add_widget(MDIconButton(icon="format-italic", on_release=lambda x: self.add_formatting("*")))
        toolbar.add_widget(MDIconButton(icon="format-list-bulleted", on_release=lambda x: self.add_formatting("- ")))
        
        self.color_spinner = Spinner(
            text="Pick a color",
            values=list(COLORS.keys()),
            size_hint=(None, None),
            size=(dp(120), dp(40))
        )
        toolbar.add_widget(self.color_spinner)
        
        layout.add_widget(toolbar)
        
        # Actions
        actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        save_btn = MDButton(
            MDButtonText(text="Save"),
            style="elevated",
            md_bg_color='#88B04B',
            on_release=self.save_note
        )
        back_btn = MDButton(
            MDButtonText(text="Back"),
            style="elevated",
            md_bg_color='#FF6F61',
            on_release=self.go_back
        )
        actions.add_widget(save_btn)
        actions.add_widget(back_btn)
        layout.add_widget(actions)
        
        self.add_widget(layout)
    
    def add_formatting(self, marker):
        current_text = self.content_input.text
        cursor_pos = self.content_input.cursor_index()
        if marker == "- ":
            self.content_input.text = current_text[:cursor_pos] + marker + current_text[cursor_pos:]
        else:
            selected_text = self.content_input.get_selected_text()
            if selected_text:
                new_text = f"{marker}{selected_text}{marker}"
                self.content_input.text = current_text.replace(selected_text, new_text)
            else:
                self.content_input.text = current_text[:cursor_pos] + marker + marker + current_text[cursor_pos:]
        self.content_input.focus = True
    
    def save_note(self, instance):
        title = self.title_input.text.strip() or "Untitled"
        content = self.content_input.text.strip()
        tags = [tag.strip() for tag in self.tags_input.text.split(',') if tag.strip()]
        color = COLORS.get(self.color_spinner.text, random.choice(list(COLORS.values())))
        if content and self.main_screen:
            self.main_screen.save_note(content, title, color, tags)
            self.manager.current = 'main'
    
    def go_back(self, instance):
        self.manager.current = 'main'