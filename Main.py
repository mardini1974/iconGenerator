#!/usr/local/bin/python
# !/usr/bin/env python

import sys, os
from PIL import Image
import argparse


def generate_fusion360_icon_images(icon_filename, minsize):
    # sizes = ["16x16", "32x32", "16x16@2x", "32x32@2x"]
    sizes = ["16", "32", "64", "128", "512"]
    image_name = icon_filename
    if os.path.isfile(image_name) is False:
        sys.exit("Missing {0} file".format(image_name))
    image_name = f"{os.getcwd()}/{image_name}"
    img = Image.open(image_name)

    # Check image size
    # if img.size < (1024, 1024):
    #     sys.exit("{0} size is {1}. Must be 1024x1024 or higher.".format(image_name, img.size))


    folder = icon_filename.split(".")
    # Create Assets folder
    current_dir = os.getcwd()
    asset_dir = f"{current_dir}/{folder[0]}"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)
    os.chdir(asset_dir)

    for size in sizes:
        for multiplier in range(1, 3):
            if minsize == "1":
                i = img.resize((multiplier * int(size), multiplier * int(size)), Image.ANTIALIAS)
            else:
                width = int(multiplier * int(size) * int(minsize)/16)
                i = img.resize((width, width), Image.ANTIALIAS)

            img_filename_normal = f"{size}x{size}-normal"
            img_filename_disabled = f"{size}x{size}-disable"
            img_filename_dark = f"{size}x{size}-dark"
            if multiplier > 1:
                save_name_normal = f"{img_filename_normal}@2x"
                save_name_disable = f"{img_filename_disabled}@2x"
                save_name_dark = f"{img_filename_dark}@2x"
            else:
                save_name_normal = img_filename_normal
                save_name_disable = img_filename_disabled
                save_name_dark = img_filename_dark

            i.save(f"{save_name_normal}.png", format="PNG")
            i.save(f"{save_name_dark}.png", format="PNG")
            color_image = i.convert('LA').save(f"{save_name_disable}.png", format="PNG")
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Assets generator for iOS projects")
    parser.add_argument("--minsize",help="Minimum size at 16x16 version Default is 1 ", default=1)
    parser.add_argument("--icon", nargs='*', help="Generate icons assets")
    parser.parse_args()
    args = parser.parse_args()
    for arg in args.icon:
        generate_fusion360_icon_images(arg, args.minsize)
