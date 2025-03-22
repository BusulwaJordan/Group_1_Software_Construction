from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonIcon, MDButtonText
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
import datetime

class NoteTile(BoxLayout):
    note_content = StringProperty('')
    note_id = StringProperty('')
    note_title = StringProperty('')
    
    def __init__(self, content, note_id, color, timestamp, title, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(80)
        self.size_hint_x = None
        self.width = dp(340)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.pos_hint = {'center_x': 0.5}
        with self.canvas.before:
            Color(rgb=[int(color[i:i+2], 16)/255 for i in (1, 3, 5)])
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.note_content = content
        self.note_id = note_id
        self.note_title = title
        
        self.add_widget(Label(text=title[:30] + "..." if len(title) > 30 else title, 
                             color=(1,1,1,1), size_hint_y=None, height=dp(40)))
        
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        date_label = Label(text=date_str, font_size=12, color=(1,1,1,0.7), 
                          size_hint_x=0.7, halign='left', valign='middle')
        date_label.bind(size=date_label.setter('text_size'))
        bottom_layout.add_widget(date_label)
        
        self.options_btn = MDIconButton(icon="dots-vertical", size_hint=(None, None), size=(dp(30), dp(30)),
                                       pos_hint={'right': 1}, on_release=self.show_options)
        bottom_layout.add_widget(self.options_btn)
        
        self.add_widget(bottom_layout)
        
        self.bind(on_touch_down=self.on_tile_click)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_tile_click(self, instance, touch):
        if self.options_btn.collide_point(*touch.pos):
            return False
        if self.collide_point(*touch.pos) and touch.button == 'left':
            self.screen.manager.get_screen('note_view').set_note(self.note_id, self.note_title, self.note_content)
            self.screen.manager.current = 'note_view'
            return True
        return False

    def show_options(self, instance):
        from kivy.uix.dropdown import DropDown
        dropdown = DropDown()
        for text, icon, action in [("Edit", "pencil", self.edit_note),
                                  ("Delete", "delete", lambda x: self.screen.delete_note(self.note_id)),
                                  ("Pin", "pin", lambda x: self.screen.pin_note(self.note_id))]:
            btn = MDButton(
                MDButtonIcon(icon=icon),
                MDButtonText(text=text),
                size_hint_y=None,
                height=dp(40),
                on_release=action or dropdown.dismiss
            )
            dropdown.add_widget(btn)
        dropdown.open(self.options_btn)

    def edit_note(self, *args):
        from kivy.uix.popup import Popup
        popup = Popup(title="Edit Note", size_hint=(0.8, 0.6))
        layout = BoxLayout(orientation='vertical', padding=dp(10))
        title_input = TextInput(text=self.note_title, multiline=False, size_hint_y=None, height=dp(40))
        content_input = TextInput(text=self.note_content, multiline=True)
        save_btn = MDButton(
            MDButtonText(text="Save"),
            style="elevated",
            md_bg_color='#88B04B',
            on_release=lambda x: self.save_edit(title_input.text, content_input.text, popup)
        )
        layout.add_widget(title_input)
        layout.add_widget(content_input)
        layout.add_widget(save_btn)
        popup.content = layout
        popup.open()

    def save_edit(self, new_title, new_content, popup):
        self.screen.edit_note(self.note_id, new_content, new_title)
        self.note_title = new_title
        self.note_content = new_content
        popup.dismiss()

class NoteViewScreen(Screen):
    def __init__(self, main_screen=None, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.layout = BoxLayout(orientation='vertical', padding=dp(5), spacing=dp(5))
        
        top_bar = BoxLayout(size_hint_y=None, height=dp(40))
        back_btn = MDButton(
            MDButtonText(text="Back"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(30)),
            md_bg_color='#FF6F61',
            on_release=self.go_back
        )
        top_bar.add_widget(back_btn)
        self.layout.add_widget(top_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', padding=dp(10))
        with self.content_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = RoundedRectangle(pos=self.content_layout.pos, size=self.content_layout.size, radius=[10])
        self.content_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        self.title_label = Label(text="", color=(0, 0, 0, 1), size_hint_y=None, height=dp(40), font_size=18, bold=True)
        self.content_label = Label(text="", color=(0, 0, 0, 1), size_hint_y=None, height=dp(100))
        self.content_layout.add_widget(self.title_label)
        self.content_layout.add_widget(self.content_label)
        
        self.layout.add_widget(self.content_layout)
        self.add_widget(self.layout)
        self.note_id = None

    def set_note(self, note_id, title, content):
        self.note_id = note_id
        self.title_label.text = title
        self.content_label.text = content
        self.content_label.height = self.content_label.texture_size[1]

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'main'