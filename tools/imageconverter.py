from PIL import Image
import numpy as np
import sys
import os
from tools.palettegenerator import Palette


def gen_palette(name, image_data):
    palette = Palette()
    palette.from_data(image_data)
    palette.write_palette("tools/palettes/" + name + ".pal")
    new = np.unique(image_data, return_inverse=True)[1]
    new = new.astype("u1").flatten()
    packed = (new[0::2] << 4) | new[1::2]
    packed.tofile("tools/converted/" + name + ".raw")
    print(f"saved palette size: {palette.size()}")


def convert_565(arr):
    r = arr[:, :, 0].astype(np.uint16)
    g = arr[:, :, 1].astype(np.uint16)
    b = arr[:, :, 2].astype(np.uint16)

    return (((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)).astype(">u2")


def convert_image(name, use_palette="false"):
    img = Image.open("tools/unconverted/" + name)
    name, _ = os.path.splitext(name)
    arr = np.asarray(img.convert("RGB"))
    rgb565 = convert_565(arr)
    print(f"input image width: {img.size[0]}\ninput image height: {img.size[1]}\n")
    print(
        f"saved image width: {rgb565.shape[1]}\nsaved image height: {rgb565.shape[0]}"
    )
    if use_palette.title() == "True":
        if rgb565.shape[1] % 2 != 0:
            raise ValueError("image width must be even if using palette")
        gen_palette(name, rgb565)
    else:
        rgb565.tofile("tools/converted/" + name + ".raw")


def convert_texture_map(name, rows, cols, use_palette="false"):
    map = Image.open("tools/unconverted/" + name)
    name, _ = os.path.splitext(name)
    arr = convert_565(np.asarray(map.convert("RGB")))
    sprite_w = map.size[0] // cols
    sprite_h = map.size[1] // rows
    if map.size[0] % cols or map.size[1] % rows:
        raise ValueError(
            f"{rows} rows and {cols} cols does not fit into image of size {map.size} cleanly"
        )
    new_img = np.empty((rows * cols, sprite_h * sprite_w), dtype=np.dtype(">u2"))

    count = 0
    for y in range(rows):
        for x in range(cols):
            new_img[count] = arr[
                y * sprite_h : (y + 1) * sprite_h, x * sprite_w : (x + 1) * sprite_w
            ].flatten()
            count += 1

    print(f"input image width: {map.size[0]}\ninput image height: {map.size[1]}\n")
    print(f"sprite_w: {sprite_w}\nsprite_h:{sprite_h}")
    if use_palette.title() == "True":
        if sprite_w % 2 != 0:
            raise ValueError("sprite width must be even if using palette")
        gen_palette(name, new_img)
    else:
        new_img.tofile("tools/converted/" + name + ".raw")


def main(args):
    # ik this isn't very safe, but only im going to be using this
    match len(args):
        case 2:
            convert_image(args[1])
        case 3:
            convert_image(args[1], args[2])
        case 4:
            convert_texture_map(args[1], int(args[2]), int(args[3]))
        case 5:
            convert_texture_map(args[1], int(args[2]), int(args[3]), args[4])
        case _:
            raise ValueError(f"only supports 1, 2, 3, 4 arguments, got {len(args) - 1}")


if __name__ == "__main__":
    main(sys.argv)
