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

import svg


def create(s, file_name):
   
    r,l,t,b = [getattr(s,"getSide")(i) for i in "RLTB"]
    
    p = 21.25 # grid

    height = p*(max(len(r), len(l)))
    width = p*(max(len(t), len(b)))
    
    svg_width  = width +2*p
    svg_height = height+2*p
    svg.start(svg_width, svg_height, svg_width*127/360, svg_height*127/360, "mm")
    svg.add_start_g(id="schematic")

    def addPin(nr,c,name,direction):
        if direction == "R":
            x = width +p
            y = (1.5+ c)*p
            r = 0
            f = 0
        elif direction == "L":
            x = p
            y = p*(1.5 +c)
            r = 0
            f = 1
        elif direction == "T":
            x = (1.5+ c)*p
            y = p
            r = 90
            f = 1
        elif direction == "B":
            x = p*(1.5 +c)
            y = height +p
            r = 90
            f = 0

        if f == 0:
            name_anchor = "end"
            nr_anchor = "start"
            direction = 1
        else:
            name_anchor = "start"
            nr_anchor = "end"
            direction = -1
        
        svg.add_start_g(transform="rotate({r}, {x}, {y}) translate({x},{y}) ".format(x=x,y=y,r=r))
        svg.add_path(d=(
                svg.M(0,-1.2),
                svg.H(p*direction),
                svg.V(1.2),
                svg.H(0),
                svg.z()), id="connector{0}pin".format(nr))
        svg.add_path(d=(
                svg.M((p)*direction-2.4*direction,-1.2),
                svg.h(2.4*direction),
                svg.v(2.4),
                svg.h(-2.4*direction),
                svg.z()), id="connector{0}terminal".format(nr))
        svg.add_text(name, x=-3*direction, y=3, font_size=10, font_family="DroidSans", text_anchor=name_anchor)
        svg.add_text(nr, x=+3*direction, y=-2, font_size=7, font_family="DroidSans", text_anchor=nr_anchor)
        svg.add_end_g()

    for data,direction in [(r,"R"), (l,"L"), (t,"T"), (b,"B")]:
        for i,pin in enumerate(data):
            if pin:
                name, description = s.pins.data[pin]
                addPin(pin, i, name, direction)
    
    svg.add_rect(p,p,width,height, fill="none", stroke_width=2.4, stroke="#000000")
    x = svg_width/2
    r = 0
    if not any(t):
        y = 18
    elif not any(b):
        y = svg_height - 1
    elif not any(r):
        r = 90
        y = svg_height/2
        x = svg_width -18
    elif not any(l):
        r = 270
        y = svg_height/2
        x = 18
    else:
        x = svg_width/2
        y = svg_height/2
        r = 270 if width < height else 0
    if r != 0:
        rotate = "rotate({r},{x},{y})".format(r=r,x=x,y=y)
    else:
        rotate = ""
    svg.add_text(s.meta.name,
        font_size=18, font_family="DroidSans", text_anchor="middle",
        transform="{r} translate({x},{y})".format(r=rotate, x=x,y=y)) # name!
    
    svg.add_end_g()
    svg.end()
    svg.write(file_name)

