from PIL import Image
import numpy as np
import sys


def convert_565(arr):
    r = arr[:, :, 0].astype(np.uint16)
    g = arr[:, :, 1].astype(np.uint16)
    b = arr[:, :, 2].astype(np.uint16)

    return (((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)).astype(">u2")


def convert_image(in_path, out_path):
    img = Image.open(in_path)
    arr = np.asarray(img.convert("RGB"))
    rgb565 = convert_565(arr)
    print(f"input image width: {img.size[0]}\ninput image heigh: {img.size[1]}\n")
    print(
        f"saved image width: {rgb565.shape[1]}\nsaved image height: {rgb565.shape[0]}"
    )
    rgb565.tofile(out_path)


def convert_texture_map(in_path, out_path, rows, cols):
    map = Image.open(in_path)
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

    print(f"input image width: {map.size[0]}\ninput image heigh: {map.size[1]}\n")
    print(f"sprite_w: {sprite_w}\nsprite_h:{sprite_h}")

    new_img.tofile(out_path)


def main(args):
    # ik this isn't very safe, but only im going to be using this
    match len(args):
        case 3:
            convert_image(args[1], args[2])
        case 5:
            convert_texture_map(args[1], args[2], int(args[3]), int(args[4]))
        case _:
            raise ValueError(f"only supports 2 or 4 arguments, got {len(args) - 1}")


if __name__ == "__main__":
    main(sys.argv)
