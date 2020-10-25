import numpy as np
import pyaudio
from array import array

from record import Recording
from GUI_RectBlock import *
from mathfunctions import genRfreq
from math import e, pi

from kivy.uix.widget import Widget




class MathController(Widget):
    def __init__(self,parent,**kwargs):
        super(MathController, self).__init__(**kwargs)
        self.iter = 1
        self.interface_widget = parent
        self.options = self.interface_widget.getOptions()
        self.height = self.options.getInt('sheight')
        self.width = self.options.getInt('swidth')
        self.rec = Recording(self.options.getInt('chunk'),pyaudio.paInt16,self.options.getInt('channels'),self.options.getInt('fs'),1,'mic_test.wav')
        self.rec.openStream()
        self.texture = self.getBlackTexture()
        self.rect = self.createRectBlock()
        self.rfreq = genRfreq(self.options.getInt('chunk'),self.options.getInt('fs'))

    def createRectBlock(self):
        block = RectBlock(self.texture,self.options.getInt('sheight'),self.options.getInt('sline'),self.options)
        block.writeOptions(-1*(self.options.getInt('sheight')/2) , self.options.getInt('swidth')-(self.options.getInt('sheight')/2))
        self.add_widget(block)
        return block

    def widenRectBlock(self,tex):
        if self.rect.height < self.options.getInt('swidth'):
            self.rect.increaseWidthFlipped(self.options.getInt('sline'))
            self.rect.moveToLeftFlipped(self.options.getInt('sline'))
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
        dft = self.genFft(chunk, self.options.getInt('fs'))
        print("dft length {0}".format(len(dft[1])))
        return dft[1]

    def toDecibels(self,chunk):
        output = []
        sig = chunk[0:self.options.getInt('sheight')]
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
        max_value = self.options.getInt('maxdb')
        min_value = self.options.getInt('mindb')
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
        print("color table len {0}".format(len(color)))
        for j in range(self.options.getInt('sline')):       #pętla for j in range(self.options.getInt('sline')):
            for i in range(len(color)):                     # nad for i in range(len(color)) to sline definiuje szerokość
              rgb=color[i]
              if type(rgb) != int:                          #pętla for j in range(self.options.getInt('sline')):
                for number in rgb:                          #nad for number in rgb sline definiuje wysokość
                    buffer.append(number)
        arr = array('B',buffer)
        print("buffer table len {0}".format(len(buffer)))
        return arr

    def getBlackTexture(self):
        size = 3 * self.options.getInt('sline') * self.options.getInt('sheight')
        buf = []
        for i in range(size):
            buf.append(255)
            buf.append(0)
            buf.append(0)
        arr = array('B',buf)
        return arr
    def getBlueTexture(self):
        size = 3 * self.options.getInt('sline') * self.options.getInt('sheight')
        buf = []
        for i in range(size):
            buf.append(0)
            buf.append(0)
            buf.append(255)
        arr = array('B',buf)
        return arr