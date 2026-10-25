from graphics.graphicsconfig import GraphicsConfig
from hardware.sd import SD


class Texture:
    def __init__(self, name, sd: SD, config: GraphicsConfig):
        if (
            name in ["bytes_per_pixel"]
        ):  # i could move these out of texture to remove edge cases, but i like it there
            raise ValueError(f"texture name {name} is illegal")
        data = config.textures.get(name)
        if data is None:
            raise ValueError(f"texture called {name} does not exist, check config")
        self.bpp = config.textures["bytes_per_pixel"]
        self.path = data["path"]
        self.w = data["sizex"]
        self.h = data["sizey"]
        self.row_size = self.w
        self.buf = None
        self.mv = None
        self.sd = sd

    def gen_buffer(self):
        self.buf = bytearray(self.row_size * self.bpp)
        self.mv = memoryview(self.buf)

    def load_row(self, row):
        if self.buf is None:
            raise ValueError("Texture.load_row() requires a generated buffer")
        bytes_per_row = self.row_size * self.bpp
        offset = row * bytes_per_row
        self.sd.use_sd()
        with open(self.path, "rb") as t:
            t.seek(offset)
            bytes_read = t.readinto(self.buf)
        if bytes_read != bytes_per_row:
            raise ValueError(f"loading row {row} from texture {self.path} failed")
        return self.mv

    def unload(self):
        self.buf = None
        self.mv = None
