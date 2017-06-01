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

WRONG PARAMETER COMBINATIONS

scale|width|height
-----|-----|------
+|+|+
+|+|-
+|-|+

RIGHT PARAMETER COMBINATIONS

scale|width|height|result
-----|-----|------|------
+|-|-|The input image will be resized by scale and saved in output
-|+|-|The input image will be resized and saved in output. Output proportion saved
-|-|+|The input image will be resized and saved in output. Output proportion saved
-|+|+|The input image will be resized and saved in output. If output proportion changed warning will appear

About output file name:

Assume we have image foo.png with size 100x100

```python3 image_resize.py foo.png --scale 0.1```
 
The image will appear with file name foo__10x10.png in same directory which foo.png
 
```python3 image_resize.py foo.png --width 5 --height 10```
 
The waring about proportion will show and image will appear with file name foo__5x10.png in same directory which foo.png


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
