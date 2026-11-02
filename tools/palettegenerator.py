import numpy as np


class Palette:
    def __init__(self, path=None) -> None:
        self.colors = None
        if path is not None:
            # this only assumes that ONLY the filled array was written
            self.colors = np.fromfile(path, dtype=">u2")

    def from_data(self, colors):
        self.colors = np.unique(colors)
        if self.size() > 256:
            raise ValueError("too many colors in palette")

    def get_colors(self):
        return self.colors

    def get_color(self, index):
        if self.colors is None:
            raise ValueError("cannot get color from uninitialized palette")
        if 0 > index or index >= self.size():
            raise ValueError(
                f"index {index} out of bounds for palette size {self.size()}"
            )
        return self.colors[index]

    def size(self):
        if self.colors is None:
            return 0
        return len(self.colors)

    def write_palette(self, path):
        if self.colors is None:
            raise ValueError("cannot write uninitialized palette to file")
        self.colors.tofile(path)
