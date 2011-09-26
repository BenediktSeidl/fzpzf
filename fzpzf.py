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

import pcb
import module
from models import parse
import breadboard
import schematic

from glob import glob
import zipfile


for file_name in glob("parts/*.part"):
    meta, packages, schem = parse(file_name)
    breadboard_file_name = "{0}_breadboard.svg".format(meta.name)
    schematic_file_name = "{0}_schematic.svg".format(meta.name)
    icon_file_name = "{0}_icon.svg".format(meta.name)

    breadboard.create(len(schem.pins.getPins())/2,4,meta.name, file_name="temp/"+breadboard_file_name)
    schematic.create(schem, file_name="temp/" + schematic_file_name)

    for p in packages:
        name = "{0}_{1}".format(meta.name, p.definition["name"])
        pcb_file_name = "{0}_pcb.svg".format(name)
        module_file_name = "{0}.fzp".format(name)
        pcb.create(p, file_name="temp/" + pcb_file_name)
        module.create(
            meta, p, schem,
            breadboard_file_name=breadboard_file_name,
            schematic_file_name=schematic_file_name,
            pcb_file_name=pcb_file_name,
            icon_file_name=icon_file_name,
            file_name="temp/{0}".format(module_file_name))

        zip_file = zipfile.ZipFile("out/{0}.fzpz".format(name), "w")
        zip_file.write("temp/{0}".format(pcb_file_name), "svg.pcb.{0}".format(pcb_file_name))
        zip_file.write("temp/{0}".format(breadboard_file_name), "svg.breadboard.{0}".format(breadboard_file_name))
        zip_file.write("temp/{0}".format(breadboard_file_name), "svg.icon.{0}".format(icon_file_name))
        zip_file.write("temp/{0}".format(schematic_file_name), "svg.schematic.{0}".format(schematic_file_name))
        zip_file.write("temp/{0}".format(module_file_name), "part.{0}".format(module_file_name))
        zip_file.close()
