from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial

#############################TODO TODO
# - Opcje powinny znaleźć się w osobnej klasie jako globale (albo w obiekcie, nie iwem co lepiej)
# - Opcje do ustawiania: widow height, window width, spec line widh, spec width, spec height
#   zakres decybeli, wyświetlanie w skali lin-lin, lin-log częstotliuwoście, wyświetlanie w decybelach i wyświetlanie liniowe,
#   okienkowanie blackmana, zakres min i max wartość db (chyba że wybierzemy wyświetlanie liniowe, to min i max dla linioweog)

class OptionsScreen(Widget):
    def __init__(self, parent,width,height, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        self.parent_widget = parent
        self.WINDOW_HEIGHT = height
        self.WINDOW_WIDTH = width
        
        self.layout_options = BoxLayout()
        self.layout_options.orientation = 'vertical'
        self.layout_options.add_widget(Label(text='jeden'))
        self.layout_options.add_widget(Label(text='dwa'))
        self.add_widget(self.layout_options)