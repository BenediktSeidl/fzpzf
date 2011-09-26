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

import re
from helper import error

class Meta(object):
    def __init__(self):
        self.name = "Unnamed"
        self.TAGS = ""

    def addData(self, topic, data):
        if topic in ["NAME"]:
            setattr(self, topic.lower(), data[0])
        else:
            setattr(self, topic.lower(), data)

class Pins(object):
    def __init__(self, meta):
        self.data = dict()
        self.meta = meta

    def addPin(self, num, desc):
        if num in self.data:
            error("pin number %s already defined" % num)
        self.data[num] = desc
    
    def getPin(self, num):
        return self.data[num]

    def isEmpty(self):
        return len(self.data) == 0

    def addLine(self, line):
        if line[0] != "$":
            print line[0]
            error("Pins: parse error at %s" % line)
        data = re.split("\s+", line[1:], 2)
        if len(data) < 2:
            error("Pins: sorry")
        elif len(data) == 2:
            num,val = data
            description = val
        elif len(data) == 3:
            num,val,description = data
        try:
            num = int(num)
        except:
            error("not a number at %s" % line)
        self.addPin(num, (val,description))

    def getPins(self):
        data = []
        for num in sorted(self.data.keys()):
            data.append(self.data[num])
        return data

class Package(object):
    def __init__(self, package, pins, meta):
        self.meta = meta
        
        package = package.strip()
        self.pins = pins
        self.data = dict()

        try:
            f = open("packages/{0}".format(package))
        except:
            error("can not find package '{0}'".format(package))
            return
        ### let's parse the file
        self.definition=dict(pin=None, c=None, ch=None, e=None, name="-")
        for line in f.read().split("\n"):
            if line.strip() == "":
                continue
            if line[0] == "#":
                continue
            key, value = line.split(" ", 1)
            key = key[1:]
            if key.lower() in self.definition:
                self.definition[key.lower().strip()] = value.strip()
            else:
                error("Package: '{0}' not a definition".format(key))


    def addPin(self, num, val):
        self.data[num] = val

    def getPin(self, num):
        return self.data[num]

    def addLine(self, line):
        m = re.match("^([\d]+)\s*->\s*\$([\d]+)\s*$", line)
        if not m:
            splitedLine = line.split(" ", 1)
            name = splitedLine[1].strip()
            if name != "NC":
                error("can not define new pins here, just NC or references to existing ones")
            self.addPin(int(splitedLine[0]), None)
        else:
            self.addPin(*map(int, m.groups()))

    def getPins(self):
        if len(self.data) == 0:
            return self.pins.getPins()
        else:
            data = [] # this should be a dict
            for num in sorted(self.data.keys()):
                val = self.data[num]
                if type(val) == int:
                    data.append(self.pins.getPin(val))
                else:
                    data.append(val)
            return data

class Schematic(object):
    def __init__(self, pins, meta):
        self.meta = meta
        self.data = dict(R=[], L=[], T=[], B=[])
        self.pins = pins

    def addSide(self, side, pins):
        if side in self.data and self.data[side] != []:
            error("side %s already defined" % side)
        self.data[side] = pins

    def addLine(self, line):
        if line[0] not in "TLRB":
            error("side %s does not exist, only R, L, T, and B are valid")
        side = line[0]
        pins = line[1:].split(",")
        parsedPins = []
        for pin in pins:
            pin = pin.strip()
            if len(pin) == 0:
                parsedPins.append(None)
                continue
            if pin[0] != "$":
                error("SCHEMATIC: pins should have a $")
            try:
                num = int(pin[1:])
            except:
                error("SCHEMATIC: pins must be integers")
            parsedPins.append(num)
        self.addSide(side, parsedPins)

    def getSide(self, side):
        if side not in "TLRB":
            error("pffff!")
        if self.data.values() == [[],[],[],[]]:
            count = len(self.pins.data)
            halfe = count/2
            if side == "L":
                return range(1,halfe+1)
            elif side == "R":
                return range(halfe+1,count+1)[::-1]
            elif side == "T":
                return [None]*4
        return self.data[side]


def parse(fileName):
    f = file(fileName)
    data = f.read()

    metaTopics = ["NAME", "TAGS"]
    topics = metaTopics + ["PINS", "PACKAGE", "SCHEMATIC"]

    meta = Meta()
    pins = Pins(meta)
    packages = []
    schematic = Schematic(pins, meta)

    for line in data.split("\n"):
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue
        if line[0] == '*':
            splitedLine = line[1:].split(" ")
            topic = splitedLine[0]
            if len(splitedLine) != 0:
                data = " ".join(splitedLine[1:]).split(",")
            else:
                data = []
            if topic not in topics:
                error("%s: topic not known" % topic)

            if topic in metaTopics:
                meta.addData(topic, data)
            elif topic == "PINS":
                currentTopic = pins
            elif topic == "PACKAGE":
                currentTopic = Package(data[0], pins, meta)
                packages.append(currentTopic)
            elif topic == "SCHEMATIC":
                currentTopic = schematic
        else:
            currentTopic.addLine(line)

    return meta, packages, schematic

