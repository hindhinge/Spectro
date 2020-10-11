import os.path
class Options():
    def __init__(self):
        self.defaults = {'sheight' : 800 ,
                         'swidth' :  1000,
                         'wheight' : 900,
                         'wwidth' : 1050 ,
                         'sline' : 2 ,
                         'yaxis' : 'lin' ,
                         'zaxis' : 'log' ,
                         'blackman' : 0 ,
                         'minlin' : 1 ,
                         'maxlin' : 1 ,
                         'mindb' : -10 ,
                         'maxdb' : 10 ,
                         'chunk' : 1024,
                         'fs' : 44100,
                         'channels' : 2}

        self.filename = 'options.txt'
        self.current_options = dict()
        self.startup()

    def startup(self):
        try:
            self.loadFromFile()
        except FileNotFoundError:
            f = open(self.filename,'w+')
            for key in self.defaults:
                f.write("{0}:{1}\n".format(key,self.defaults[key]))
            f.close()
            self.current_options = self.defaults

    def saveToFile(self):
        f = open(self.filename, 'w+')
        for key in self.defaults:
            f.write("{0}:{1}\n".format(key, self.current_options[key]))
        f.close()

    def loadFromFile(self):
        f = open(self.filename,'r')
        contents = f.read()
        split = contents.split('\n')
        for option in split:
            nextSplit = option.split(':')
            if len(nextSplit) == 1:
                pass
            else:
                key = nextSplit[0]
                value = nextSplit[1]
                self.current_options[key] = value
        f.close()

    def get(self,key):
        return self.current_options[key]

    def getInt(self,key):
        return int(self.current_options[key])

    def set(self,key,value):
        self.current_options[key] = value

options = Options()
