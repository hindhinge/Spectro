from kivy import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.graphics import *
from functools import partial
from math import log2
from kivy.core.window import Window
#############################TODO TODO
# - Opcje powinny znaleźć się w osobnej klasie jako globale (albo w obiekcie, nie iwem co lepiej)
# - Opcje do ustawiania: widow height, window width, spec line widh, spec width, spec height
#   wyświetlanie w skali lin-lin, lin-log częstotliuwoście, wyświetlanie w decybelach i wyświetlanie liniowe,
#   okienkowanie blackmana, zakres min i max wartość db (chyba że wybierzemy wyświetlanie liniowe, to min i max dla linioweog)
# - font size zależny od window width
# - spacer boxy do color values
# - obsługa back button i zapisanie opcij

class OptionsScreen(Widget):
    def __init__(self, parent, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        self.parent_widget = parent
        self.WINDOW_HEIGHT = int(self.parent_widget.getOptions().get('wheight'))
        # # self.WINDOW_HEIGHT = 800
        self.WINDOW_WIDTH = int(self.parent_widget.getOptions().get('wwidth'))
        # # self.WINDOW_WIDTH = 1000
        self.text_titles = {'dim':'Dimensions',
                            'spec':'Spectrogram',
                            'rec':'Recording'}

        self.input_fields = dict()

        self.errorLabel = Label(text = '')
        self.errorLabel.size_hint = (0.9,1.0)
        self.errorLabel.font_size = 10

        self.noEmptyFieldsLast = None

        self.layout_options = BoxLayout()
        self.layout_options.orientation = 'vertical'
        self.layout_options.width = self.WINDOW_WIDTH
        self.layout_options.height = self.WINDOW_HEIGHT
        self.layout_options.size_hint_max_x = self.WINDOW_WIDTH
        self.layout_options.size_hint_min_x = self.WINDOW_WIDTH
        self.layout_options.size_hint_max_y = self.WINDOW_HEIGHT
        self.layout_options.size_hint_min_y = self.WINDOW_HEIGHT
        self.layout_options.spacing = int(self.WINDOW_HEIGHT*0.05)

        self.layout_dimensions = BoxLayout()
        self.layout_spectro = BoxLayout()
        self.layout_recording = BoxLayout()

        self.sectionDimensions()
        self.sectionSpectro()
        self.sectionRecording()
        self.sectionBackButton()
        self.fillValues()

        self.add_widget(self.layout_options)

    def setDimensions(self,width,height):
        self.WINDOW_HEIGHT = height
        self.WINDOW_WIDTH = width
        self.height = self.WINDOW_HEIGHT
        self.width = self.WINDOW_WIDTH
        self.layout_options.width = self.WINDOW_WIDTH
        self.layout_options.height = self.WINDOW_HEIGHT
        self.layout_options.size_hint_max_x = self.WINDOW_WIDTH
        self.layout_options.size_hint_min_x = self.WINDOW_WIDTH
        self.layout_options.size_hint_max_y = self.WINDOW_HEIGHT
        self.layout_options.size_hint_min_y = self.WINDOW_HEIGHT

    def sectionSpectro(self):
        self.layout_spectro.orientation = 'vertical'
        self.layout_spectro.size_hint = (1.0, 0.33)

        box_title = BoxLayout()
        box_title.orientation = 'horizontal'
        box_title.size_hint = (1.0, 0.2)
        box_title.add_widget(Label(text = self.text_titles['spec']))
        self.layout_spectro.add_widget(box_title)

        box_options = BoxLayout()
        box_options.orientation = 'horizontal'
        box_options.size_hint = (1.0, 0.8)
        self.layout_spectro.add_widget(box_options)

        box_options_titles = ['Scales', 'Window function', 'Color Values']
        box_options_children = []
        for i in range(3):
            child = BoxLayout()
            child.orientation = 'vertical'
            child.size_hint = (0.2, 1.0)
            child.id = box_options_titles[i]
            title = Label()
            title.size_hint = (1.0,0.1)
            title.text = box_options_titles[i]
            child.add_widget(title)
            self.fillOptions(child)
            box_options_children.append(child)
            box_options.add_widget(child)

        self.layout_options.add_widget(self.layout_spectro)
    def sectionRecording(self):
        self.layout_recording.orientation = 'vertical'
        self.layout_recording.size_hint = (1.0, 0.15)

        box_title = BoxLayout()
        box_title.orientation = 'horizontal'
        box_title.size_hint = (1.0, 0.2)
        box_title.add_widget(Label(text = self.text_titles['rec']))
        self.layout_recording.add_widget(box_title)

        box_options = BoxLayout()
        box_options.orientation = 'horizontal'
        box_options.size_hint = (1.0, 0.8)
        self.layout_recording.add_widget(box_options)

        value_names = {'0' : 'Chunk length',
                       '1' : 'Channels',
                       '2' : 'Sampling rate'}

        boxes = self.getOptionsLayout(3, 0.8)
        for lines in boxes:
            for child in lines.children:
                if child.id == 'text':
                    label = Label()
                    label.text = value_names[lines.id]
                    child.add_widget(label)

                if child.id == 'values':
                    textbox = TextInput()
                    textbox.text = '0'
                    textbox.multiline = False
                    textbox.size_hint = (1.0, 0.25)
                    if lines.id == '0':
                        self.input_fields['chunk'] = textbox
                    if lines.id == '1':
                        self.input_fields['channels'] = textbox
                    if lines.id == '2':
                        self.input_fields['fs'] = textbox
                    spacer_top = BoxLayout()
                    spacer_top.size_hint = (1.0, 0.35)
                    spacer_bot = BoxLayout()
                    spacer_bot.size_hint = (1.0, 0.35)
                    child.add_widget(spacer_top)
                    child.add_widget(textbox)
                    child.add_widget(spacer_bot)

            box_options.add_widget(lines)


        self.layout_options.add_widget(self.layout_recording)
    def sectionDimensions(self):
        self.layout_dimensions.orientation = 'vertical'
        self.layout_dimensions.size_hint = (1.0,0.33)

        box_title =BoxLayout()
        box_title.orientation = 'horizontal'
        box_title.size_hint = (1.0,0.2)
        box_title.add_widget(Label(text = self.text_titles['dim']))
        self.layout_dimensions.add_widget(box_title)

        box_options = BoxLayout()
        box_options.orientation = 'horizontal'
        box_options.size_hint = (1.0,0.8)
        self.layout_dimensions.add_widget(box_options)

        box_options_titles = ['Window', 'Spectrogram', 'Lines']
        box_options_children = []
        for i in range(3):
            child = BoxLayout()
            child.orientation = 'vertical'
            child.size_hint = (0.33, 1.0)
            child.id = box_options_titles[i]
            title = Label()
            title.size_hint = (1.0,0.1)
            title.text = box_options_titles[i]
            child.add_widget(title)
            self.fillOptions(child)
            box_options_children.append(child)
            box_options.add_widget(child)


        self.layout_options.add_widget(self.layout_dimensions)

    def sectionBackButton(self):
        box_bottom = BoxLayout()
        box_bottom.orientation = 'horizontal'
        box_bottom.size_hint = (1.0,0.05)

        backbutton = Button()
        backbutton.text = "BACK"
        backbutton.size_hint = (0.1,1.0)
        backbutton.pos_hint['left'] = 0.0
        backbutton.bind(on_press=partial(self.backButtonPress, backbutton))

        self.errorLabel.text = 'Information about errors will show up here'
        box_bottom.add_widget(backbutton)
        box_bottom.add_widget(self.errorLabel)
        self.layout_options.add_widget(box_bottom)
    
    def fillOptions(self,box):

        if box.id == 'Window':
            boxes = self.getOptionsLayout(2,0.8)
            for lines in boxes:
                for child in lines.children:
                    if child.id == 'text' and lines.id == '0':
                        label = Label()
                        label.text = 'Spectrogram width'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '0':
                        textbox = TextInput()
                        textbox.text = '0'
                        textbox.multiline = False
                        textbox.size_hint = (1.0, 0.25)
                        self.input_fields['swidth'] = textbox
                        spacer_top = BoxLayout()
                        spacer_top.size_hint = (1.0, 0.35)
                        spacer_bot = BoxLayout()
                        spacer_bot.size_hint = (1.0, 0.35)
                        child.add_widget(spacer_top)
                        child.add_widget(textbox)
                        child.add_widget(spacer_bot)
                    if child.id == 'text' and lines.id == '1':
                        label = Label()
                        label.text = 'Spectrogram height'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '1':
                        textbox = TextInput()
                        textbox.text = '1'
                        textbox.multiline = False
                        textbox.size_hint = (1.0, 0.25)
                        self.input_fields['sheight'] = textbox
                        spacer_top = BoxLayout()
                        spacer_top.size_hint = (1.0, 0.35)
                        spacer_bot = BoxLayout()
                        spacer_bot.size_hint = (1.0, 0.35)
                        child.add_widget(spacer_top)
                        child.add_widget(textbox)
                        child.add_widget(spacer_bot)
                box.add_widget(lines)

        if box.id == 'Spectrogram':
            boxes = self.getOptionsLayout(2,0.8)
            for lines in boxes:
                for child in lines.children:
                    if child.id == 'text' and lines.id == '0':
                        label = Label()
                        label.text = 'Window width'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '0':
                        textbox = TextInput()
                        textbox.text = '0'
                        textbox.multiline = False
                        textbox.size_hint = (1.0, 0.25)
                        self.input_fields['wwidth'] = textbox
                        spacer_top = BoxLayout()
                        spacer_top.size_hint = (1.0, 0.35)
                        spacer_bot = BoxLayout()
                        spacer_bot.size_hint = (1.0, 0.35)
                        child.add_widget(spacer_top)
                        child.add_widget(textbox)
                        child.add_widget(spacer_bot)
                    if child.id == 'text' and lines.id == '1':
                        label = Label()
                        label.text = 'Window height'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '1':
                        textbox = TextInput()
                        textbox.text = '1'
                        textbox.multiline = False
                        textbox.size_hint = (1.0, 0.25)
                        self.input_fields['wheight'] = textbox
                        spacer_top = BoxLayout()
                        spacer_top.size_hint = (1.0, 0.35)
                        spacer_bot = BoxLayout()
                        spacer_bot.size_hint = (1.0, 0.35)
                        child.add_widget(spacer_top)
                        child.add_widget(textbox)
                        child.add_widget(spacer_bot)
                box.add_widget(lines)

        if box.id == 'Lines':
            boxes = self.getOptionsLayout(1,0.8)
            for lines in boxes:
                for child in lines.children:
                    if child.id == 'text' and lines.id == '0':
                        label = Label()
                        label.text = 'Line width'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '0':
                        textbox = TextInput()
                        textbox.text = '0'
                        textbox.multiline = False
                        textbox.size_hint = (1.0, 0.125)
                        self.input_fields['sline'] = textbox
                        spacer_top = BoxLayout()
                        spacer_top.size_hint = (1.0, 0.35)
                        spacer_bot = BoxLayout()
                        spacer_bot.size_hint = (1.0, 0.35)
                        child.add_widget(spacer_top)
                        child.add_widget(textbox)
                        child.add_widget(spacer_bot)
                box.add_widget(lines)
        if box.id == 'Scales':
            boxes = self.getOptionsLayout(2,0.5)
            for lines in boxes:
                for child in lines.children:
                    if child.id == 'text' and lines.id == '0':
                        label = Label()
                        label.text = 'Y axis scale'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '0':
                        box_labels = BoxLayout()
                        box_labels.orientation = 'horizontal'
                        box_labels.size_hint = (1.0,0.2)

                        label_lin = Label()
                        label_lin.text = 'Linear'
                        label_lin.font_size = 12
                        label_log = Label()
                        label_log.text = 'Logarithmic'
                        label_log.font_size = 12

                        box_labels.add_widget(label_lin)
                        box_labels.add_widget(label_log)

                        box_radio = BoxLayout()
                        box_radio.orientation = 'horizontal'
                        box_radio.size_hint = (1.0, 0.2)

                        radio_lin = CheckBox()
                        radio_lin.group = '0'
                        radio_lin.active = True
                        radio_log = CheckBox()
                        radio_log.group = '0'
                        radio_log.active = False

                        self.input_fields['yaxis'] = (radio_lin,radio_log)

                        box_radio.add_widget(radio_lin)
                        box_radio.add_widget(radio_log)

                        child.add_widget(box_labels)
                        child.add_widget(box_radio)
                    if child.id == 'text' and lines.id == '1':
                        label = Label()
                        label.text = '\"Z\" axis scale'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '1':
                        box_labels = BoxLayout()
                        box_labels.orientation = 'horizontal'
                        box_labels.size_hint = (1.0, 0.2)

                        label_lin = Label()
                        label_lin.text = 'Linear'
                        label_lin.font_size = 12
                        label_log = Label()
                        label_log.text = 'Decibels'
                        label_log.font_size = 12

                        box_labels.add_widget(label_lin)
                        box_labels.add_widget(label_log)

                        box_radio = BoxLayout()
                        box_radio.orientation = 'horizontal'
                        box_radio.size_hint = (1.0, 0.2)

                        radio_lin = CheckBox()
                        radio_lin.group = '1'
                        radio_lin.active = True
                        radio_log = CheckBox()
                        radio_log.group = '1'
                        radio_log.active = False

                        self.input_fields['zaxis'] = (radio_lin, radio_log)

                        box_radio.add_widget(radio_lin)
                        box_radio.add_widget(radio_log)

                        child.add_widget(box_labels)
                        child.add_widget(box_radio)
                box.add_widget(lines)
        if box.id == 'Window function':
            boxes = self.getOptionsLayout(1, 0.8)
            for lines in boxes:
                for child in lines.children:
                    if child.id == 'text' and lines.id == '0':
                        label = Label()
                        label.text = 'Blackman window'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '0':
                        checkbox = CheckBox()
                        checkbox.size_hint = (1.0, 0.2)
                        spacer_top = BoxLayout()
                        spacer_top.size_hint = (1.0, 0.4)
                        spacer_bot = BoxLayout()
                        spacer_bot.size_hint = (1.0, 0.4)
                        self.input_fields['blackman'] = checkbox
                        child.add_widget(spacer_top)
                        child.add_widget(checkbox)
                        child.add_widget(spacer_bot)
                box.add_widget(lines)
        if box.id == 'Color Values':
            boxes = self.getOptionsLayout(2, 0.5)
            for lines in boxes:
                for child in lines.children:
                    if child.id == 'text' and lines.id == '0':
                        label = Label()
                        label.text = 'Maximum value'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '0':
                        box_labels = BoxLayout()
                        box_labels.orientation = 'horizontal'
                        box_labels.size_hint = (1.0, 0.3)

                        label_lin = Label()
                        label_lin.text = 'Linear'
                        label_lin.font_size = 12
                        label_log = Label()
                        label_log.text = 'Decibels'
                        label_log.font_size = 12

                        box_labels.add_widget(label_lin)
                        box_labels.add_widget(label_log)


                        box_input = BoxLayout()
                        box_input.orientation = 'horizontal'
                        box_input.size_hint = (1.0, 0.2)

                        value_lin = TextInput()
                        value_lin.text = '0'
                        value_lin.multiline = False
                        value_lin.size_hint = (0.5, 1.0)
                        value_db = TextInput()
                        value_db.text = '0'
                        value_db.multiline = False
                        value_db.size_hint = (0.5, 1.0)

                        self.input_fields['maxlin'] = value_lin
                        self.input_fields['maxdb'] = value_db

                        box_input.add_widget(value_lin)
                        box_input.add_widget(value_db)

                        box_spacer = BoxLayout()
                        box_spacer.size_hint = (1.0,0.3)
                        child.add_widget(box_labels)
                        child.add_widget(box_input)
                        child.add_widget(box_spacer)
                    if child.id == 'text' and lines.id == '1':
                        label = Label()
                        label.text = 'Minimum value'
                        child.add_widget(label)
                    if child.id == 'values' and lines.id == '1':
                        box_labels = BoxLayout()
                        box_labels.orientation = 'horizontal'
                        box_labels.size_hint = (1.0, 0.3)

                        label_lin = Label()
                        label_lin.text = 'Linear'
                        label_lin.font_size = 12
                        label_log = Label()
                        label_log.text = 'Decibels'
                        label_log.font_size = 12

                        box_labels.add_widget(label_lin)
                        box_labels.add_widget(label_log)

                        box_input = BoxLayout()
                        box_input.orientation = 'horizontal'
                        box_input.size_hint = (1.0, 0.2)

                        value_lin = TextInput()
                        value_lin.text = '0'
                        value_lin.multiline = False
                        value_lin.size_hint = (0.5, 1.0)
                        value_db = TextInput()
                        value_db.text = '0'
                        value_db.multiline = False
                        value_db.size_hint = (0.5, 1.0)

                        self.input_fields['minlin'] = value_lin
                        self.input_fields['mindb'] = value_db

                        box_input.add_widget(value_lin)
                        box_input.add_widget(value_db)

                        box_spacer = BoxLayout()
                        box_spacer.size_hint = (1.0, 0.3)

                        child.add_widget(box_labels)
                        child.add_widget(box_input)
                        child.add_widget(box_spacer)
                box.add_widget(lines)

    def getOptionsLayout(self,amount,text_width):
        return_list = []
        for i in range(amount):
            box_master = BoxLayout()
            box_master.size_hint_x = 1.0
            box_master.orientation = 'horizontal'
            box_master.id = str(i)

            box_text = BoxLayout()
            box_text.size_hint_x = text_width
            box_text.id = 'text'

            box_values = BoxLayout()
            box_values.size_hint_x = 1-text_width
            box_values.orientation = 'vertical'
            box_values.id = 'values'

            box_master.add_widget(box_text)
            box_master.add_widget(box_values)
            return_list.append(box_master)
        return tuple(return_list)

    def fillValues(self):
        for key in self.input_fields:
            value = self.parent_widget.getOptions().get(key)
            #print("key is {0}, value is {1}, type is {2}".format(key, value, type(value)))
            if key == 'yaxis' or key == 'zaxis':
                for widget in self.input_fields[key]:
                    widget.bind(active=partial(self.validateInput, key))
                if value == 'lin':
                    self.input_fields[key][0].active = True
                else:
                    self.input_fields[key][1].active = True
            else:
                if key == 'blackman':
                    self.input_fields[key].bind(active=partial(self.validateInput, key))
                    if int(value) == 0:
                        self.input_fields[key].active = False
                    else:
                        self.input_fields[key].active = True

                else:
                    print(key)
                    self.input_fields[key].bind(text=partial(self.validateInput, key))
                    self.input_fields[key].bind(focus=partial(self.noEmptyFields, key))
                    self.input_fields[key].text = value

    def validateInput(self,key,*args):
        dimension_keys = ['sheight','swidth','wheight','wwidth']
        other_keys = ['sline', 'minlin', 'maxlin', 'mindb', 'maxdb', 'chunk', 'fs', 'channels']
        if key in dimension_keys:
            self.validateDimensions(key)
        if key in other_keys:
            self.validateOthers(key)
        if key == 'yaxis' or key == 'zaxis':
            self.validateRadios(key)

    def validateDimensions(self,key):
        counterparts = {'sheight': 'wheight', 'swidth': 'wwidth', 'wheight': 'sheight', 'wwidth': 'swidth'}
        try:
            value = int(self.input_fields[key].text)
        except ValueError:
            if self.input_fields[key].text == '':
                self.input_fields[key].text = ''
            else:
                self.errorLabel.text = 'ERROR: Dimension must be a number'
                value = self.parent_widget.getOptions().defaults[key]
                value_counterpart = self.parent_widget.getOptions().defaults[counterparts[key]]
                self.input_fields[key].text = str(value)
                self.input_fields[counterparts[key]].text = str(value_counterpart)

    def validateOthers(self,key):
        try:
            value = int(self.input_fields[key].text)
        except ValueError:
            if self.input_fields[key].text == '':
                self.input_fields[key].text = ''
            else:
                self.errorLabel.text = 'ERROR: {0} value must be a number'.format(key)
                value = self.parent_widget.getOptions().defaults[key]
                self.input_fields[key].text = str(value)

    def validateRadios(self,key):
        if self.input_fields[key][0].active == False and  self.input_fields[key][1].active == False:
            self.input_fields[key][0].active = True


    def noEmptyFields(self,key,*args):
        self.noEmptyFieldsLast = key
        value = self.input_fields[key].text
        dimension_keys = ['sheight','swidth','wheight','wwidth']
        other_keys = ['sline', 'minlin', 'maxlin', 'mindb', 'maxdb', 'channels']
        minmax_dict = {'sline': (1, 5),
                       'minlin': (1, 1),
                       'maxlin': (1, 1),
                       'mindb': (-100, 100),
                       'maxdb': (-100, 100),
                       'channels': (1, 2)}
        if key in dimension_keys:
            max_value = 3000
            min_value = 101
            if self.input_fields[key].text == '':
                self.input_fields[key].text = str(self.parent_widget.getOptions().defaults[key])
                self.errorLabel.text = 'ERROR: Dimension value cannot be left empty - changing to default.'
            elif int(value) < min_value:
                value = min_value
                self.input_fields[key].text = str(value)
                self.errorLabel.text = 'ERROR: Dimension value must be between {0} and {1}. Changing to {0}'.format(key,min_value,max_value)
            elif int(value) > max_value:
                value = max_value
                self.input_fields[key].text = str(value)
                self.errorLabel.text = 'ERROR: Dimension value must be between {0} and {1}. Changing to {1}'.format(key,min_value,max_value)
            if key == 'sheight':
                self.input_fields['wheight'].text = str(int(value)+100)
            if key == 'swidth':
                self.input_fields['wwidth'].text = str(int(value)+50)
            if key == 'wwidth':
                self.input_fields['swidth'].text = str(int(value)-50)
            if key == 'wheight':
                self.input_fields['sheight'].text = str(int(value)-100)

        if key in other_keys:
            counterparts_colors = {'mindb': 'maxdb', 'maxdb': 'mindb', 'minlin': 'maxlin', 'maxlin': 'minlin'}
            if self.input_fields[key].text == '':
                self.input_fields[key].text = str(self.parent_widget.getOptions().defaults[key])
                self.errorLabel.text = 'ERROR: {0} field cannot be left empty - changing to default.'.format(key)
            elif int(value) < minmax_dict[key][0]:
                value = minmax_dict[key][0]
                self.input_fields[key].text = str(value)
                self.errorLabel.text = 'ERROR: {0} value must be between {1} and {2}. Changing to {1}'.format(key,minmax_dict[key][0],minmax_dict[key][1])
            elif int(value) > minmax_dict[key][1]:
                value = minmax_dict[key][1]
                self.input_fields[key].text = str(value)
                self.errorLabel.text = 'ERROR: {0} value must be between {1} and {2}. Changing to {2}'.format(key,minmax_dict[key][0],minmax_dict[key][1])
            if key == 'mindb' or key == 'minlin':
                if int(self.input_fields[key].text) > int(self.input_fields[counterparts_colors[key]].text):
                    self.input_fields[key].text = str(self.parent_widget.getOptions().defaults[key])
                    self.input_fields[counterparts_colors[key]].text = str(self.parent_widget.getOptions().defaults[counterparts_colors[key]])
                    self.errorLabel.text = 'ERROR: Minimal value must be smaller than maximal. Returning both to default.'
            if key == 'maxdb' or key == 'maxlin':
                if int(self.input_fields[key].text) < int(self.input_fields[counterparts_colors[key]].text):
                    self.input_fields[key].text = str(self.parent_widget.getOptions().defaults[key])
                    self.input_fields[counterparts_colors[key]].text = str(self.parent_widget.getOptions().defaults[counterparts_colors[key]])
                    self.errorLabel.text = 'ERROR: Maximal value must be bigger than minimal. Returning both to default.'


        if key == 'chunk':
            value = int(self.input_fields[key].text)
            power = log2(value)
            if self.input_fields[key].text == '':
                self.input_fields[key].text = str(self.parent_widget.getOptions().defaults[key])
                self.errorLabel.text = 'ERROR: Chunk size field cannot be left empty - changing to default.'
            if 2**int(power) != value:
                self.errorLabel.text = 'ERROR: Chunk size must be a power of 2.'
                self.input_fields[key].text = str(self.parent_widget.getOptions().defaults[key])

        if key == 'fs':
            default_value = self.parent_widget.getOptions().defaults[key]
            value = int(self.input_fields[key].text)
            formatted = format((value/default_value),'.1f')
            if self.input_fields[key].text == '':
                self.input_fields[key].text = str(default_value)
                self.errorLabel.text = 'ERROR: Sampling frequency field cannot be left empty - changing to default.'
            if default_value*float(formatted) != value:
                self.errorLabel.text = 'ERROR: Sampling frequency must by a fraction (10%, 20%, 30%...) of 44100.'
                self.input_fields[key].text = str(default_value)

    def backButtonPress(self,instance,*args):
        if self.noEmptyFieldsLast != None:
            self.noEmptyFields(self.noEmptyFieldsLast)
        keys = ['sheight','swidth','wheight','wwidth','sline','yaxis','zaxis','blackman','minlin','maxlin','mindb','maxdb','chunk','fs','channels']
        for key in keys:
            if key == 'yaxis' or key == 'zaxis':
                if self.input_fields[key][0].active == True:
                    value = 'lin'
                else:
                    value = 'log'
            elif key == 'blackman':
                if self.input_fields[key].active == True:
                    value = 1
                else:
                    value = 0
            else:
                value = int(self.input_fields[key].text)
            options = self.parent_widget.getOptions()
            options.set(key,value)
        self.parent_widget.getOptions().saveToFile()
        self.parent_widget.back_options()




