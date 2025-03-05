from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from decorators.note_decorator import FormattedNoteDecorator
from strategies.share_context import NoteSharingContext
from strategies.share_strategy import SocialMediaShareStrategy, GoogleDriveShareStrategy
from config.colors import COLOR_MAP
from kivy.app import App  # Import App to resolve undefined variable errors

def add_note_widget_methods(cls):
    def show_options(self, instance):
        content = BoxLayout(orientation="vertical")
        actions = ["Edit", "Delete", "Share", "Add Label", "Change Color", "Format", "Upload to Drive"]
        for action in actions:
            btn = Button(text=action, background_color=(0.2, 0.7, 0.3, 1))
            btn.bind(on_press=lambda btn, a=action: self.perform_action(a))
            content.add_widget(btn)
        popup = Popup(title="Note Options", content=content, size_hint=(0.8, 0.8), background_color=(0.9, 0.9, 0.9, 1))
        popup.open()

    def perform_action(self, action):
        app = App.get_running_app()
        if action == "Edit":
            app.root.current = "edit"
            app.root.get_screen("edit").load_note(self.note_id)
        elif action == "Delete":
            app.note_model.delete_note(self.note_id)
            app.root.get_screen("home").update_notes()
        elif action == "Share":
            share_context = NoteSharingContext(SocialMediaShareStrategy())
            share_context.share_note(self.title, self.content)
        elif action == "Add Label":
            self.add_label_popup()
        elif action == "Change Color":
            self.change_color_popup()
        elif action == "Format":
            decorated_note = FormattedNoteDecorator(self)
            decorated_note.build_layout()
        elif action == "Upload to Drive":
            share_context = NoteSharingContext(GoogleDriveShareStrategy())
            share_context.share_note(self.title, self.content)

    def add_label_popup(self):
        content = BoxLayout(orientation="vertical")
        label_input = TextInput(hint_text="Enter label")
        content.add_widget(label_input)
        btn = Button(text="Add", background_color=(0.1, 0.6, 0.9, 1))
        btn.bind(on_press=lambda x: self.add_label(label_input.text))
        content.add_widget(btn)
        popup = Popup(title="Add Label", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def add_label(self, label):
        app = App.get_running_app()
        app.note_model.add_label(self.note_id, label)
        app.root.get_screen("home").update_notes()

    def change_color_popup(self):
        content = BoxLayout(orientation="vertical")
        colors = ["white", "lightblue", "lightgreen", "lightyellow"]
        spinner = Spinner(values=colors, background_color=(0.9, 0.9, 0.9, 1))
        content.add_widget(spinner)
        btn = Button(text="Apply", background_color=(0.1, 0.6, 0.9, 1))
        btn.bind(on_press=lambda x: self.change_color(spinner.text))
        content.add_widget(btn)
        popup = Popup(title="Change Color", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def change_color(self, color):
        self.bg_color = COLOR_MAP.get(color, "#FFFFFF")
        app = App.get_running_app()
        app.note_model.notes[self.note_id]["bg_color"] = self.bg_color
        app.note_model.save_notes()
        app.root.get_screen("home").update_notes()

    # Attach methods to the class
    cls.show_options = show_options
    cls.perform_action = perform_action
    cls.add_label_popup = add_label_popup
    cls.add_label = add_label
    cls.change_color_popup = change_color_popup
    cls.change_color = change_color
    return cls