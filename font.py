#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PIL import ImageFont

class Font(object):
    def __init__(self):
        self.name = ""
        self.width = ""
        self.height = ""
        self.ratio = 0
        self.asciiList = []
        self.pilFont = ""
    
    # TODO: Finish proper __repr__ and __str__
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)
        
class LuconFont(Font):
    def __init__(self):
        self.name = "Lucon"
        self.width = 6
        self.height = 10
        self.ratio = 1.6
        self.asciiList = [" ",",",".","*","|","\\",";","+","?","C","0","H","#"]
        self.pilFont = ImageFont.truetype("lucon.ttf", 10)
        
if __name__ == "__main__":
    print Font
