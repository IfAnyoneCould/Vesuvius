from graphics.texturemap import TextureMap
from graphics.graphicsconfig import GraphicsConfig
from hardware.lcd import LCD
from hardware.sd import SD


class Animation:
    def __init__(self, name, sd: SD, config: GraphicsConfig) -> None:
        data = config.animations.get(name)
        if data is None:
            raise ValueError(f"animation {name} does not exist, check config")
        self.texturemap = TextureMap(data["source_map"], sd, config)
        self.start_frame = data["start_frame"]
        self.end_frame = data["end_frame"]
        if self.start_frame >= self.end_frame:
            raise ValueError(
                "animation start frame cannot be greater or equal to end frame, check config"
            )
        if (
            self.start_frame < 0
            or self.end_frame >= self.texturemap.rows * self.texturemap.cols
        ):
            raise ValueError("start or end frame out of bounds, check config")
        self.time_step_ms = data["time_step_ms"]
        self.current_frame = self.start_frame
        self.x_pos = 0
        self.y_pos = 0
        self.last_frame_change_ms = None
        self.frame_data = None

    def load_frame(self, frame):
        if (
            self.start_frame <= frame <= self.end_frame
        ):  # python letting you do this is so cursed
            return self.texturemap.load_row(frame)
        raise ValueError(f"frame {frame} outside animation bounds")

    def advance_frame(self):
        self.current_frame += 1
        if self.current_frame > self.end_frame:
            self.current_frame = self.start_frame

    def set_frame(self, frame):
        if (
            self.start_frame <= frame <= self.end_frame
        ):  # ik this is duplicated code, but its small so who cares
            self.current_frame = frame
            self.last_frame_change_ms = None
            self.frame_data = self.load_frame(self.current_frame)
            return
        raise ValueError(f"frame {frame} outside animation bounds")

    def set_position(
        self, x: int, y: int
    ):  # put the ints there because it makes the return type on get_position pretty
        self.x_pos = x
        self.y_pos = y

    def get_position(self):
        return (self.x_pos, self.y_pos)

    def play(
        self, time_ms
    ):  # you run play every frame you want it to run and give it the current time
        if self.last_frame_change_ms is None:
            self.last_frame_change_ms = time_ms
            if self.frame_data is None:
                self.frame_data = self.load_frame(self.current_frame)
        delta_time = time_ms - self.last_frame_change_ms
        if delta_time >= self.time_step_ms:
            self.advance_frame()
            if delta_time >= 2 * self.time_step_ms:
                self.last_frame_change_ms = time_ms
            else:
                self.last_frame_change_ms += self.time_step_ms
            self.frame_data = self.load_frame(self.current_frame)
        return self.frame_data

    def unload(self):
        self.frame_data = None
        self.texturemap.unload()
        self.last_frame_change_ms = None

    def gen_buffer(self):
        self.texturemap.gen_buffer()

    def draw(self, lcd: LCD):
        if self.frame_data is None:
            raise ValueError("cannot draw uninitialized animation")
        lcd.use_lcd()
        lcd.blit(
            self.frame_data,
            self.x_pos,
            self.y_pos,
            self.texturemap.sprite_w,
            self.texturemap.sprite_h,
        )
