#!/usr/bin/env python
# -*- coding: utf-8 -*-

header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"
     version="1.1" baseProfile="full"
     viewBox="0 0 {w} {h}"
     width="{w_unit}{unit}" height="{h_unit}{unit}">
"""

footer = """</svg>"""

text = ""

def append(newText):
    global text
    text += newText + "\n"

def start(width, height, w_unit, h_unit, unit):
    new()
    append(header.format(w=width,h=height, h_unit=h_unit, w_unit=w_unit, unit=unit))

def end():
    append(footer)

def write(file_name="test.svg"):
    f = file(file_name, "w")
    f.write(text)
    f.close()

def new():
    global text
    text = ""

############ helper functions ###############

def deCamelCase(string):
    return string.lower().replace("__", ":").replace("_", "-")

def _xml(arg):
    return " ".join(('{0}="{1}"'.format(deCamelCase(key), value) for key,value in arg.iteritems()))

def xml(name, content=None, **arg):
    attributes = _xml(arg)
    if content == None:
        return "<{0} {1} />".format(name, attributes)
    else:
        return "<{0} {1}>{2}</{0}>".format(name, attributes, content)


####### svg wrapper ##########

def add_rect(x,y,w,h, **arg):
    append(xml("rect", x=x, y=y, width=w, height=h, **arg))

def add_line(x,y,ox,oy, **arg):
    append(xml("line", x1=x, y1=y, x2=x+ox, y2=y+oy, **arg))

def add_text(text, **arg):
    append(xml("text", content=text, **arg))

def add_circle(x,y,r, **arg):
    append(xml("circle", cx=x, cy=y, r=r, **arg))

def add_start_g(**arg):
    "start a group"
    append("<g {0}>".format(_xml(arg)))

def add_end_g():
    "end a group"
    append("</g>")

def add_use(link, **arg):
    print "WARNING! not supported by fritzing"
    append(xml("use", xlink__href=link, **arg))

def add_path(d, **arg):
    "add a path"
    append(xml("path", d=" ".join(d), **arg))

def M(x,y):
    "move to"
    return "M {x},{y}".format(x=x,y=y)
    
def H(x):
    "horizontal line, absolute coordinates"
    return "H {x}".format(x=x)

def V(y):
    "vertical line, absolute coordinates"
    return "V {y}".format(y=y)

def A(rx,ry, a,b,c, x,y):
    "part of a circle, absolute"
    return "A {rx} {ry} {a} {b} {c} {x} {y}".format(**locals())

def a(rx,ry, a,b,c, x,y):
    "part of a circle"
    return "a {rx} {ry} {a} {b} {c} {x} {y}".format(**locals())

def l(x,y):
    "line to, relative coordinates"
    return "l {x} {y}".format(x=x,y=y)

def L(x,y):
    "line to, absolute coordinates"
    return "L {x} {y}".format(x=x,y=y)

def h(x):
    return "h {x}".format(x=x)

def v(y):
    return "v {y}".format(y=y)

def z():
    "close path"
    return "z"

