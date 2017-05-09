import os
import sys
import argparse
from PIL.Image import open


class ResizeException(Exception):
    pass


def get_args():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('input', type=str, help='input image name')
    parser.add_argument('--width', type=int, help='width required image')
    parser.add_argument('--height', type=int, help='height required image')
    parser.add_argument('--scale', type=int, help='scale required image')
    parser.add_argument('--output', type=str, help='output image name')
    return parser.parse_args()


def _check_scale_arg(args, is_none):
    if is_none is True and args.scale is not None:
        raise ResizeException('You have scale option with width and/or height option')
    elif is_none is False and args.scale is None:
        raise ResizeException('You must use scale or width and height option')


def get_width_and_height(args):
    image_original_width, image_original_height = get_image_size(args)
    if args.width is not None and args.height is not None:
        _check_scale_arg(args, is_none=True)
        original_proportion = image_original_width / image_original_height
        new_proportion = args.width / args.height
        if original_proportion != new_proportion:
            print('Warning image proportions will break')
        return args.width, args.height
    elif args.width is None and args.height is None:
        _check_scale_arg(args, is_none=False)
        return int(image_original_width * args.scale), int(image_original_height * args.scale)
    elif args.width is not None:
        _check_scale_arg(args, is_none=True)
        scale = args.width / image_original_width
        return args.width, int(image_original_height * scale)
    else:
        _check_scale_arg(args, is_none=True)
        scale = args.height / image_original_height
        return int(image_original_width * scale), args.height


def get_output_file_name(args, image_width, image_height):
    if args.output is not None:
        return args.output
    input_file_name = args.input
    root, ext = os.path.splitext(input_file_name)
    return '{root}__{width}x{height}{ext}'.format(
        root=root, width=image_width, height=image_height, ext=ext
    )


def resize_image(args):
    size = get_width_and_height(args)
    output_file_name = get_output_file_name(args, *size)
    with open(args.input) as f:
        im = f.resize(size)
    im.save(output_file_name)


def get_image_size(args):
    with open(args.input) as f:
        return f.width, f.height

if __name__ == '__main__':
    args = get_args()
    try:
        resize_image(args)
    except ResizeException as e:
        print(e)
        sys.exit(1)
