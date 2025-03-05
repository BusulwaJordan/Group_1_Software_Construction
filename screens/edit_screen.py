from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import AsyncImage
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp

class EditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.background_image = None
        self.background_color = get_color_from_hex("#FFFFFF")  # Default to white, managed by SettingsScreen
        self.current_note_id = None

        back_btn = MDIconButton(
            icon="arrow-left",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            md_bg_color=get_color_from_hex("#26A69A"),
            pos_hint={"top": 0.93, "x": 0.06},
            padding=dp(10)
        )
        back_btn.bind(on_press=self.go_back)

        edit_container = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=get_color_from_hex("#FFFFFF"),
            radius=[20, 20, 20, 20]
        )

        edit_container.add_widget(Label(
            text="[b]Edit Note[/b]",
            markup=True,
            font_size=dp(24),
            size_hint_y=0.1,
            color=get_color_from_hex("#333333"),
            halign="center"
        ))

        self.title_field = MDTextField(
            hint_text="Note Title",
            mode="rectangle",
            size_hint_y=0.15,
            fill_color_normal=get_color_from_hex("#F5F5F5"),
            line_color_normal=get_color_from_hex("#26A69A"),
            line_color_focus=get_color_from_hex("#26A69A"),
            font_size=dp(18)
        )
        edit_container.add_widget(self.title_field)

        self.content_field = MDTextField(
            hint_text="Note Content",
            mode="rectangle",
            multiline=True,
            size_hint_y=0.6,
            fill_color_normal=get_color_from_hex("#F5F5F5"),
            line_color_normal=get_color_from_hex("#26A69A"),
            line_color_focus=get_color_from_hex("#26A69A"),
            font_size=dp(16)
        )
        edit_container.add_widget(self.content_field)

        save_btn = MDIconButton(
            icon="check",
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            md_bg_color=get_color_from_hex("#26A69A"),
            pos_hint={"right": 0.95, "y": 0.05}
        )
        save_btn.bind(on_press=self.save_note)

        self.layout.add_widget(edit_container)
        self.layout.add_widget(back_btn)
        self.layout.add_widget(save_btn)
        self.add_widget(self.layout)

    def load_note(self, note_id):
        app = App.get_running_app()
        if hasattr(app, 'note_model') and note_id in app.note_model.notes:
            note = app.note_model.notes[note_id]
            self.title_field.text = note.get("title", "")
            self.content_field.text = note.get("content", "")
            self.current_note_id = note_id
        else:
            print(f"Note with ID {note_id} not found")

    def load_new_note(self):
        self.title_field.text = ""
        self.content_field.text = ""
        self.current_note_id = None

    def update_background_color(self, color):
        self.background_color = color
        Window.clearcolor = color
        if self.background_image:
            self.layout.remove_widget(self.background_image)
            self.background_image = None

    def set_background_image(self, file_path):
        if self.background_image:
            self.layout.remove_widget(self.background_image)
        self.background_image = AsyncImage(source=file_path, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background_image, index=len(self.layout.children))

    def save_note(self, instance):
        app = App.get_running_app()
        note_title = self.title_field.text or "Untitled"
        note_content = self.content_field.text or ""
        if hasattr(app, 'note_model'):
            if self.current_note_id is not None:
                # Update existing note
                app.note_model.update_note(self.current_note_id, note_content, note_title)
            else:
                # Create new note
                new_note_id = app.note_model.create_note(
                    title=note_title,
                    content=note_content,
                    labels=[],
                    bg_color=app.bg_color if hasattr(app, 'bg_color') else "#FFFFFF",  # Use app-wide bg color
                    note_type="regular"
                )
                self.current_note_id = new_note_id
            app.note_model.save_notes()
            self.manager.current = "home"
            self.manager.get_screen("home").update_notes()
            print(f"Note saved with ID {self.current_note_id}: {note_title}")
        else:
            print("Note model not found")

    def go_back(self, instance):
        self.manager.current = "home"

    def on_enter(self):
        # Only set background if it’s not already set by SettingsScreen
        app = App.get_running_app()
        if hasattr(app, 'bg_color'):
            Window.clearcolor = app.bg_color
        else:
            Window.clearcolor = self.background_color
        if self.background_image:
            self.layout.add_widget(self.background_image, index=len(self.layout.children))