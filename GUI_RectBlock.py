from kivy.graphics import *
from kivy.graphics.texture import TextureRegion
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
import pyaudio

# #########GLOBALS##########
# #########Recording options##########
REC_CHUNK = 1024  # Number of recorded samples in one chunk. Default 1024
REC_CHANNELS = 2  # Number of channels to record
REC_FORMAT = pyaudio.paInt16  # Data format in which recorded data is stored
REC_FS = 44100  # Input stream sampling frequency. Use 44100 to get final frequency scale of 22050
REC_SECONDS = 1  # Seconds of recording to capture. Not used if live microphone signal is the source
REC_FILENAME = "mic_test.wav"  # Output file name. Not used if live microphone signal is the source
# #########SPECTROGRAPH OPTIONS##########
SPEC_LINEWIDTH = 2  # Width of a line created after one data chunk is processed
SPEC_WIDTH = 1000  # Default 1000
SPEC_HEIGHT = 800  # Default 800
SPEC_REFRESHDELETE = 3 * SPEC_LINEWIDTH * SPEC_HEIGHT  # Amount of data to delete from texture array if spectrogram
                                                         # line reaches end of the window
# #########b##########
# #########c##########
# #########d##########
# #########e##########


class RectBlock(Widget):
    def __init__(self,texture_array,xsize,ysize, **kwargs):
        super(RectBlock, self).__init__(**kwargs)
        self.texture = TextureRegion.create(size=(xsize, ysize))
        self.arr = texture_array
        self.setSize(xsize,ysize)
        self.update()
        self.iter = 1
        self.canvas.before.add(PushMatrix())
        self.canvas.before.add(Rotate(angle=-90,origin=self.center))
        self.canvas.after.add(PopMatrix())
    x_size = NumericProperty(0)
    y_size = NumericProperty(0)
    x_pos = NumericProperty(int(SPEC_WIDTH - (SPEC_HEIGHT/2)))  # For window width of 1000, x_pos = 556 was working just right
    y_pos = NumericProperty(SPEC_HEIGHT/2)   # For window height of 882, y_pos = 439 was working just right

    def setTexture(self,arr):
        tex = TextureRegion.create(size=(self.x_size, self.y_size))
        self.texture = tex
        if self.height < SPEC_WIDTH:
            self.arr.extend(arr)
        else:
            del self.arr[0:SPEC_REFRESHDELETE]
            self.arr.extend(arr)
        self.update()


    def setSize(self,xsize,ysize):
        self.x_size = xsize
        self.y_size = ysize

    def moveToLeft(self,amount):
        self.x_pos -= amount

    def moveToLeftFlipped(self,amount):
        self.y_pos -= amount

    def increaseWidth(self,amount):
        self.x_size += amount

    def increaseWidthFlipped(self,amount):
        self.y_size += amount

    def update(self):
        self.texture.blit_buffer(self.arr, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=(self.x_size,self.y_size))
    def update_rect(self, *args):
        self.canvas.clear()
        self.rect.pos = self.pos
        self.rect.size = self.size