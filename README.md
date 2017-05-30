# Image Resizer
## Installation
You should install Pillow.
```python3 -m pip install -r requirements.txt```

It is better use virtual enviroments
```python3 -m venv venv```
## How to use
```python3 image_resize.py --help```
will show options.
You should use --scale or --width and/or --height.

Use cases by using tree options:

scale|width|height|result
-----|-----|------|------
+|+|+|'You have scale option with width and/or height option' end exit
+|+|-|'You should not use scale' and exit
+|-|+|'You should not use scale' and exit
+|-|-|The input image will be resized by scale and saved in output
-|+|-|The input image will be resized and saved in output. Output proportion saved
-|-|+|The input image will be resized and saved in output. Output proportion saved
-|+|+|The input image will be resized and saved in output. If output proportion changed warning will appear

If no output parameter - output file will be saved in input/file__WidthxHeight.ext

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
