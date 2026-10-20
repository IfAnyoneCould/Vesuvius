class Entity:
    _next_id = 0

    def __init(self):
        self.id = Entity._next_id
        Entity._next_id += 1
