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

import time
import random

head = """<?xml version="1.0" encoding="UTF-8"?>
<module fritzingVersion="0.1.1201" moduleId="{module_id}">
    <version>{version}</version>
    <title>{title}</title>
    <label>{label}</label>
    <date>{date}</date>
    <author>{author}</author>
    <tags>
        {tags}
    </tags>
    <properties>
      <property name="family">{family}</property>
      <property name="package">{package}</property>
    </properties>
"""

tag = """<tag>{tag}</tag>"""

view = """<views>
        <iconView>
            <layers image="icon/{icon_file}">
                <layer layerId="icon"/>
            </layers>
        </iconView>
        <breadboardView>
            <layers image="breadboard/{breadboard_file}">
                <layer layerId="breadboard"/>
            </layers>
        </breadboardView>
        <schematicView>
            <layers image="schematic/{schematic_file}">
                <layer layerId="schematic"/>
            </layers>
        </schematicView>
        <pcbView>
            <layers image="pcb/{pcb_file}">
                {copper_layers}
                <layer layerId="silkscreen"/>
            </layers>
        </pcbView>
    </views>"""

copper_layer = """<layer layerId="copper{0}"/>"""

connector = """
        <connector id="connector{id}" name="{name}" type="{type}">
            <description>{description}</description>
            <views>
                <breadboardView>
                    <p layer="breadboard" svgId="connector{id}pin" terminalId="connector{id}terminal"/>
                </breadboardView>
                <schematicView>
                    <p layer="schematic" svgId="connector{id}pin" terminalId="connector{id}terminal"/>
                </schematicView>
                <pcbView>
                    {copper_ps}
                </pcbView>
            </views>
        </connector>"""
    
copper_p = """<p layer="copper{nr}" svgId="connector{id}pin"/>"""

connectors_start = """<connectors>"""
connectors_end = """</connectors>"""
footer = """
</module>
"""
text = ""
def append(string):
    global text
    text += string

def new():
    global text
    text = ""

def create(meta, package, schematic, breadboard_file_name, schematic_file_name, pcb_file_name, icon_file_name, file_name):
    unique_id = "{0}-{1}".format(int(time.time()*100), "".join([random.choice("1234567890") for i in range(20)]))
    is_smd = not package.definition["pin"].startswith("THT")
    num_copper_layers = [1] if is_smd else [0,1]
    
    new()

    append(head.format(
        module_id=unique_id,
        version="0.1 ({time})".format(time = time.strftime("%Y-%m-%d")),
        title=meta.name,
        label="IC1",
        date=time.strftime("%Y-%m-%d"),
        author="#TODO",
        tags="\n".join(tag.format(tag=t) for t in meta.tags),
        family=meta.name,
        package=package.definition["name"]))

    copper_layers= "\n".join(copper_layer.format(i) for i in num_copper_layers)

    append(view.format(
        icon_file=icon_file_name,
        breadboard_file=breadboard_file_name,
        schematic_file=schematic_file_name,
        pcb_file=pcb_file_name,
        copper_layers=copper_layers,
        ))

    append(connectors_start)
    for i,(name,description) in enumerate(schematic.pins.getPins()):
        copper_ps = "\n".join(copper_p.format(nr=j, id=i+1) for j in num_copper_layers)
        append(connector.format(
            id = i+1,
            type = "pad" if is_smd else "male",
            name=name,
            description=description,
            copper_ps = copper_ps))




    append(connectors_end)

    append(footer)
    f = open(file_name, "w")
    f.write(text)
