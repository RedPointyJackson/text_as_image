# text\_as\_image

Use this utility to fill some image with code. It's a quick script bodged
together in an afternoon, and as such not bulletproof, but does the work. As an
example, given the code in file `sample.txt` and the image in `robin.png`, we
can use

    ./text_as_image.py sample.txt robin.png > out.tex

To get a LaTeX file in `out.tex`. Compiling with LuaLaTeX (or maybe XeLaTeX), we
get the following result:

![alt text](https://github.com/RedPointyJackson/text_as_image/blob/master/robin_as_code.png "Example output")
