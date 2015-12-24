#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import subprocess
import multiprocessing
import time
import shutil
import signal
import argparse


def worker_init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def convert(f):
    root, fileext = os.path.splitext(f)
    if fileext == '.m4a':
        out = root + '.mp3'
        if os.path.exists(out):
            return
        args = ['ffmpeg', '-y', '-i', f, out]
        sys.stdout.write("converting {}\n".format(f))
        p = subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        status = os.waitpid(p.pid, 0)[1]
        if status == 0:
            sys.stdout.write("{} converted to {} ok\n".format(f, out))
        else:
            sys.stdout.write("{} converted to {} failed\n".format(f, out))
    else:
        sys.stderr.write("{} not a m4a file\n".format(f))


def rename(f):
    relpath = os.path.relpath(f)
    seps = relpath.split("/")[1:]
    if len(seps) != 3:
        return
    root, fileext = os.path.splitext(f)
    if fileext == ".mp3":
        newpath = os.path.join(
            "Musics", "{}.{}.{}".format(seps[0], seps[1], seps[2]))
        if not os.path.exists(newpath):
            print("copying {} to {}".format(f, newpath))
            shutil.copyfile(f, newpath)


def to_backup(f):
    root, fileext = os.path.splitext(f)
    if fileext == ".mp3":
        os.rename(f, f + ".backup")


def from_backup(f):
    root, fileext = os.path.splitext(f)
    if fileext == ".backup":
        os.rename(f, root)


def list_files_recursively(dirpath):
    for root, subFolders, files in os.walk(dirpath):
        for f in files:
            yield os.path.join(root, f)


def tasks_from_targets(targets):
    for target in targets:
        if os.path.isdir(target):
            yield from list_files_recursively(target)
        elif os.path.isfile(target):
            yield target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', help="action")
    parser.add_argument(
        'targets', nargs=argparse.REMAINDER, help="action targets")
    options = parser.parse_args()
    if options.action == "convert":
        action = convert
    elif options.action == "rename":
        action = rename
    elif options.action == "to_backup":
        action = to_backup
    elif options.action == "from_backup":
        action = from_backup
    else:
        print("no action")
        sys.exit(1)
    tasks = tasks_from_targets(options.targets)
    pool = multiprocessing.Pool(
        processes=multiprocessing.cpu_count(), initializer=worker_init)
    try:
        # See http://stackoverflow.com/a/1408476/288089.
        if sys.version_info.major >= 3 and sys.version_info.minor >= 4:
            # See http://bugs.python.org/issue9205.
            pool.map(action, tasks)
        else:
            pool.map_async(
                action, tasks).get(2 ^ 32)
        pool.close()
    except KeyboardInterrupt:
        print("terminating")
        pool.terminate()
    pool.join()
    print("done")
