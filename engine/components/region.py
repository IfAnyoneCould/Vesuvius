from engine.core.config import Config
from engine.core.handler import HandlerTemplate


class RegionHandler(HandlerTemplate):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._regions_left = [i for i in range(config.regions.count)]
        self.handlers = {"standard": StandardRegionHandler(config)}

    def add(self, id, kind="standard"):
        if not self._regions_left:
            raise ValueError(
                "cannot add new region, no unused region left. check config"
            )
        handler = self.handlers[kind]
        index = self._regions_left.pop()
        name = self.config.regions.names[index]
        handler.add(id, index, name)
        self.ids[id] = handler

    def remove(self, id):
        index = self.get_region_index(id)
        self.ids[id].remove(id)
        self.ids.pop(id, None)
        self._regions_left.append(index)

    def get_name(self, id):
        return self.ids[id].get_name(id)

    def get_region_index(self, id):
        return self.ids[id].get_region_index(id)

    def get_adjacency(self, id1, id2):
        return self.ids[id1].get_adjacency(id1, id2)


class StandardRegionHandler:
    def __init__(self, config: Config) -> None:
        self._regions = {}
        self._region_num = {}
        self.config = config

    def add(self, id, index, name):
        self._regions[id] = name
        self._region_num[id] = index

    def remove(self, id):
        self._regions.pop(id, None)
        self._region_num.pop(id, None)

    def get_name(self, id):
        return self._regions[id]

    def get_region_index(self, id):
        return self._region_num[id]

    # this only works for 4 regions, but it's never going to handle more than that
    # if i really care later for some reason i can make it more expandable
    def get_adjacency(self, id1, id2):
        # 0 1 2 3 is 0  1
        #            2  3
        index1 = self._region_num[id1]
        index2 = self._region_num[id2]
        if index1 == index2:
            return "own"
        if index1 + index2 == 3:
            return "diagonal"
        return "adjacent"
