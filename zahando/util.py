from random import randint
import string
import config
import os

def generate_filename(extension):
    s = ""
    l = len(string.hexdigits) - 1
    for _ in range(12):
        s += string.hexdigits[randint(0, l)]
    if file_exists(s + extension):
        generate_filename(extension)
    return os.path.join(*config.path + [s + extension])

def file_exists(filename):
    path = os.path.join(*config.path + [filename])
    return os.path.isfile(path)

def make_dir():
    path = os.path.join(*config.path)
    if os.path.isdir(path):
        return
    os.makedirs(path)

