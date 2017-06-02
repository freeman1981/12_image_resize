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


def show_proportion_warning_if_necessary(image_original_width, image_original_height,
                                         image_new_width, image_new_height):
    original_proportion = image_original_width / image_original_height
    new_proportion = image_new_width / image_new_height
    if original_proportion != new_proportion:
        print('Warning image proportions will break')


def get_width_and_height(image_original_width, image_original_height, width, height, scale):
    if width is not None and height is not None:
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


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.input
    if not os.path.exists(input_file_name):
        sys.exit('File {} does not exists'.format(input_file_name))
    parameter_combination_error = get_parameter_combination_error(args.wigth, args.height, args.scale)
    if parameter_combination_error is not None:
        sys.exit(parameter_combination_error)
    original_image = pillow_open(input_file_name)
    width, height = get_width_and_height(
        original_image.width, original_image.height, args.wigth, args.height, args.scale)
    show_proportion_warning_if_necessary(original_image.width, original_image.height, width, height)
    output_file_name = args.output if args.output is not None else get_default_output_file_name(
        input_file_name, width, height)
    resized_image = original_image.resize((width, height))
    original_image.close()
    resized_image.save(output_file_name)
