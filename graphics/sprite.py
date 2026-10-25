from graphics.texturemap import TextureMap
from graphics.graphicsconfig import GraphicsConfig
from hardware.lcd import LCD
from hardware.sd import SD


class Sprite:
    def __init__(self, name, sd: SD, config: GraphicsConfig):
        data = config.sprites.get(name)
        if data is None:
            raise ValueError(f"sprite {name} does not exist, check config")
        self.texturemap = TextureMap(data["source_map"], sd, config)
        self.frame = data["frame"]
        if self.frame < 0 or self.frame >= self.texturemap.rows * self.texturemap.cols:
            raise ValueError(
                f"frame {self.frame} out of bounds for texturemap, check config"
            )
        self.x_pos = 0
        self.y_pos = 0

    def load_sprite(self):
        return self.texturemap.get_sprite_pixels(self.frame)

    def set_position(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def get_position(self):
        return (self.x_pos, self.y_pos)

    def load(self):
        self.texturemap.gen_buffer()
        self.load_sprite()

    def unload(self):
        self.texturemap.unload()

    def draw(self, lcd: LCD):
        if self.texturemap.mv is None:
            raise ValueError("cannot draw uninitialized sprite")
        lcd.use_lcd()
        lcd.blit(
            self.texturemap.mv,
            self.x_pos,
            self.y_pos,
            self.texturemap.sprite_w,
            self.texturemap.sprite_h,
        )
