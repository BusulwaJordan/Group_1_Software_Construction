from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivymd.uix.list import MDList
from kivymd.uix.list import MDListItem  # Updated to MDListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDIcon
from kivymd.icon_definitions import md_icons
import random
from kivy.utils import get_color_from_hex
import webbrowser
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.set_system_cursor("arrow")
        self.layout = FloatLayout()
        self.view_mode = "list"
        self.background_image = None
        self.background_color = get_color_from_hex("#FFFFFF")

        self.content_layout = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        top_layout = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        
        menu_btn = MDIconButton(icon="menu", size_hint_x=0.15, md_bg_color=get_color_from_hex("#26A69A"), padding=dp(5))
        menu_btn.bind(on_press=self.toggle_menu)
        menu_btn.bind(on_hover=self.change_cursor_pointer)
        menu_btn.bind(on_leave=self.change_cursor_default)
        top_layout.add_widget(menu_btn)

        self.search_input = MDTextField(
            hint_text="Search..",
            size_hint_x=0.55,
            mode="rectangle",
            fill_color_normal=get_color_from_hex("#FFFFFF"),
            line_color_normal=get_color_from_hex("#26A69A"),
            line_color_focus=get_color_from_hex("#26A69A")
        )
        self.search_input.radius = [15, 15, 15, 15]
        self.search_input.bind(text=self.on_search)
        self.search_input.bind(on_enter=self.change_cursor_default)
        self.search_input.bind(focus=self.on_search_focus)
        top_layout.add_widget(self.search_input)

        search_btn = MDIconButton(icon="magnify", size_hint_x=0.15, md_bg_color=get_color_from_hex("#26A69A"), padding=dp(5))
        search_btn.bind(on_press=self.perform_search)
        search_btn.bind(on_hover=self.change_cursor_pointer)
        search_btn.bind(on_leave=self.change_cursor_default)
        top_layout.add_widget(search_btn)

        self.view_toggle_btn = MDIconButton(icon="view-list", size_hint_x=0.15, md_bg_color=get_color_from_hex("#26A69A"), padding=dp(5))
        self.view_toggle_btn.bind(on_press=self.toggle_view_mode)
        self.view_toggle_btn.bind(on_hover=self.change_cursor_pointer)
        self.view_toggle_btn.bind(on_leave=self.change_cursor_default)
        top_layout.add_widget(self.view_toggle_btn)

        settings_btn = MDIconButton(icon="cog", size_hint_x=0.15, md_bg_color=get_color_from_hex("#26A69A"), padding=dp(5))
        settings_btn.bind(on_press=self.go_to_settings)
        settings_btn.bind(on_hover=self.change_cursor_pointer)
        settings_btn.bind(on_leave=self.change_cursor_default)
        top_layout.add_widget(settings_btn)

        self.content_layout.add_widget(top_layout)

        self.scroll = ScrollView()
        self.notes_list = MDList(spacing=dp(10), size_hint_y=None)
        self.notes_list.bind(minimum_height=self.notes_list.setter('height'))
        
        self.notes_grid = BoxLayout(orientation='horizontal', spacing=dp(20), padding=dp(20), size_hint_y=None, height=0)
        self.notes_grid.bind(minimum_height=self.notes_grid.setter('height'))
        
        self.scroll.add_widget(self.notes_list)
        self.content_layout.add_widget(self.scroll)

        btn_layout = BoxLayout(size_hint_y=0.1, spacing=dp(10), padding=[0, dp(10), 0, 0])
        refresh_btn = MDIconButton(icon="refresh", size_hint_x=0.15, md_bg_color=get_color_from_hex("#26A69A"), padding=dp(5))
        refresh_btn.bind(on_press=self.refresh_notes)
        refresh_btn.bind(on_hover=self.change_cursor_pointer)
        refresh_btn.bind(on_leave=self.change_cursor_default)
        btn_layout.add_widget(refresh_btn)
        self.content_layout.add_widget(btn_layout)

        create_btn = MDIconButton(icon="plus", size_hint=(None, None), size=(dp(60), dp(60)), md_bg_color=get_color_from_hex("#26A69A"), pos_hint={"right": 0.93, "y": 0.06})
        create_btn.bind(on_press=self.create_new_note)
        create_btn.bind(on_hover=self.change_cursor_pointer)
        create_btn.bind(on_leave=self.change_cursor_default)

        self.menu_layout = BoxLayout(orientation="vertical", size_hint=(0.675, 1.0), pos_hint={"x": -0.675, "y": 0}, padding=dp(10), spacing=dp(10))
        with self.menu_layout.canvas.before:
            Color(rgba=get_color_from_hex("#FFFFFF"))
            self.menu_bg = Rectangle(pos=self.menu_layout.pos, size=self.menu_layout.size)
        self.menu_layout.bind(pos=self.update_menu_bg, size=self.update_menu_bg)

        menu_list = MDList(spacing=dp(10), size_hint_y=None)
        menu_list.bind(minimum_height=menu_list.setter('height'))
        menu_items = [
            ("Favorite", "star", lambda x: print("Favorite selected")),
            ("Category", "folder", lambda x: print("Category selected")),
            ("Tags", "tag", lambda x: print("Tags selected")),
            ("Help Center", "help-circle", lambda x: print("Help Center selected"))
        ]

        for text, icon, callback in menu_items:
            item = MDListItem(  # Updated to MDListItem
                text=text,
                on_release=lambda x, cb=callback: self.on_menu_item_selected(cb),
                radius=[15, 15, 15, 15]
            )
            item.add_widget(MDIcon(
                icon=icon,
                pos_hint={"center_y": .5},
                theme_text_color="Custom",
                text_color=get_color_from_hex("#757575")
            ))
            item.bind(on_enter=self.change_cursor_pointer)
            item.bind(on_leave=self.change_cursor_default)
            menu_list.add_widget(item)

        menu_scroll = ScrollView(size_hint=(1, 1))
        menu_scroll.add_widget(menu_list)
        self.menu_layout.add_widget(menu_scroll)

        self.overlay = MDIconButton(icon="", size_hint=(1, 1), pos_hint={"x": 0, "y": 0}, opacity=0, disabled=True)
        self.overlay.bind(on_press=self.close_menu_on_outside_click)

        self.layout.add_widget(self.content_layout)
        self.layout.add_widget(self.menu_layout)
        self.layout.add_widget(self.overlay)
        self.layout.add_widget(create_btn)
        self.add_widget(self.layout)
        self.refresh_notes()
        self.menu_open = False

    def update_menu_bg(self, instance, value):
        self.menu_bg.pos = instance.pos
        self.menu_bg.size = instance.size

    def toggle_menu(self, instance):
        if not self.menu_open:
            anim = Animation(pos_hint={"x": 0, "y": 0}, duration=0.3)
            anim.start(self.menu_layout)
            self.overlay.disabled = False
            self.overlay.opacity = 0.3
            self.menu_open = True
        else:
            self.close_menu()

    def close_menu(self):
        if self.menu_open:
            anim = Animation(pos_hint={"x": -0.675, "y": 0}, duration=0.3)
            anim.start(self.menu_layout)
            self.overlay.opacity = 0
            self.overlay.disabled = True
            self.menu_open = False

    def close_menu_on_outside_click(self, instance):
        if self.menu_open:
            self.close_menu()

    def on_menu_item_selected(self, callback):
        callback(None)
        self.close_menu()

    def set_background_image(self, file_path):
        if self.background_image:
            self.layout.remove_widget(self.background_image)
        self.background_image = AsyncImage(source=file_path, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background_image, index=len(self.layout.children))

    def update_background_color(self, color):
        self.background_color = color
        Window.clearcolor = color
        if self.background_image:
            self.layout.remove_widget(self.background_image)
            self.background_image = None

    def on_search(self, instance, value):
        self.update_notes(value)

    def perform_search(self, instance):
        self.update_notes(self.search_input.text)

    def on_search_focus(self, instance, value):
        Window.set_system_cursor("ibeam" if value else "arrow")

    def change_cursor_pointer(self, instance):
        Window.set_system_cursor("hand")

    def change_cursor_default(self, instance):
        Window.set_system_cursor("arrow")

    def toggle_view_mode(self, instance):
        if self.view_mode == "list":
            self.view_mode = "grid"
            self.view_toggle_btn.icon = "view-grid"
            self.scroll.remove_widget(self.notes_list)
            self.scroll.add_widget(self.notes_grid)
        else:
            self.view_mode = "list"
            self.view_toggle_btn.icon = "view-list"
            self.scroll.remove_widget(self.notes_grid)
            self.scroll.add_widget(self.notes_list)
        self.update_notes(self.search_input.text)

    def animate_card(self, widget):
        anim = Animation(elevation=8, duration=0.2) + Animation(elevation=4, duration=0.2)
        anim.start(widget)

    def refresh_notes(self, instance=None):
        app = App.get_running_app()
        if hasattr(app, 'note_model'):
            app.note_model.load_notes()
            self.update_notes()
        else:
            print("NoteModel not found in app")

    def update_notes(self, query=""):
        if self.view_mode == "list":
            self.notes_list.clear_widgets()
        else:
            self.notes_grid.clear_widgets()
            
        app = App.get_running_app()
        if not hasattr(app, 'note_model'):
            print("NoteModel not found")
            return
        
        try:
            notes = app.note_model.search_notes(query) if query else app.note_model.notes
        except Exception as e:
            print(f"Error updating notes: {e}")
            return
        
        tile_colors = ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#D1C4E9", "#C5CAE9",
                       "#BBDEFB", "#B3E5FC", "#B2EBF2", "#B2DFDB", "#C8E6C9"]
        
        for note_id, note_data in notes.items():
            timestamp = note_data.get("created_at", "Unknown")[:19]
            color = note_data.get("bg_color", random.choice(tile_colors))
            
            if self.view_mode == "list":
                item = MDListItem(  # Updated to MDListItem
                    text=f"{note_data['title']} ({timestamp})",
                    on_release=lambda x, nid=note_id: self.view_note(nid),
                    md_bg_color=get_color_from_hex(color),  # Updated to md_bg_color
                    radius=[15, 15, 15, 15],
                )
                item.add_widget(MDIcon(
                    icon="note-text",
                    pos_hint={"center_y": .5},
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#757575")
                ))
                item.bind(on_enter=self.change_cursor_pointer)
                item.bind(on_leave=self.change_cursor_default)
                more_btn = MDIconButton(
                    icon="dots-vertical",
                    pos_hint={"center_y": .5, 'center_x': .95},
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#757575"),
                    size_hint=(None, None),
                    size=(dp(48), dp(48)),
                )
                more_btn.bind(on_release=lambda instance, nid=note_id: self.show_options(instance, nid))
                more_btn.bind(on_enter=self.change_cursor_pointer)
                more_btn.bind(on_leave=self.change_cursor_default)
                item.add_widget(more_btn)
                self.notes_list.add_widget(item)
            else:
                card = MDCard(size_hint=(None, None), size=(dp(220), dp(280)), padding=dp(15), spacing=dp(10),
                              orientation='vertical', elevation=4, radius=[20, 20, 20, 20], md_bg_color=get_color_from_hex(color),
                              ripple_behavior=True)
                title = MDLabel(text=note_data['title'], size_hint=(1, None), height=dp(40), font_style="H6",
                                font_size=dp(18), halign="left", color=get_color_from_hex("#333333"))
                card.add_widget(title)
                content_preview = note_data.get('content', 'No content')[:60] + ('...' if len(note_data.get('content', '')) > 60 else '')
                content = MDLabel(text=content_preview, size_hint=(1, 1), font_size=dp(14), halign="left",
                                  color=get_color_from_hex("#333333"))
                card.add_widget(content)
                time_label = MDLabel(text=timestamp, size_hint=(1, None), height=dp(30), font_size=dp(12),
                                    halign="left", color=get_color_from_hex("#666666"))
                card.add_widget(time_label)
                btn_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(15), padding=[dp(5), 0, dp(5), 0])
                view_btn = MDIconButton(icon="eye", pos_hint={"center_y": .5}, md_bg_color=get_color_from_hex("#26A69A"))
                view_btn.bind(on_release=lambda x, nid=note_id: self.view_note(nid))
                view_btn.bind(on_enter=self.change_cursor_pointer)
                view_btn.bind(on_leave=self.change_cursor_default)
                btn_layout.add_widget(view_btn)
                more_btn = MDIconButton(icon="dots-vertical", pos_hint={"center_y": .5}, md_bg_color=get_color_from_hex("#757575"))
                more_btn.bind(on_release=lambda instance, nid=note_id: self.show_options(instance, nid))
                more_btn.bind(on_enter=self.change_cursor_pointer)
                more_btn.bind(on_leave=self.change_cursor_default)
                btn_layout.add_widget(more_btn)
                card.add_widget(btn_layout)
                card.bind(on_enter=lambda x: self.animate_card(card))
                card.bind(on_enter=self.change_cursor_pointer)
                card.bind(on_leave=self.change_cursor_default)
                self.notes_grid.add_widget(card)

    def show_options(self, instance, note_id):
        menu_items = [
            {"text": "Share", "icon": "share-variant", "on_release": lambda x=note_id: self.share_note(x)},
            {"text": "Delete", "icon": "delete", "on_release": lambda x=note_id: self.delete_note(x)},
            {"text": "Archive", "icon": "archive", "on_release": lambda x=note_id: self.archive_note(x)}
        ]
        self.menu = MDDropdownMenu(caller=instance, items=menu_items, width_mult=4, max_height=dp(200),
                                   border_margin=dp(10), padding=dp(10), position="auto", elevation=2)
        self.menu.open()

    def share_note(self, note_id):
        app = App.get_running_app()
        note = app.note_model.notes.get(note_id)
        if note:
            title = note.get("title", "Untitled")
            content = note.get("content", "No content")
            share_text = f"{title}\n\n{content}"
            encoded_text = share_text.replace("\n", "%0A").replace(" ", "%20")
            share_urls = {
                "Facebook": ("facebook", f"https://www.facebook.com/sharer/sharer.php?u={encoded_text}"),
                "WhatsApp": ("whatsapp", f"https://wa.me/?text={encoded_text}"),
                "Twitter": ("twitter", f"https://twitter.com/intent/tweet?text={encoded_text}")
            }
            self.show_share_dialog(share_urls)
        self.menu.dismiss()

    def show_share_dialog(self, share_urls):
        buttons = []
        for platform, (icon, url) in share_urls.items():
            item = MDListItem(  # Updated to MDListItem
                text=platform,
                on_release=lambda x, u=url: webbrowser.open(u)
            )
            item.add_widget(MDIcon(
                icon=icon,
                pos_hint={"center_y": .5},
                theme_text_color="Custom",
                text_color=get_color_from_hex("#757575")
            ))
            buttons.append(item)
        cancel_item = MDListItem(  # Updated to MDListItem
            text="Cancel",
            on_release=lambda x: self.menu.dismiss()
        )
        cancel_item.add_widget(MDIcon(
            icon="close",
            pos_hint={"center_y": .5},
            theme_text_color="Custom",
            text_color=get_color_from_hex("#757575")
        ))
        buttons.append(cancel_item)
        dialog = MDDialog(title="Share Note", type="simple", items=buttons)
        dialog.open()

    def delete_note(self, note_id):
        app = App.get_running_app()
        try:
            success = app.note_model.delete_note(note_id)
            if success:
                self.update_notes()
                print(f"Note {note_id} deleted successfully")
                self.show_undo_popup(note_id)
            else:
                print(f"Failed to delete note {note_id}")
        except Exception as e:
            print(f"Error deleting note {note_id}: {e}")
        self.menu.dismiss()

    def show_undo_popup(self, note_id):
        dialog = MDDialog(
            title="Note Deleted",
            text="Would you like to undo this action?",
            buttons=[
                MDButton(text="Undo", md_bg_color=get_color_from_hex("#26A69A"), on_release=lambda x: self.undo_last_delete(note_id)),
                MDButton(text="Dismiss", on_release=lambda x: dialog.dismiss())
            ],
            auto_dismiss=False,
            size_hint=(0.7, 0.3)
        )
        dialog.open()

    def undo_last_delete(self, note_id):
        app = App.get_running_app()
        try:
            restored_id = app.note_model.undo_delete()
            if restored_id:
                self.update_notes()
                print(f"Restored note {restored_id}")
            else:
                print("Undo failed")
        except Exception as e:
            print(f"Error undoing delete: {e}")

    def archive_note(self, note_id):
        app = App.get_running_app()
        try:
            success = app.note_model.archive_note(note_id)
            if success:
                self.update_notes()
                print(f"Note {note_id} archived successfully")
            else:
                print(f"Failed to archive note {note_id}")
        except Exception as e:
            print(f"Error archiving note {note_id}: {e}")
        self.menu.dismiss()

    def view_note(self, note_id):
        self.manager.get_screen("edit").load_note(note_id)
        self.manager.current = "edit"

    def create_new_note(self, instance=None):
        self.manager.get_screen("edit").load_new_note()
        self.manager.current = "edit"

    def go_to_settings(self, instance):
        self.manager.current = "settings"