#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import sys

class argParser(object):
    def __init__(self, args):
        self._initParser()
        self.options = self.parser.parse_args(args)
    def _initParser(self):
        self.parser = argparse.ArgumentParser(description="pic2ascii: Take pictures, make ascii!")
        self.parser.add_argument('called_script')
        self.parser.add_argument('image_path')
        self.parser.add_argument('--invert', action="store_true",
                                help='invert greyscale')
        self.parser.add_argument('--color', action="store_true",
                                help="generate color image")
        self.parser.add_argument('--bg', default="white",
                                help="background color (white or black)")
        self.parser.add_argument('-o', '--output', default="",
                                help="path for ASCII image")

if __name__ == '__main__':
    a = argParser(sys.argv)
    print a.options
