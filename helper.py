#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011 Benedikt Seidl
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.

import sys
import re

def error(string):
    print string
    sys.exit()

conversion=dict(px=1,pt=1,mm=360/127.,mils=2.54*360/127.,inch=72,cm=36/127)
conversion.update({"in":72})

def to_pixel(string):
    m = re.match(r"^([\d.]+)\s*([a-zA-Z]+)$", string.strip())
    if m:
        f,s = m.groups()
        if s not in conversion:
            error("'{0}' not a known unit. known units:{1}".format(s, ", ".join(["'{0}'".format(k) for k in conversion.keys()])))
        try:
            f = float(f)
        except:
            error("can not convert to float: '{0}'".format(f))
        return f * conversion[s]
    else:
        error("can not convert '{0}' to a string".format(string))

if __name__ == "__main__":
    print to_pixel("1px")
    print to_pixel("1.px")
    print to_pixel("1.0px")
    print to_pixel("1.0 px")
    print to_pixel("1 px")
    print to_pixel("1  px")
    print to_pixel("1  pt")
    print to_pixel("1  mm")
    print to_pixel("1mils")
    print to_pixel("1in")
    print to_pixel("1inch")
    print to_pixel("1 cm")
    print to_pixel("100mm")
    print to_pixel("100mils")
    # want to see the error
    print to_pixel("100xxx")
