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

from svg import M,H,V,z,a,A,L # path commands
from svg import add_path, add_line, add_use, add_start_g, add_end_g
from svg import add_circle, add_text
from svg import start, end, write
from svg import append
from svg import xml

def add_bb_connector(num, y):
    append(xml("rect", x=-1.08,y=-1.08, width=2.16,height=2.16, id="connector{0}terminal".format(num), fill="none"))
    append(xml("rect", x=-1.08,y=y, width=2.16,height=3.24, id="connector{0}pin".format(num), fill="none"))

def create(width, height, name, file_name=None):
    if file_name == None:
        file_name = "breadboard_{0}.svg".format(name)

    inner_l = 3.6
    inner_r = 3.6 + width*7.2
    inner_t = 3.6 + 7.2
    inner_b = height*7.2 - 3.6

    outer_l = inner_l -1
    outer_r = inner_r +1
    outer_t = inner_t - 2.8
    outer_b = inner_b + 2.8

    center_x = 0.5*(inner_r+inner_l)
    center_y = 0.5*(inner_t+inner_b)

    circle_r = 3.6
    circle_t = center_y - circle_r
    circle_b = center_y + circle_r
    circle_half_way = inner_l + circle_r
    circle_inner_r = 1.8
    circle_inner_t = center_y - circle_inner_r
    circle_inner_b = center_y + circle_inner_r
    circle_inner_half_way = inner_l + circle_inner_r

    debug = False

    if debug:
        scale = 16
        start(1000, 1000, 1000, 1000, "px")
        add_start_g(transform='scale({s})'.format(s=scale))
        # grid
        for i in range(int(500/7.2)):
            add_line(0,i*7.2,500,0, color="#4affff", width=0.5)
            add_line(i*7.2,0,0,500, color="#4affff", width=0.5)
    else:
        scale = 1
        svg_width=outer_r-outer_l
        svg_height=(height-1)*7.2 + 2*1.08
        start(svg_width,svg_height, svg_width*127./360, svg_height*127./360, "mm")
        add_start_g(id='breadboard', transform='translate({x},{y})'.format(x=-outer_l, y=-(7.2-1.08)))

    append("""<defs>
     <polygon id="TopPin" fill="#8C8C8C" points="
      1.08,-1.08
     -1.08,-1.08

     -1.08,0.54
     -2.16,1.08
     -2.16,2.16

      2.16,2.16
      2.16,1.08
      1.08,0.54" />
      <use id="BottomPin" transform="rotate(180)" xlink:href="#TopPin"/>
    </defs>
    """)

    # dark background + left shadow
    add_path(d=(
    M(outer_l, outer_t),
    H(outer_r),
    V(outer_b),
    H(outer_l),
    z()
    ), fill="#202020")

    # main
    add_path(d=(
    M(inner_l, inner_t),
    V(circle_t),
    a(circle_r, circle_r, 0,1,1, 0, circle_r*2),
    V(inner_b),
    H(inner_r),
    V(inner_t),
    z()
    ), fill="#303030")

    #shadow top/bottom
    shadow_top = (
    M(outer_l, outer_t),
    H(outer_r),
    L(inner_r, inner_t),
    H(inner_l),
    z())
    add_path(d=shadow_top, fill="#3E3E3E")
    add_path(d=shadow_top, fill="#010101", transform="rotate(180, {0}, {1})".format(center_x, center_y),)

    #shadow right
    add_path(d=(
    M(outer_r, outer_t),
    V(outer_b),
    L(inner_r, inner_b),
    V(inner_t),
    z(),
    ), fill="#161616" )

    # shadow circle top
    add_path(d=(
    M(inner_l, circle_t),
    A(circle_r,circle_r, 0,0,1, circle_half_way, center_y),
    H(x=circle_inner_half_way),
    A(circle_inner_r, circle_inner_r, 0,0,0, inner_l, circle_inner_t),
    z()
    ), fill="#1c1c1c" )

    # shadow circle bottom
    add_path(d=(
    M(x=circle_half_way, y=center_y),
    A(circle_r, circle_r, 0,0,1, inner_l, circle_b),
    V(y=circle_inner_b),
    A(circle_inner_r, circle_inner_r, 0,0,0, circle_inner_half_way, center_y),
    z(),
    ), fill="#383838")

    # shadow half-circle
    add_path(d=(
    M(x=inner_l, y=circle_inner_t),
    A(circle_inner_r, circle_inner_r, 0,0,1, inner_l, circle_inner_b),
    z()
    ), fill="#272727")

    # pins
    for i in range(width):
        add_start_g(transform="translate({x},{y})".format(x=7.2*(1+i), y=7.2))
        add_use(link="#TopPin", x=0, y=0)
        add_bb_connector(width*2-i, y=-1.08)
        add_end_g()

        add_start_g(transform="translate({x},{y})".format(x=7.2*(1+i), y=(height)*7.2))
        add_use(link="#BottomPin")
        add_bb_connector(i+1, y=-2*1.08)
        add_end_g()

    # circle for pin #1
    add_circle(x=inner_l+4, y=inner_b-3, r=1.5,)

    # text
    add_text(text=name, fill="#e6e6e6",
            font_family="ocra10, OCRA", text_anchor="middle", font_size=5,
            x=center_x + circle_r/2, y=center_y+2)

    add_end_g()
    end()
    write(file_name)

