#!/usr/bin/env python
# -*- coding: utf-8 -*-


from xml.dom import minidom

xml_document = None
svg = None
insertPoint = None

def append(newElement):
    #global text
    #text += newText + "\n"
    global insertPoint
    insertPoint.appendChild(newElement)

def start(width, height, w_unit, h_unit, unit):
    new()
    global svg
    svg.setAttribute("viewBox", "0 0 {w} {h}".format(w=width, h=height))
    svg.setAttribute("width", "{w_unit}{unit}".format(unit=unit, w_unit=w_unit))
    svg.setAttribute("height", "{h_unit}{unit}".format(unit=unit, h_unit=h_unit))

def end(): # TODO: remove
    pass 

def write(file_name="test.svg"):
    f = file(file_name, "w")
    #f.write(text)
    xml_document.writexml(f,
            indent="  ",
            addindent="  ",
            newl="\n",
            encoding="UTF-8")
    f.close()

def new():
    global xml_document, svg, insertPoint

    domi = minidom.getDOMImplementation()
    documentType = domi.createDocumentType(
            "svg",
            "-//W3C//DTD SVG 1.1//EN",
            "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd")
    xml_document = domi.createDocument(
            "eins",
            "svg",
            documentType)
    
    svg = xml_document.documentElement
    attributes = [("xmlns", "http://www.w3.org/2000/svg"),
            ("xmlns:xlink", "http://www.w3.org/1999/xlink"),
            ("xmlns:ev", "http://www.w3.org/2001/xml-events"),
            ("version", "1.1"),
            ("baseProfile","full"),
            ]

    for name, value in attributes:
        svg.setAttribute(name, value)

    insertPoint = svg


############ helper functions ###############

def deCamelCase(string):
    return string.lower().replace("__", ":").replace("_", "-")

def _xml(arg):
    return " ".join(('{0}="{1}"'.format(deCamelCase(key), value) for key,value in arg.iteritems()))

def xml(name, content=None, **arg):
    global xml_document
    element = xml_document.createElement(name)
    for name, value in arg.iteritems():
        element.setAttribute(
            name.lower().replace("__", ":").replace("_", "-"),
            str(value))
    if content != None:
        element.appendChild(xml_document.createTextNode(content))
    return element
        

####### svg wrapper ##########

def add_rect(x,y,w,h, **arg):
    append(xml("rect", x=x, y=y, width=w, height=h, **arg))

def add_line(x,y,ox,oy, **arg):
    append(xml("line", x1=x, y1=y, x2=x+ox, y2=y+oy, **arg))

def add_text(text, **arg):
    append(xml("text", content=str(text), **arg))

def add_circle(x,y,r, **arg):
    append(xml("circle", cx=x, cy=y, r=r, **arg))

def add_start_g(**arg):
    "start a group"
    #append("<g {0}>".format(_xml(arg)))
    global insertPoint
    append(xml("g", **arg))
    insertPoint = insertPoint.lastChild

def add_end_g():
    "end a group"
    global insertPoint
    insertPoint = insertPoint.parentNode
    #append("</g>")

def add_use(link, **arg):
    print "WARNING! not supported by fritzing"
    append(xml("use", xlink__href=link, **arg))

def add_path(d, **arg):
    "add a path"
    append(xml("path", d=" ".join(d), **arg))

def add_polygon(**arg):
    append(xml("polygon", **arg))


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


######### test #########
if __name__ == "__main__":
    start(10,10,10,10,"mm")
    add_circle(5,5,10)
    add_start_g()
    add_circle(1,1,1)
    add_end_g()
    write()
