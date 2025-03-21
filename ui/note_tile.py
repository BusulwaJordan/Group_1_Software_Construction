from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonIcon, MDButtonText
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle, Line
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
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])  # Increased from 10 to 20
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
        edit_btn = MDButton(
            MDButtonIcon(icon="pencil"),
            MDButtonText(text="Edit"),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.edit_note()
        )
        delete_btn = MDButton(
            MDButtonIcon(icon="delete"),
            MDButtonText(text="Delete"),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.screen.delete_note(self.note_id) or dropdown.dismiss()
        )
        share_btn = MDButton(
            MDButtonIcon(icon="share"),
            MDButtonText(text="Share"),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.screen.share_email(self.note_content) or dropdown.dismiss()
        )
        pin_btn = MDButton(
            MDButtonIcon(icon="pin"),
            MDButtonText(text="Pin"),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.screen.pin_note(self.note_id) or dropdown.dismiss()
        )
        dropdown.add_widget(edit_btn)
        dropdown.add_widget(delete_btn)
        dropdown.add_widget(share_btn)
        dropdown.add_widget(pin_btn)
        dropdown.open(self.options_btn)

    def edit_note(self):
        from kivy.uix.popup import Popup
        popup = Popup(title="Edit Note", size_hint=(0.8, 0.6))
        layout = BoxLayout(orientation='vertical', padding=dp(10))
        title_input = TextInput(text=self.note_title, multiline=False, size_hint_y=None, height=dp(40))
        content_input = TextInput(text=self.note_content, multiline=True)
        save_btn = MDButton(
            MDButtonIcon(icon="check"),
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
            MDButtonIcon(icon="arrow-left"),
            MDButtonText(text="Back"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(30)),
            md_bg_color='#FF6F61',
            on_release=self.go_back
        )
        top_bar.add_widget(back_btn)
        self.layout.add_widget(top_bar)
        
        self.content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        with self.content_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.border_rect = RoundedRectangle(pos=self.content_layout.pos, size=self.content_layout.size, radius=[10])
        self.border_line = Line(rounded_rectangle=(self.content_layout.x, self.content_layout.y, 
                                                  self.content_layout.width, self.content_layout.height, 10), width=1)
        with self.content_layout.canvas.after:
            Color(0.7, 0.7, 0.7, 1)
            self.content_layout.canvas.after.add(self.border_line)
        self.content_layout.bind(pos=self.update_border, size=self.update_border)
        
        self.title_label = Label(
            text="",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40),
            font_size=18,
            bold=True,
            text_size=(Window.width - dp(40), None),
            halign='left',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.content_layout.add_widget(self.title_label)
        
        self.content_label = Label(
            text="",
            color=(0, 0, 0, 1),
            size_hint=(1, 1),
            text_size=(Window.width - dp(40), None),
            halign='left',
            valign='top'
        )
        self.content_label.bind(size=self.content_label.setter('text_size'))
        self.content_layout.add_widget(self.content_label)
        
        bottom_bar = BoxLayout(size_hint_y=None, height=dp(40))
        edit_btn = MDButton(
            MDButtonIcon(icon="pencil"),
            MDButtonText(text="Edit"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(30)),
            md_bg_color='#88B04B',
            pos_hint={'center_x': 0.5},
            on_release=self.edit_note
        )
        bottom_bar.add_widget(edit_btn)
        self.content_layout.add_widget(bottom_bar)
        
        self.layout.add_widget(self.content_layout)
        self.add_widget(self.layout)
        self.note_id = None

    def set_note(self, note_id, title, content):
        self.note_id = note_id
        self.title_label.text = title
        self.content_label.text = content
        self.content_label.height = self.content_label.texture_size[1]

    def update_border(self, instance, value):
        self.border_rect.pos = instance.pos
        self.border_rect.size = instance.size
        self.border_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 10)

    def go_back(self, instance):
        self.manager.current = 'main'

    def edit_note(self, instance):
        from kivy.uix.popup import Popup
        popup = Popup(title="Edit Note", size_hint=(0.8, 0.6))
        layout = BoxLayout(orientation='vertical', padding=dp(10))
        title_input = TextInput(text=self.title_label.text, multiline=False, size_hint_y=None, height=dp(40))
        content_input = TextInput(text=self.content_label.text, multiline=True)
        save_btn = MDButton(
            MDButtonIcon(icon="check"),
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
        if self.main_screen and self.note_id:
            self.main_screen.edit_note(self.note_id, new_content, new_title)
            self.title_label.text = new_title
            self.content_label.text = new_content
            self.content_label.height = self.content_label.texture_size[1]
        popup.dismiss()