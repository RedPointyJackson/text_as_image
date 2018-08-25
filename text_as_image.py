#!/usr/bin/env python3

"""
Output in stdout a .tex file where the TEXTFILE is laid over an IMG. The .tex
file is meant to be compiled by LuaLaTeX, but with manual tweaking it could
possibly be compiled with other engines.

Defaults are shown in [brackets]. Note that TEXTFILE should be trimmed of all
whitespace and breaklines, as the program does not do this automagically. For
example, instead of using

    #include <stdio.h>
    #include <stdlib.h>

    int main(int argc, char** argv){
        printf("%d\\n", 42);
    }

use

    #include <stdio.h> #include <stdlib.h> int main(int argc,
    char** argv){printf("%d\\n", 42);}

to get the picture correctly filled.
"""


import matplotlib.pyplot as plt
import numpy as np
from imageio import imread
from argparse import ArgumentParser, RawTextHelpFormatter
import sys

parser = ArgumentParser(description=__doc__,
                        formatter_class=RawTextHelpFormatter)
parser.add_argument("TEXTFILE", type=str,
                    help="Text file to use. Will use it as it is.")
parser.add_argument("IMG", type=str,
                    help="Image to use.")
parser.add_argument("-x", type=float, default=-2.5,
                    help="Horizontal kerning correction in pt [-2.5]")
parser.add_argument("-y", type=float, default=-1.2,
                    help="Interline spacing correction in pt [-1.2]")
parser.add_argument("-f", type=str, default='Inconsolata',
                    help="Font to use [Inconsolata]")
parser.add_argument("-p", type=float, default='5',
                    help="Size to use in points [5].")
args = parser.parse_args()

font_pt = args.p
font_h_correction_pt = args.x
font_v_correction_pt = args.y
font = args.f
text = open(args.TEXTFILE).read().strip()

img = imread(args.IMG)[:, :, :3]  # Discard alpha channel

print(args, file=sys.stderr)


def get_width_central_figure(arr):
    """
    Advance in the array `arr` until the pixels change:

    ----------X---XXX_----X-----XX-------
              ↑                  ↑
           'start'             'end'

    Return end - start.

    """
    start = 0
    end = 0
    for i, a in enumerate(arr):
        if a == arr[0]:
            start = i
        else:
            break
    for j, a in enumerate(reversed(arr)):
        if a == arr[-1]:
            end = len(arr) - 1 - j
        else:
            break
    return end - start


def measure_font(char, font, size):
    """
    Get width and height of a `char` (str) of the `font` (str) at size `size`
    pt (float) in pixels.
    """
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.text(0.5, 0.5, char,
            va='center', ha='center',
            size=size,
            fontname=font)
    fig.savefig('/tmp/text_as_image.png', dpi=300)
    char_img = imread('/tmp/text_as_image.png')
    x_size_px = get_width_central_figure(np.sum(char_img[:, :, 0], axis=0))
    y_size_px = get_width_central_figure(np.sum(char_img[:, :, 0], axis=1))
    return x_size_px, y_size_px

def escape(char):
    """
    Substitute the character for a LaTeX-safe escaped sequence.
    """
    subs = {'%': '\\%', '$': '\\$', '{': '\\{', '}': '\\}', '_': '\\_',
            '#': '\\#', '&': '\\&', '<': '\\textless', '^': '\\^',
            '\\': '\\textbackslash', '\n': ' '}
    return subs.get(char, char)

if __name__ == '__main__':

    dpi = 300
    px_in_mm = 25.4 / dpi

    font_width_px, font_height_px = measure_font('mAm', font, font_pt)
    font_width_px //= 3

    Ly, Lx, nchannels = img.shape

    xblocks = Lx // font_width_px
    yblocks = Ly // font_height_px

    char_idx = 0

    print(r"\documentclass[a4paper]{report}")
    print(r"\usepackage{xcolor}")
    print(r"\usepackage{fontspec}")
    print(r"\setmonofont{", font, "}", sep='')
    print(r"\begin{document}")

    print("{")
    print("\\bf")
    print("\\renewcommand{\\baselinestretch}{0}")

    print('\\fontsize{%dpt}{%dpt}\\selectfont' % (font_pt, int(1.14*font_pt)))

    for i in range(yblocks):
        for j in range(xblocks):

            if char_idx > len(text) - 2:
                print("Runned out of chars, wrapping.", file=sys.stderr)
                char_idx = 0

            chunk = img[i*font_height_px:(i+1)*font_height_px,
                        j*font_width_px:(j+1)*font_width_px,
                        :]
            r = np.median(chunk[:, :, 0])
            g = np.median(chunk[:, :, 1])
            b = np.median(chunk[:, :, 2])
            if r == g == b == 255:
                # Don't consume a character, print a dummy in white
                print("{\\color[RGB]{255,255,255} \\texttt{x}}", end='')
            else:
                while not text[char_idx].isprintable():
                    char_idx += 1
                char = text[char_idx]
                print("{\\color[RGB]{%d,%d,%d} \\texttt{%s}}" % (r, g, b, escape(char)), end='')
                char_idx += 1
            print('\\hspace{%lfpt}' % font_h_correction_pt)
        print()
        print("\\vspace{%lfpt}" % font_v_correction_pt)
        print()

    print("}")

    print(r"\end{document}")
