import os
import sys
import argparse
from PIL.Image import open as pillow_open


def get_args():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('input', type=str, help='input image name')
    parser.add_argument('--width', type=int, help='width required image')
    parser.add_argument('--height', type=int, help='height required image')
    parser.add_argument('--scale', type=float, help='scale required image')
    parser.add_argument('--output', type=str, help='output image name')
    return parser.parse_args()


def get_parameter_combination_error(width, height, scale):
    if width is not None and height is not None and scale is not None:
        return 'You have scale option with width and/or height option'
    elif width is None and height is None and scale is None:
        return 'You must use scale or width and height option'
    elif width is not None and scale is not None:
        return 'You should not use scale'
    elif height is not None and scale is not None:
        return 'You should not use scale'
    else:
        return None


def get_check_proportion_warning(image_original_width, image_original_height, image_new_width, image_new_height):
    original_proportion = image_original_width / image_original_height
    new_proportion = image_new_width / image_new_height
    if original_proportion != new_proportion:
        return 'Warning image proportions will break'
    return None


def get_width_and_height(width, height, scale):
    image_original_width, image_original_height = get_image_size(args)
    if width is not None and height is not None:
        proportion_warning = get_check_proportion_warning(image_original_width, image_original_height, width, height)
        if proportion_warning is not None:
            print(proportion_warning)
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


def get_resized_image(input_file_name, width, height):
    with pillow_open(input_file_name) as f:
        return f.resize((width, height))


def get_image_size(args):
    with pillow_open(args.input) as f:
        return f.width, f.height


if __name__ == '__main__':
    args = get_args()
    args_width = args.width
    args_height = args.height
    args_scale = args.scale
    input_file_name = args.input
    if not os.path.exists(input_file_name):
        sys.exit('File {} does not exists'.format(input_file_name))
    parameter_combination_error = get_parameter_combination_error(args_width, args_height, args_scale)
    if parameter_combination_error is not None:
        sys.exit(parameter_combination_error)
    width, height = get_width_and_height(args_width, args_height, args_scale)
    output_file_name = args.output if args.output is not None else get_default_output_file_name(
        input_file_name, width, height)
    resized_image = get_resized_image(input_file_name, width, height)
    resized_image.save(output_file_name)
