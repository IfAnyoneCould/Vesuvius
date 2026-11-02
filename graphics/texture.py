from graphics.graphicsconfig import GraphicsConfig
from hardware.sd import SD
import framebuf


class Texture:
    def __init__(self, name, sd: SD, config: GraphicsConfig):
        if (
            name in ["normal_bpp", "packed_bpp"]
        ):  # i could move these out of texture to remove edge cases, but i like it there
            raise ValueError(f"texture name {name} is illegal")
        data = config.textures.get(name)
        if data is None:
            raise ValueError(f"texture called {name} does not exist, check config")
        self.bpp = config.textures["normal_bpp"]
        self.path = data["path"]
        self.w = data["sizex"]
        self.h = data["sizey"]
        self.row_size = self.w
        self.row_width = self.row_size
        self.row_height = 1
        self.buf = None
        self.mv = None
        self.framebuf = None
        self.palettebuf = None
        self.palette = None
        self.sd = sd
        self.palette_path = data.get("palette_path")
        if self.palette_path is not None:
            self.bpp = config.textures["packed_bpp"]
            self.sd.use_sd()
            with open(self.palette_path, "rb") as f:
                self.palettebuf = bytearray(f.read())

    def gen_buffer(self):
        self.buf = bytearray(self.row_size * self.bpp // 8)
        self.mv = memoryview(self.buf)
        if self.palettebuf is not None:
            self.framebuf = framebuf.FrameBuffer(
                self.buf, self.row_width, self.row_height, framebuf.GS4_HMSB
            )
            self.palette = framebuf.FrameBuffer(
                self.palettebuf, len(self.palettebuf) // 2, 1, framebuf.RGB565
            )

    def load_row(self, row):
        if self.buf is None:
            raise ValueError("Texture.load_row() requires a generated buffer")
        bytes_per_row = self.row_size * self.bpp // 8
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
        self.framebuf = None
        self.palette = None

    def is_palette_texture(self):
        return self.palettebuf is not None
