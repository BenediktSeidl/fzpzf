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
#

import BaseHTTPServer
import SocketServer
import json
import time
import glob
import os
import stat
import math
import subprocess
import mimetypes

def get_files():
    all_files = glob.glob("../*.py")
    all_files += glob.glob("../parts/*")
    for root, dirs, files in os.walk('../packages'):
        files = filter(lambda f: f[0] != "." , files)
        all_files += map(lambda f: root +"/"+ f, files)
    return all_files

class myHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        if "?" in self.path:
            self.path = self.path.split("?")[0]

        if self.path in ["/favicon.ico", "/script.js", "/index.html", "/jquery-1.6.4.min.js", "/style.css"]:
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(self.path)[0])
            self.end_headers()
            f = open(self.path[1:])
            self.wfile.write(f.read())
            f.close()
        elif self.path == "/files":
            self.send_response(200)
            self.send_header("Content-Type", "")
            self.end_headers()
            files = map(os.path.basename, glob.glob("../temp/*.*"))
            self.wfile.write(json.dumps(files))
        elif self.path.startswith("/file/"):
            file_name = os.path.basename(self.path)
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(self.path)[0])
            self.end_headers()
            f = open("../temp/{0}".format(file_name))
            self.wfile.write(f.read())
            f.close()
        elif self.path == "/poll":
            self.send_response(200)
            self.end_headers()
            last_diff = 0
            for i in range(100):
                time.sleep(1)
                if not cfc:
                    return
                last_change = max(map(lambda f: os.stat(f)[stat.ST_MTIME], get_files()))
                diff = math.floor(time.time()) - last_change
                print "check_for_change:", diff
                if  diff < last_diff:
                    # now we have to execute the script
                    p = subprocess.Popen(["./execute.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    code = p.wait()
                    data = dict(executed = True, returncode = code, stdout = p.stdout.read(), stderr = p.stderr.read())
                    self.wfile.write(json.dumps(data))
                    return
                last_diff = diff
            data = dict(executed = False)
            self.wfile.write(json.dumps(data))
        else:
            self.send_error(404)

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

def run(server_class=ThreadedHTTPServer, handler_class=myHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    global cfc
    cfc = True
    print "starting server"
    print "surf to http://localhost:8000/"
    try:
        run()
    except KeyboardInterrupt:
        print "stopped via keyboardinterrupt"
        cfc = False
        print "also stopped check for changes"
