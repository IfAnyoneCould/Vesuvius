import json


class GraphicsConfig:
    def __init__(self, data) -> None:
        self.textures = data["textures"]
        self.texturemaps = data["texturemaps"]
        self.animations = data["animations"]
        self.sprites = data["sprites"]


def load_config():
    with open("configs/graphics.json") as f:
        data = json.load(f)
    return GraphicsConfig(data)
