import os
import sys
import argparse
from PIL.Image import open as pillow_open


class ResizeException(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('input', type=str, help='input image name')
    parser.add_argument('--width', type=int, help='width required image')
    parser.add_argument('--height', type=int, help='height required image')
    parser.add_argument('--scale', type=float, help='scale required image')
    parser.add_argument('--output', type=str, help='output image name')
    return parser.parse_args()


def validate_parameters(width, height, scale):
    if width is not None and height is not None and scale is not None:
        print('You have scale option with width and/or height option')
        sys.exit(1)
    elif width is None and height is None and scale is None:
        print('You must use scale or width and height option')
        sys.exit(1)
    elif width is not None and scale is not None:
        print('You should not use scale')
        sys.exit(1)
    elif scale is not None:
        print('You should not use scale')
        sys.exit(1)


def _check_proportion(image_original_width, image_original_height, image_new_width, image_new_height):
    original_proportion = image_original_width / image_original_height
    new_proportion = image_new_width / image_new_height
    if original_proportion != new_proportion:
        print('Warning image proportions will break')


def get_width_and_height(width, height, scale):
    image_original_width, image_original_height = get_image_size(args)
    if width is not None and height is not None:
        _check_proportion(image_original_width, image_original_height, width, height)
        return width, height
    elif width is None and height is None:
        return int(image_original_width * scale), int(image_original_height * scale)
    elif width is not None:
        calculated_scale = width / image_original_width
        return width, int(image_original_height * calculated_scale)
    else:
        calculated_scale = height / image_original_height
        return int(image_original_width * calculated_scale), height


def get_default_output_file_name(input_file_name, image_width, image_height):
    root, ext = os.path.splitext(input_file_name)
    return '{root}__{width}x{height}{ext}'.format(
        root=root, width=image_width, height=image_height, ext=ext
    )


def resize_image(input_file_name, output_file_name, width, height):
    with pillow_open(input_file_name) as f:
        im = f.resize((width, height))
    im.save(output_file_name)


def get_image_size(args):
    with pillow_open(args.input) as f:
        return f.width, f.height


def check_input_file_existence(input_file_name):
    if not os.path.exists(input_file_name):
        print('File {} does not exists'.format(input_file_name))
        sys.exit(1)

if __name__ == '__main__':
    args = get_args()
    args_width = args.width
    args_height = args.height
    args_scale = args.scale
    input_file_name = args.input
    check_input_file_existence(input_file_name)
    validate_parameters(args_width, args_height, args_scale)
    width, height = get_width_and_height(args_width, args_height, args_scale)
    output_file_name = args.output if args.output is not None else get_default_output_file_name(
        input_file_name, width, height)
    resize_image(input_file_name, output_file_name, width, height)
