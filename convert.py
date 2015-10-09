#!/usr/bin/env python
# encoding: utf-8
#
# Convert all m4a files to mp3.
#

import os
import sys
import subprocess

def convert(f):
    root, fileext = os.path.splitext(f)
    if fileext == '.m4a':
        out = root + '.mp3'
        if os.path.exists(out):
            return
        args = ['ffmpeg', '-y', '-i', f, out]
        sys.stdout.write("converting {}\n".format(f))
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        status = os.waitpid(p.pid, 0)[1]
        if status == 0:
            sys.stdout.write("{} converted to {} ok\n".format(f, out))
        else:
            sys.stdout.write("{} converted to {} failed\n".format(f, out))
    else:
        sys.stderr.write("{} not a m4a file\n".format(f))

def list_files_recursively(dirpath):
    for root, subFolders, files in os.walk(dirpath):
        for f in files:
            yield os.path.join(root, f)

if __name__ == '__main__':
    args = sys.argv[1:]
    for arg in args:
        if os.path.isdir(arg):
            for f in list_files_recursively(arg):
                convert(f)
        elif os.path.isfile(arg):
            convert(f)
        else:
            sys.stderr.write("{} ignored\n".format(arg))
