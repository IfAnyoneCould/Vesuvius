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

    def size(self):
        return (self.texturemap.sprite_w, self.texturemap.sprite_h)

    def load(self):
        self.texturemap.gen_buffer()
        self.load_sprite()

    def unload(self):
        self.texturemap.unload()

    def write_buffer(self, lcd: LCD):
        if self.texturemap.mv is None:
            raise ValueError("cannot draw uninitialized sprite")
        if self.texturemap.is_palette_texture() and self.texturemap.palette is not None:
            lcd.write_buffer(
                self.texturemap.framebuf,
                self.texturemap.sprite_w,
                self.texturemap.sprite_h,
                self.texturemap.palette,
            )
        else:
            raise ValueError("cannot write non palette sprite to a framebuffer")

    def write_screen(self, lcd: LCD):
        lcd.use_lcd()
        lcd.write_screen(
            self.x_pos, self.y_pos, self.texturemap.sprite_w, self.texturemap.sprite_h
        )

    def draw(self, lcd: LCD):
        if self.texturemap.mv is None:
            raise ValueError("cannot draw uninitialized sprite")
        lcd.use_lcd()
        if self.texturemap.is_palette_texture() and self.texturemap.palette is not None:
            lcd.blit_palette(
                self.texturemap.framebuf,
                self.x_pos,
                self.y_pos,
                self.texturemap.sprite_w,
                self.texturemap.sprite_h,
                self.texturemap.palette,
            )
        else:
            lcd.blit(
                self.texturemap.mv,
                self.x_pos,
                self.y_pos,
                self.texturemap.sprite_w,
                self.texturemap.sprite_h,
            )

    def get_width(self):
        return self.texturemap.sprite_w

    def get_height(self):
        return self.texturemap.sprite_h

    def is_loaded(self):
        return self.texturemap.is_loaded()
