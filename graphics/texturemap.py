from graphics.texture import Texture
from graphics.graphicsconfig import GraphicsConfig
from hardware.sd import SD


class TextureMap(Texture):
    def __init__(self, name, sd: SD, config: GraphicsConfig):
        data = config.texturemaps.get(name)
        if data is None:
            raise ValueError(f"texturemap called {name} does not exist, check config")
        super().__init__(data["source_texture"], sd, config)
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.sprite_w = self.w // self.cols
        if self.w % self.cols != 0:
            raise ValueError("texturemap columns do not fit evenly into texture width")
        self.sprite_h = self.h // self.rows
        if self.h % self.rows != 0:
            raise ValueError("texturemap rows do not fit evenly into texture height")
        self.row_size = self.sprite_h * self.sprite_w

    def get_sprite_pixels(self, index):
        if index >= self.rows * self.cols or index < 0:
            raise ValueError(
                f"index {index} outside of bounds for texturemap with {self.rows} rows and {self.cols} columns"
            )
        return self.load_row(index)
