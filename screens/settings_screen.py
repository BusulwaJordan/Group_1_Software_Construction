from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.background_image = None
        self.background_color = get_color_from_hex("#FFFFFF")  # Default to white

        back_btn = MDIconButton(
            icon="arrow-left",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            md_bg_color=get_color_from_hex("#26A69A"),
            pos_hint={"top": 0.93, "x": 0.06},
            padding=dp(10)
        )
        back_btn.bind(on_press=self.go_back)

        settings_container = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=get_color_from_hex("#FFFFFF"),
            radius=[20, 20, 20, 20]
        )

        settings_container.add_widget(Label(
            text="[b]Settings[/b]",
            markup=True,
            font_size=dp(24),
            size_hint_y=0.1,
            color=get_color_from_hex("#333333"),
            halign="center"
        ))

        theme_layout = MDBoxLayout(orientation="horizontal", size_hint_y=0.1, spacing=dp(10))
        theme_layout.add_widget(Label(text="Theme:", color=get_color_from_hex("#333333"), size_hint_x=0.4))
        self.theme_field = MDTextField(
            text="Light",
            size_hint_x=0.5,
            mode="rectangle",
            readonly=True,
            fill_color_normal=get_color_from_hex("#F5F5F5"),
            line_color_normal=get_color_from_hex("#26A69A"),
            line_color_focus=get_color_from_hex("#26A69A")
        )
        theme_btn = MDIconButton(icon="menu-down", size_hint_x=0.1, md_bg_color=get_color_from_hex("#26A69A"))
        theme_btn.bind(on_release=self.show_theme_menu)
        theme_layout.add_widget(self.theme_field)
        theme_layout.add_widget(theme_btn)
        self.theme_menu_items = [
            {"text": "Light", "on_release": lambda x="Light": self.change_theme(None, x)},
            {"text": "Dark", "on_release": lambda x="Dark": self.change_theme(None, x)}
        ]
        self.theme_menu = MDDropdownMenu(caller=theme_btn, items=self.theme_menu_items, width_mult=4)
        settings_container.add_widget(theme_layout)

        bg_layout = MDBoxLayout(orientation="horizontal", size_hint_y=0.1, spacing=dp(10))
        bg_layout.add_widget(Label(text="Background Color:", color=get_color_from_hex("#333333"), size_hint_x=0.4))
        self.color_field = MDTextField(
            text="White",
            size_hint_x=0.5,
            mode="rectangle",
            readonly=True,
            fill_color_normal=get_color_from_hex("#F5F5F5"),
            line_color_normal=get_color_from_hex("#26A69A"),
            line_color_focus=get_color_from_hex("#26A69A")
        )
        color_btn = MDIconButton(icon="menu-down", size_hint_x=0.1, md_bg_color=get_color_from_hex("#26A69A"))
        color_btn.bind(on_release=self.show_color_menu)
        bg_layout.add_widget(self.color_field)
        bg_layout.add_widget(color_btn)
        self.color_menu_items = [
            {"text": color, "on_release": lambda x=color: self.change_bg_color(None, x)}
            for color in ["Coral", "Amber", "Sky Blue", "Purple", "White", "Lime Green", "Pink", "Teal",
                          "Lavender", "Orange", "Mint", "Yellow", "Red", "Blue", "Green"]
        ]
        self.color_menu = MDDropdownMenu(caller=color_btn, items=self.color_menu_items, width_mult=4)
        settings_container.add_widget(bg_layout)

        font_layout = MDBoxLayout(orientation="horizontal", size_hint_y=0.1, spacing=dp(10))
        font_layout.add_widget(Label(text="Font Size:", color=get_color_from_hex("#333333"), size_hint_x=0.4))
        self.font_field = MDTextField(
            text="16",
            size_hint_x=0.5,
            mode="rectangle",
            readonly=True,
            fill_color_normal=get_color_from_hex("#F5F5F5"),
            line_color_normal=get_color_from_hex("#26A69A"),
            line_color_focus=get_color_from_hex("#26A69A")
        )
        font_btn = MDIconButton(icon="menu-down", size_hint_x=0.1, md_bg_color=get_color_from_hex("#26A69A"))
        font_btn.bind(on_release=self.show_font_menu)
        font_layout.add_widget(self.font_field)
        font_layout.add_widget(font_btn)
        self.font_menu_items = [
            {"text": size, "on_release": lambda x=size: self.change_font_size(None, x)}
            for size in ["12", "14", "16", "18", "20", "22", "24"]
        ]
        self.font_menu = MDDropdownMenu(caller=font_btn, items=self.font_menu_items, width_mult=4)
        settings_container.add_widget(font_layout)

        autosave_layout = MDBoxLayout(orientation="horizontal", size_hint_y=0.1, spacing=dp(10))
        autosave_layout.add_widget(Label(text="Auto-Save Notes:", color=get_color_from_hex("#333333"), size_hint_x=0.4))
        self.autosave_switch = MDCheckbox(active=True, size_hint=(None, None), size=(dp(40), dp(40)), pos_hint={"center_y": 0.5})
        self.autosave_switch.bind(active=self.toggle_autosave)
        autosave_layout.add_widget(self.autosave_switch)
        settings_container.add_widget(autosave_layout)

        bg_image_btn = MDButton(
            text="Set Background Image",
            md_bg_color=get_color_from_hex("#26A69A"),
            text_color=[1, 1, 1, 1],
            size_hint=(None, None),
            height=dp(40),
            width=dp(200),
            pos_hint={"center_x": 0.5}
        )
        bg_image_btn.bind(on_press=self.open_file_chooser)
        settings_container.add_widget(bg_image_btn)

        self.layout.add_widget(settings_container)
        self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def show_theme_menu(self, instance):
        self.theme_menu.open()

    def show_color_menu(self, instance):
        self.color_menu.open()

    def show_font_menu(self, instance):
        self.font_menu.open()

    def open_file_chooser(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.set_background_image)
        popup = Popup(title="Select Background Image", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def set_background_image(self, instance, file_path, *args):
        if not file_path:
            return
        if self.background_image:
            self.layout.remove_widget(self.background_image)
        self.background_image = AsyncImage(source=file_path[0], allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background_image, index=len(self.layout.children))
        for screen_name in ["home", "edit"]:
            self.manager.get_screen(screen_name).set_background_image(file_path[0])

    def change_theme(self, instance, value):
        app = App.get_running_app()
        app.theme_cls.theme_style = value
        self.theme_field.text = value
        self.theme_menu.dismiss()
        print(f"Theme changed to {value}")

    def change_bg_color(self, instance, value):
        app = App.get_running_app()
        color_map = {
            "Coral": "#FF6F61", "Amber": "#FFB300", "Sky Blue": "#42A5F5", "Purple": "#AB47BC",
            "White": "#FFFFFF", "Lime Green": "#C6FF00", "Pink": "#F06292", "Teal": "#26A69A",
            "Lavender": "#CE93D8", "Orange": "#FF9800", "Mint": "#80DEEA", "Yellow": "#FFFF00",
            "Red": "#F44336", "Blue": "#2196F3", "Green": "#4CAF50"
        }
        selected_color = get_color_from_hex(color_map.get(value, "#FFFFFF"))
        app.bg_color = selected_color  # Store in app for global access
        Window.clearcolor = selected_color
        self.background_color = selected_color
        self.color_field.text = value
        self.color_menu.dismiss()
        for screen_name in ["home", "edit"]:
            self.manager.get_screen(screen_name).update_background_color(selected_color)
        print(f"Background color changed to {value}")

    def change_font_size(self, instance, value):
        app = App.get_running_app()
        app.font_size = f"{value}sp"
        self.font_field.text = value
        self.font_menu.dismiss()
        print(f"Font size changed to {value}sp")

    def toggle_autosave(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'note_model'):
            app.note_model.set_autosave(value)
            print(f"Autosave {'enabled' if value else 'disabled'}")
        else:
            print("NoteModel not found")

    def go_back(self, instance):
        self.manager.current = "home"