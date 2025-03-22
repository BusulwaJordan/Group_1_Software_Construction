from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonIcon, MDButtonText
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle
import datetime
import webbrowser
from urllib.parse import quote

class NoteTile(BoxLayout):
    note_content = StringProperty('')
    note_id = StringProperty('')
    note_title = StringProperty('')
    note_tags = ListProperty([])
    
    def __init__(self, content, note_id, color, timestamp, title, tags, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(120)
        self.size_hint_x = 1
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        with self.canvas.before:
            Color(rgb=[int(color[i:i+2], 16)/255 for i in (1, 3, 5)])
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.note_content = content
        self.note_id = note_id
        self.note_title = title
        self.note_tags = tags
        
        self.title_label = Label(
            text=title[:25] + "..." if len(title) > 25 else title,
            color=(1, 1, 1, 1),
            font_size=16,
            bold=True,
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.add_widget(self.title_label)
        
        self.content_label = Label(
            text=content[:50] + "..." if len(content) > 50 else content,
            color=(1, 1, 1, 0.8),
            font_size=12,
            size_hint_y=None,
            height=dp(40),
            halign='left',
            valign='top'
        )
        self.content_label.bind(size=self.content_label.setter('text_size'))
        self.add_widget(self.content_label)
        
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        date_label = Label(
            text=date_str,
            font_size=10,
            color=(1, 1, 1, 0.6),
            size_hint_x=0.6,
            halign='left',
            valign='middle'
        )
        date_label.bind(size=date_label.setter('text_size'))
        bottom_layout.add_widget(date_label)
        
        self.options_btn = MDIconButton(
            icon="dots-vertical",
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            on_release=self.show_options
        )
        self.share_btn = MDIconButton(
            icon="share",
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            on_release=self.show_share_options
        )
        bottom_layout.add_widget(self.options_btn)
        bottom_layout.add_widget(self.share_btn)
        
        self.add_widget(bottom_layout)
        self.bind(on_touch_down=self.on_tile_click)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_tile_click(self, instance, touch):
        if any(btn.collide_point(*touch.pos) for btn in [self.options_btn, self.share_btn]):
            return False
        if self.collide_point(*touch.pos) and touch.button == 'left':
            self.screen.manager.get_screen('note_view').set_note(self.note_id, self.note_title, self.note_content, self.note_tags)
            self.screen.manager.current = 'note_view'
            return True
        return False

    def show_options(self, instance):
        from kivy.uix.dropdown import DropDown
        dropdown = DropDown()
        for text, icon, action in [
            ("Edit", "pencil", self.edit_note),
            ("Delete", "delete", lambda x: self.screen.delete_note(self.note_id)),
            ("Pin", "pin", lambda x: self.screen.pin_note(self.note_id))
        ]:
            btn = MDButton(
                MDButtonIcon(icon=icon),
                MDButtonText(text=text),
                size_hint_y=None,
                height=dp(40),
                on_release=action or dropdown.dismiss
            )
            dropdown.add_widget(btn)
        dropdown.open(instance)

    def show_share_options(self, instance):
        from kivy.uix.dropdown import DropDown
        dropdown = DropDown()
        platforms = [
            ("X", "twitter", f"https://twitter.com/intent/tweet?text={quote(self.note_content)}"),
            ("Facebook", "facebook", f"https://www.facebook.com/sharer/sharer.php?u={quote('Note from Q-NOTE')}&quote={quote(self.note_content)}"),
            ("Instagram", "instagram", None),
            ("Threads", "web", f"https://threads.net/intent/post?text={quote(self.note_content)}")
        ]
        for platform, icon, url in platforms:
            btn = MDButton(
                MDButtonIcon(icon=icon),
                MDButtonText(text=platform),
                size_hint_y=None,
                height=dp(40),
                on_release=lambda x, u=url: self.share_to_platform(u) if u else self.show_instagram_popup()
            )
            dropdown.add_widget(btn)
        dropdown.open(instance)

    def share_to_platform(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            Popup(title="Error", content=Label(text=f"Failed to share: {e}"), size_hint=(0.8, 0.4)).open()

    def show_instagram_popup(self):
        popup = Popup(title="Instagram Share", size_hint=(0.8, 0.4))
        layout = BoxLayout(orientation='vertical', padding=dp(10))
        layout.add_widget(Label(text="Instagram doesn’t support direct sharing. Copy the note content and paste it manually."))
        layout.add_widget(MDButton(
            MDButtonText(text="OK"),
            style="elevated",
            md_bg_color='#88B04B',
            on_release=lambda x: popup.dismiss()
        ))
        popup.content = layout
        popup.open()

    def edit_note(self, *args):
        popup = Popup(title="Edit Note", size_hint=(0.8, 0.6))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        title_input = TextInput(text=self.note_title, multiline=False, size_hint_y=None, height=dp(40))
        content_input = TextInput(text=self.note_content, multiline=True)
        tags_input = TextInput(text=', '.join(self.note_tags), hint_text="Tags (e.g., @friend)", size_hint_y=None, height=dp(40))
        save_btn = MDButton(
            MDButtonText(text="Save"),
            style="elevated",
            md_bg_color='#88B04B',
            on_release=lambda x: self.save_edit(title_input.text, content_input.text, tags_input.text, popup)
        )
        layout.add_widget(title_input)
        layout.add_widget(content_input)
        layout.add_widget(tags_input)
        layout.add_widget(save_btn)
        popup.content = layout
        popup.open()

    def save_edit(self, new_title, new_content, new_tags, popup):
        tags_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
        self.screen.edit_note(self.note_id, new_content, new_title, tags_list)
        self.note_title = new_title
        self.note_content = new_content
        self.note_tags = tags_list
        self.title_label.text = new_title[:25] + "..." if len(new_title) > 25 else new_title
        self.content_label.text = new_content[:50] + "..." if len(new_content) > 50 else new_content
        popup.dismiss()

class NoteViewScreen(Screen):
    def __init__(self, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        header = BoxLayout(size_hint_y=None, height=dp(60))
        back_btn = MDButton(
            MDButtonText(text="Back"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            md_bg_color='#FF6F61',
            on_release=self.go_back
        )
        self.title_label = Label(
            text="",
            color=(0, 0, 0, 1),
            font_size=20,
            bold=True,
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        header.add_widget(back_btn)
        header.add_widget(self.title_label)
        self.layout.add_widget(header)
        
        scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', padding=dp(10), size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.content_label = Label(
            text="",
            color=(0, 0, 0, 1),
            font_size=16,
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(self.width - dp(20), None)
        )
        self.content_label.bind(texture_size=self.content_label.setter('size'))
        self.content_layout.add_widget(self.content_label)
        scroll.add_widget(self.content_layout)
        self.layout.add_widget(scroll)
        
        self.tags_label = Label(
            text="",
            color=(0, 0, 0, 0.7),
            font_size=14,
            size_hint_y=None,
            height=dp(30),
            halign='left',
            valign='middle'
        )
        self.tags_label.bind(size=self.tags_label.setter('text_size'))
        self.layout.add_widget(self.tags_label)
        
        self.add_widget(self.layout)
        self.note_id = None

    def set_note(self, note_id, title, content, tags):
        self.note_id = note_id
        self.title_label.text = title
        self.content_label.text = content
        self.content_label.height = self.content_label.texture_size[1]
        self.tags_label.text = "Tags: " + (', '.join(tags) if tags else "None")

    def go_back(self, instance):
        self.manager.current = 'main'