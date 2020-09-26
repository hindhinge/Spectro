import numpy as np
import pyaudio
from array import array

from record import Recording
from GUI_RectBlock import RectBlock
from mathfunctions import genRfreq
from math import e, pi
from GUI_RectBlock import REC_FS,REC_CHUNK, SPEC_HEIGHT, SPEC_WIDTH,REC_FORMAT,REC_CHANNELS,REC_SECONDS,REC_FILENAME,SPEC_LINEWIDTH

from kivy.uix.widget import Widget




class MathController(Widget):
    def __init__(self,**kwargs):
        super(MathController, self).__init__(**kwargs)
        self.iter = 1
        self.height = SPEC_HEIGHT
        self.width = SPEC_WIDTH
        self.rec = Recording(REC_CHUNK,REC_FORMAT,REC_CHANNELS,REC_FS,REC_SECONDS,REC_FILENAME)
        self.rec.openStream()
        self.texture = self.getBlackTexture()
        self.rect = self.createRectBlock()
        self.rfreq = genRfreq(REC_CHUNK,REC_FS)

    def createRectBlock(self):
        block = RectBlock(self.texture,SPEC_HEIGHT,SPEC_LINEWIDTH)
        self.add_widget(block)
        return block

    def widenRectBlock(self,tex):
        if self.rect.height < SPEC_WIDTH:
            self.rect.increaseWidthFlipped(SPEC_LINEWIDTH)
            self.rect.moveToLeftFlipped(SPEC_LINEWIDTH)
        self.rect.setTexture(tex)
        self.rect.update_rect()
        self.rect.update()
        self.iter += 1

    def microProcessing(self,dt):
        dft = self.getDft()
        dbs = self.toDecibels(dft)
        db_color = self.genColorsDB(dbs)
        tex_array = self.getTextureArray(db_color)
        self.widenRectBlock(tex_array)


    def genFft(self,sig, N):
        y = np.fft.rfft(sig)
        modul = np.abs(y) / (N / 2)
        return (y, modul)



    def getDft(self):
        chunk = self.rec.recordChunk()
        dft = self.genFft(chunk, REC_FS)
        return dft[1]

    def toDecibels(self,chunk):
        output = []
        sig = chunk[0:SPEC_HEIGHT]
        sig = sig[::-1]
        for value in sig:
            abs = np.absolute(value)
            if(abs <= 0):
                db = -40
                output.append(db)
            else:
                db = 10*np.log10(abs)
                output.append(db)
        return output

    def genColorsDB(self,dbs):
        signal = dbs
        max_value = 15
        min_value = -5
        output = []
        resolution = (max_value - min_value) / 1275
        for value in signal:
            if value > max_value:
                output.append((255,255,255))
            elif value < min_value:
                output.append((0,0,0))
            else:
                added_value = value - min_value
                val = added_value/resolution
                if (val <= 255):
                    color = (0, 0, int(val))
                    output.append(color)
                elif val > 255 and val <= 510:
                    color = (int(val) - 255, 0, 255)
                    output.append(color)
                elif val > 510 and val <= 765:
                    color = (255, 0, 255 - (int(val) - 510))
                    output.append(color)
                elif val > 765 and val <= 1020:
                    color = (255, int(val) - 765, 0)
                    output.append(color)
                elif val > 1020:
                    color = (255, 255, int(val) - 1020)
                    output.append(color)

        return output

    def getTextureArray(self,color):
        buffer = []
        for i in range(len(color)):
            rgb=color[i]
            if type(rgb) != int:
                for j in range(SPEC_LINEWIDTH):
                    for number in rgb:
                        buffer.append(number)
        arr = array('B',buffer)
        return arr

    def getBlackTexture(self):
        size = 3 * SPEC_LINEWIDTH * SPEC_HEIGHT
        buf = []
        for i in range(size):
            buf.append(255)
            buf.append(0)
            buf.append(0)
        arr = array('B',buf)
        return arr
    def getBlueTexture(self):
        size = 3 * SPEC_LINEWIDTH * SPEC_HEIGHT
        buf = []
        for i in range(size):
            buf.append(0)
            buf.append(0)
            buf.append(255)
        arr = array('B',buf)
        return arr