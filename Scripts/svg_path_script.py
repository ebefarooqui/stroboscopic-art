import os
import numpy
import svgwrite
from svgpathtools import *
from subprocess import check_call

def create_svg (orig_file):
    bitmap_file = "./test_bitmap.ppm"
    f = open(bitmap_file,"w+")
    svg_file = "./test.svg"
    s = open(svg_file, "w+")
    os.system("magick convert " + orig_file + " " + bitmap_file)
    os.system("potrace -s " + bitmap_file + " -o" + svg_file)
    return svg_file

svg_path = create_svg("./test3.jpg")
print(svg2paths(svg_path))
paths, attributes = svg2paths(svg_path)
disvg(paths=paths, attributes=attributes,  filename="output.svg")
os.system("magick convert " + "output.svg " + "output.jpg")
