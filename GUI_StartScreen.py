from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial

class StartScreen(Widget):
    def __init__(self, parent, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.txt_dict = {'welcome': 'Welcome to Spectro',
                         'description': 'This application allows you to create spectrograms from signal gathered directly from your microphone.',
                         'source': 'Please configure options or start analysis: ',
                         'madeby': 'Made by Radosław Sawicki\nPolitechnika Wrocławska\nWrocław 2020'}
        self.parent_widget = parent
        self.font_size_desc = 15
        self.font_size_title = 40
        self.WINDOW_HEIGHT = int(self.parent_widget.getOptions().get('wheight'))
        #  self.WINDOW_HEIGHT = 800
        self.WINDOW_WIDTH = int(self.parent_widget.getOptions().get('wwidth'))
        #  self.WINDOW_WIDTH = 1000

        self.layout_start = BoxLayout()
        self.layout_start.orientation = 'vertical'
        self.layout_start.height = self.WINDOW_HEIGHT
        self.layout_start.width = self.WINDOW_WIDTH

        self.add_welcome()
        self.add_buttons()
        self.add_signature()

        self.add_widget(self.layout_start)

    def add_welcome(self):
        layout_welcome = BoxLayout()
        layout_welcome.orientation = 'vertical'
        layout_welcome.size_hint = (1.0, 0.2)

        textbox_welcome = Label(font_size=self.font_size_title, text=self.txt_dict['welcome'])
        textbox_welcome.size_hint = (1.0, 0.7)
        textbox_description = Label(font_size=self.font_size_desc, text=self.txt_dict['description'])
        textbox_description.size_hint = (1.0, 0.15)
        textbox_source = Label(font_size=self.font_size_desc, text=self.txt_dict['source'])
        textbox_source.size_hint = (1.0, 0.15)

        layout_welcome.add_widget(textbox_welcome)
        layout_welcome.add_widget(textbox_description)
        layout_welcome.add_widget(textbox_source)

        self.layout_start.add_widget(layout_welcome)

    def add_buttons(self):
        layout_buttons = BoxLayout()
        layout_buttons.orientation = 'horizontal'
        layout_buttons.size_hint = (1.0, 0.7)
        # layout_buttons.spacing = int(WINDOW_WIDTH/4)
        layout_buttons.padding = [50, int(self.WINDOW_HEIGHT / 6), 50, int(self.WINDOW_HEIGHT / 3)]

        button_file = Button(text="OPTIONS")
        button_file.size_hint = (0.3, 0.5)
        button_file.bind(on_press=partial(self.show_options, button_file))

        button_mic = Button(text="START")
        button_mic.size_hint = (0.3, 0.5)
        button_mic.bind(on_press=partial(self.use_mic, button_mic))

        layout_buttons.add_widget(button_file)
        layout_buttons.add_widget(button_mic)

        self.layout_start.add_widget(layout_buttons)

    def add_signature(self):
        signature_layout = BoxLayout()
        signature_layout.orientation = 'horizontal'
        signature_layout.size_hint = (1.0, 0.1)
        signature_layout.padding = [self.WINDOW_WIDTH - signature_layout.width - 50, 0, 0, 0]

        textbox_madeby = Label(halign='right', valign='bottom', font_size=10, text=self.txt_dict['madeby'])
        textbox_madeby.size_hint = (1.0, 1.0)
        signature_layout.add_widget(textbox_madeby)
        self.layout_start.add_widget(signature_layout)

    def show_options(self, instance, *args):
        self.parent_widget.show_options()

    def use_mic(self, instance, *args):
        self.parent_widget.show_mic()