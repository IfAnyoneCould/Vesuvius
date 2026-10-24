from graphics.graphicsconfig import GraphicsConfig


class Texture:
    def __init__(self, name, config: GraphicsConfig):
        data = config.textures.get(name)
        if data is None:
            raise ValueError(f"texturemap called {name} does not exist, check config")
        self.bpp = data["bytes_per_pixel"]
        self.path = data["path"]
        self.w = data["sizex"]
        self.h = data["sizey"]
        self.buf = None
        self.mv = None

    def load_full(self):
        self.buf = bytearray(self.w * self.bpp * self.h)
        self.mv = memoryview(self.buf)
        with open(self.path, "rb") as t:
            t.readinto(self.buf)
        return self.mv

    def load_row(self, row):
        pass

    def unload(self):
        self.buf = None
        self.mv = None
