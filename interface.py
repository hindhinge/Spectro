import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.config import Config

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')
Config.write()

color_r = [i/10 for i in range(0,11)]
color_g = [i/10 for i in range(0,11)]
color_b = [i/10 for i in range(0,11)]
print(color_r)

class RectBlock(Widget):
    def __init__(self,color, **kwargs):
        super(RectBlock, self).__init__(**kwargs)
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        with self.canvas:
            Color(self.r, self.g, self.b, 1)  # set the colour to red
            self.rect = Rectangle(pos=(0,0),size=(8, 8))
    def getColors(self,num1,num2):
        self.r = color_r[num1]
        self.g = color_g[num2]
        self.b = color_b[int((num1+num2)/2)]




class MyGrid(Widget):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.block_x = 8
        self.block_y = 8
        for i in range(0, 100):
            for j in range(0,100):
                r = float((i%11)/10)
                g = float(1 - (i%11)/10)
                b = 0.0
                block = RectBlock([r,g,b])
                block.rect.pos = (i*self.block_x, j*self.block_x)
                self.add_widget(block)



class Kurwy(Widget):
    pass

class SpectroApp(App):
    def build(self):
        return MyGrid()


SpectroApp().run()
# class Spectro(Widget):
# pass
