#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pprint import pprint
import shellArgs
import sys
import math
from PIL import Image, ImageDraw, ImageFont
import font
import datetime

class Pic2Ascii(object):
    """
    Pic2Ascii: Let's you turn images into ASCII! It's so useful!
    
    Can be initialized with the following arguments:
        Pic2Ascii(font=Font_object(), **kwargs)
        
    Supported keyword args:
        color=(True|False)
        invert=(True|False)
        bg=(black|white|*)
        o=(file path)
    """
    SUPPORTED_FORMATS = [('JPEG', '*.jpg'),
                         ('Graphics Interchange Format', '*.gif'),
                         ('Portable Network Graphic', '*.png')]
    
    MAX_THUMBNAIL=200
    
    def __init__(self, font=font.LuconFont, **kwargs):
        """ 
        Initialize with a font and possible kwargs. The kwargs
        are the same as if you call it for the first time from
        output_image()
        """
        self.font = font()
        if kwargs:
            self.options = kwargs
        self.asciiList = self.font.asciiList
        self.font.asciiList.reverse()
        self.numChars = len(self.font.asciiList)-1
        self.image = None
        self.greyscale_image = None
        self.asciiString = ""
        self.colorString = []
        
    def _load_image(self):
        """Use PIL to load an image into self.image"""
        try:
            self.image = Image.open(self.options['image_path'])
        except IOError:
            print "Error: Not a valid filename."
    
    def _prep_image(self):
        """
        - Scale the image to the ratio of the font used.
        - Thumbnail the image so the longest size is equal
            to MAX_THUMBNAIL
        """
        # Convert to black and white and multiply the length
        # by 1.6 (since the font is has a 1:1.6 ratio)
        
        self.image = self.image.resize(
            ((self.image.size[0]*self.font.ratio), self.image.size[1]))
            
        self.image.thumbnail(
            (Pic2Ascii.MAX_THUMBNAIL, Pic2Ascii.MAX_THUMBNAIL))
        self.greyscale_image = self.image.convert("L")
    
    def _create_ascii_string(self):
        """
         Loop over every pixel in the image. Find relative
         darkness from the greyscale image, find color from
         the original (resized image). Store these values
         into asciiString and colorString
        """     
        asciiStringList = []
        
        for y in range(0, self.image.size[1]):
            for x in range(0, self.image.size[0]):
            
                pix = self.greyscale_image.getpixel((x, y))
                color_pix = self.image.getpixel((x, y))
                
                # Based on darkness (out of 255) find the
                # character that is closest in our font's
                # greyscale.
                asciiStringList.append(self.font.asciiList[
                    int( math.floor((pix/(255/self.numChars ))) )
                ])
                
                self.colorString.append(color_pix)
        self.asciiString = ''.join(asciiStringList)
        
    def _create_image(self):
        """
        Generate the image given the asciiString and colorString
        """
        if self.options['bg'] == "black":
            backgroundColor = (0, 0, 0)
            foregroundColor = (255, 255, 255)
        elif self.options['bg'] == "white":
            backgroundColor = (255, 255, 255)
            foregroundColor = (0, 0, 0)
        else:
            backgroundColor = (255, 255, 255)
            foregroundColor = (0, 0, 0)
            
        # Size of the new image is scaled to the 
        # width/height of the thumbnail with corrections 
        # for the aspect ratio of the chosen font
        size = (self.image.size[0]*self.font.width, 
                self.image.size[1]*self.font.height)
        
        print size
        
        # Set up the new image so we can dump
        # text onto it!
        self.asciiImage = Image.new("RGB", size, backgroundColor)
        draw = ImageDraw.Draw(self.asciiImage)

        i,j = 0,0

        # Loop over each character in the string built from create_ASCII_string
        # and print the letter to the image.
        #
        # i progresses from left to right
        # j progresses downward
        # k keeps track of the total number of pixels
        # ---> (i*j) should equal k
        
        for k in range(len(self.asciiString)):
            if self.options['color'] == True:
                draw.text((i, j), self.asciiString[k], 
                    fill=self.colorString[k], font=self.font.pilFont)
            else: 
                draw.text((i, j), self.asciiString[k], 
                    fill=foregroundColor, font=self.font.pilFont)

            i += self.font.width
            
            if k % Pic2Ascii.MAX_THUMBNAIL == 0 and k>0: 
                j+=self.font.height
            if i == self.image.size[0]*self.font.width: 
                i=0
                
        del draw
        
    def output_image(self, **kwargs):
        if kwargs:
            self.options = kwargs
        if self.options['invert'] == True:
            self.font.asciiList.reverse()
            
        self._load_image()
        self._prep_image()
        self._create_ascii_string()
        # print "Length of colorstring: " + str(len(self.colorString))
        # print "Length of asscistring: " + str(len(self.asciiString))
        self._create_image()
        
        return self.asciiImage
        
        
            
if __name__ == "__main__":
    shell_args = shellArgs.argParser(sys.argv)
    app = Pic2Ascii(font=font.LuconFont)
        
    image = app.output_image(**shell_args.options.__dict__) 
    
    
    # This is ugly.
    outputName = vars(shell_args.__dict__['options'])['output']
    if not outputName:
        now = datetime.datetime.now()
        outputName = now.strftime("%Y-%m-%d-%H:%M") + str(".jpg")
        
    image.save(outputName, "JPEG")
    
    
