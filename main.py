from kivy.app import App
from GUI_Interface import Interface
from GUI_ColorScale import ColorScale

class SpectroApp(App):
    def build(self):
        interface = Interface()
        interface.setWindowDimension(interface.WINDOW_WIDTH,interface.WINDOW_HEIGHT)
        # color = ColorScale(interface)
        # return color
        return interface

if __name__ == '__main__':
    SpectroApp().run()
