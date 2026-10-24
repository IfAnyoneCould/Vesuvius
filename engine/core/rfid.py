from hardware.scanners import Scanners
from engine.core.config import Config


class RFIDProcessor:
    def __init__(self, scanners: Scanners, config: Config) -> None:
        self.scanners = scanners
        self.config = config

    # NOTE this code is NOT safe, but i doubt that it will ever overflow
    def encode_rfid(self, id, piece, region):
        tag = id.to_bytes(self.config.rfid.id_bytes, self.config.rfid.id_encoding)
        tag += piece.encode().ljust(self.config.rfid.piece_bytes, b"\x00")
        tag += region.encode().ljust(self.config.rfid.region_bytes, b"\x00")
        return tag

    def decode_rfid(self, rfid):
        id_bytes = self.config.rfid.id_bytes
        piece_bytes = self.config.rfid.piece_bytes
        region_bytes = self.config.rfid.region_bytes
        id = int.from_bytes(rfid[0:id_bytes], self.config.rfid.id_encoding)
        piece = rfid[id_bytes : id_bytes + piece_bytes].rstrip(b"\x00").decode()
        region = (
            rfid[id_bytes + piece_bytes : id_bytes + piece_bytes + region_bytes]
            .rstrip(b"\x00")
            .decode()
        )
        return (id, piece, region)

    def poll_all(self):
        data = self.scanners.poll_all()
        results = {}
        for i, rfid in data.items():
            results[i] = self.decode_rfid(rfid)
        return results

    def poll_position(self, position):
        index = self.scanners.get_index_from_position(position)
        return self.poll_index(index)

    def poll_index(self, index):
        rfid = self.scanners.poll_index(index)
        return self.decode_rfid(rfid) if rfid is not None else (None, None, None)

    def verify_data(self, piece, region, rfid):
        _, r_piece, r_region = self.decode_rfid(rfid)
        return r_piece == piece and r_region == region

    def write_index(self, index, rfid):
        _, piece, region = self.poll_index(index)
        if not self.verify_data(piece, region, rfid):
            return False
        return self.scanners.write_index(index, rfid)
