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
from helper import to_pixel

def create(p, file_name):

    pin, size = p.definition["pin"].split(" ", 1)
    chip_width = to_pixel(p.definition["c"]) # TODO: error check
    pins_gap = to_pixel(p.definition["e"]) # TODO: error check

    if p.definition["ch"] != None:
        chip_height = to_pixel(p.definition["ch"])
    else:
        chip_height = None

    if pin.strip() == "THT":
        is_smd = False
        dimension = size.split(",")

        d, pin_width, pin_height = map(to_pixel, dimension)
        stroke_width = 0.5*(min(pin_width, pin_height) - d)

        def add_pin(nr):
            if pin_width == pin_height:
                svg.add_circle(0,0, d/2+stroke_width/2, stroke_width=stroke_width, fill="none", stroke="#F7BD13")
            else:
                offset = pin_width/3.
                svg.add_path(transform="rotate(90,0,0)",
                        d=(
                        svg.M(-pin_width/2+offset, -pin_height/2),
                        svg.h(pin_width-offset*2),
                        svg.l(offset, offset),
                        svg.v(pin_height-offset*2),
                        svg.l(-offset, offset),
                        svg.h(-pin_width+offset*2),
                        svg.l(-offset, -offset),
                        svg.v(-pin_height+offset*2),
                        svg.z(),
                        svg.M(0,-d/2),
                        svg.A(d/2, d/2, 0,1,0, 0, d/2), 
                        svg.A(d/2, d/2, 0,1,0, 0, -d/2), # can not draw a whole circle at once :-P
                        svg.z()
                        ), fill="#F7BD13")
            if nr != None:
                arg = dict(id="connector{0}pin".format(nr))
            else:
                arg = dict()
            svg.add_circle(0,0, d/2+stroke_width/2, stroke_width=stroke_width, fill="none", stroke="#F7BD13", **arg)


    else:
        is_smd = True
        pin_width,pin_height = map(to_pixel, size.split(","))
        def add_pin(nr):
            if nr != None:
                arg = dict(id="connector{0}pin".format(nr))
            else:
                arg = dict()
            svg.add_rect(-pin_width/2, -pin_height/2, pin_width, pin_height, fill="#F7BD13",
                    transform="rotate(90,0,0)", **arg)

    count = len(p.getPins())

    if chip_height == None:
        # only two sides
        svg_width = chip_width+pin_height
        svg_height = pins_gap*(count/2 )+1

        svg.start(svg_width, svg_height, svg_width*127/360, svg_height*127/360, "mm")
        #svg.add_rect(-500,-500,1000,1000) # debug
        transform_translate="translate({x},{y})".format(x=svg_width/2, y=0.5 + pins_gap * 0.5)
        offset = pin_height/2 + 1.5
        svg.add_start_g(id="silkscreen", transform=transform_translate)
        svg.add_path(d=(
                svg.M(-chip_width/2 + offset, 0-0.5*pins_gap),
                svg.v(pins_gap*count/2),
                svg.h(chip_width-offset*2),
                svg.v(-pins_gap*count/2),
                svg.z()
                ), stroke="ffffff", fill="none")
        svg.add_circle(-chip_width/2 + offset + 3,-0.25*pins_gap +1 ,1.5, fill="#ffffff")
        svg.add_end_g()

        svg.add_start_g(id="copper1", transform=transform_translate)
        if not is_smd: svg.add_start_g(id="copper0")
        for i in range(count/2):
            #left
            svg.add_start_g(transform="translate({x},{y})".format(x=-chip_width/2,y=i*pins_gap))
            add_pin(i+1)
            svg.add_end_g()

            #right
            svg.add_start_g(transform="translate({x},{y})".format(x=+chip_width/2,y=(count/2-1-i)*pins_gap))
            add_pin(count-i)
            svg.add_end_g()

        if not is_smd: svg.add_end_g()
        svg.add_end_g()
    else:
        # 4 sides of pins
        
        svg_width = chip_width + pin_height
        svg_height = chip_height + pin_height

        svg.start(svg_width, svg_height, svg_width*127/360, svg_height*127/360, "mm")
        #svg.add_rect(-500,-500,1000,1000,fill="#cccccc") # debug
        transform_translate = "translate({x},{y})".format(x=chip_width/2+pin_height/2, y=chip_height/2+pin_height/2)
        #svg.add_circle(0,0,1,fill="0000ff") # debug
        
        offset_h = (chip_height - (count/4-1)*pins_gap) / 2
        offset_v = (chip_width - (count/4-1)*pins_gap) / 2

        svg.add_start_g(id="silkscreen", transform=transform_translate)
       
        svg.add_circle(-chip_width/2, -chip_height/2, pin_height/2, fill="#fff")

        for angle in (0,90,180,270):
            svg.add_path(d=(
                svg.M(-chip_width/2 + offset_h - 1, -chip_height/2),
                svg.h(-offset_h+1),
                svg.v(+offset_v-1),
                ),      fill="none",
                        stroke="ffffff",
                        stroke_width="0.5",
                        transform="rotate({angle})".format(angle=angle))

        svg.add_end_g()


        svg.add_start_g(id="copper1", transform=transform_translate)
        if not is_smd: svg.add_start_g(id="copper0")

        def add_pin_shortcut(i,x,y,r=0):
            pin_nr = i
            svg.add_start_g(transform="translate({x},{y})".format(
                                x=x,
                                y=y))
            if r != 0: svg.add_start_g(transform="rotate({0})".format(r))
            add_pin(pin_nr)
            svg.add_end_g()
            if r != 0: svg.add_end_g()

        for i in range(count/4):
            #left
            add_pin_shortcut(
                    i=i+1,
                    x=-chip_width/2,
                    y=-chip_height/2 + offset_h + pins_gap*i)
            
            #bottom
            add_pin_shortcut(
                    i=1+ count/4 + i,
                    x=-chip_width/2 + offset_v + pins_gap*i,
                    y=chip_height/2,
                    r=90)
            
            #right
            add_pin_shortcut(
                    i=1+ 2*count/4 + i,
                    x=chip_width/2,
                    y=+chip_height/2 - offset_h - pins_gap*i)
            
            #top
            add_pin_shortcut(
                    i=1+ 3*count/4 + i,
                    x=chip_width/2 - offset_v - pins_gap*i,
                    y=-chip_height/2,
                    r=90)

        if not is_smd: svg.add_end_g()
        svg.add_end_g()

    svg.end()
    svg.write(file_name)




