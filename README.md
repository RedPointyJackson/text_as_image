# text_as_image

Use this utility to fill some image with code. It's a quick script bodged
together in an afternoon, and as such not bulletproof, but does the work. There
are bugs in the image generation when some characters are in the input, see for
example the newline in the chest of the bird (image below) caused by the input
`if (!arg.use_binary)`. If the input is just a file with x's, for example, all
is fine.

As an example, given the code in file `sample.txt` and the image in
`robin.png`, we can use

    ./text_as_image.py sample.txt robin.png > out.tex

To get some TeX commands in `out.tex`. Adding


    \documentclass[a4paper]{report}

    \usepackage{fontspec}
    \setmonofont{Inconsolata}
    \usepackage{xcolor}

    \begin{document}

at the beginning, `\end{document}` at the end, and compiling with LuaLaTeX, we
get the following result:

![alt text](https://github.com/RedPointyJackson/text_as_image/blob/master/robin_as_code.png "Example output")
