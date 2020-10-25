from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from GUI_Yaxis_Ruler import Ruler

class Yaxis(Widget):
    def __init__(self, parent, **kwargs):
        super(Yaxis, self).__init__(**kwargs)
        self.interface_widget = parent
        self.options = self.interface_widget.getOptions()
        self.SPEC_HEIGHT = self.options.getInt('sheight')
        self.OPTIONS_WIDTH = 50
        self.WINDOW_WIDTH = self.options.getInt('wwidth')
        self.height = self.SPEC_HEIGHT
        self.width = self.OPTIONS_WIDTH
        self.pos = (self.WINDOW_WIDTH-50,0)

        self.rulers = [] #Every widget is responsible for one ruler containing 4000Hz

        self.layout_yaxis = BoxLayout()
        self.layout_yaxis.size = (self.width,self.height)
        self.layout_yaxis.orientation = 'vertical'
        self.layout_yaxis.pos = self.pos


        self.generateWidgets()
        self.add_widget(self.layout_yaxis)

    def generateWidgets(self):
        rulerAmount = int(self.SPEC_HEIGHT / 42)
        placedTopSpacer = 0
        layout_ruler = BoxLayout()
        layout_ruler.orientation = 'vertical'
        layout_ruler.size_hint_x = 0.5

        layout_numbers = BoxLayout()
        layout_numbers.orientation = 'vertical'
        layout_numbers.size_hint = (0.5,1.0)
        layout_numbers.spacing = 42
        layout_numbers.padding = [0,self.SPEC_HEIGHT-(42*rulerAmount),0,42]

        for i in range(rulerAmount):
            ruler = Ruler(int(self.WINDOW_WIDTH-50),int(i*42))
            layout_ruler.add_widget(ruler)

            text_number = "{0}".format(((rulerAmount+1)*1764)-((i+1)*1764))
            label = Label(text=text_number,font_size = 7)
            layout_numbers.add_widget(label)


        layout_container = BoxLayout()
        layout_container.orientation='horizontal'
        layout_container.size_hint_x = 1.0
        layout_container.height = 42
        layout_container.pos = (self.WINDOW_WIDTH,0)
        layout_container.add_widget(layout_ruler)
        layout_container.add_widget(layout_numbers)
        self.layout_yaxis.add_widget(layout_container)
