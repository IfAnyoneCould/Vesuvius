from engine.core.rfid import RFIDProcessor
from hardware.scanners import Scanners


def get_ids_from_scanners(scanners: Scanners, processor: RFIDProcessor):
    rfids = scanners.poll_all()
    results = {}
    for k, v in rfids.items():
        results[k] = processor.decode_rfid(v)[0]
    return results


def get_center_id(scanners: Scanners, processor: RFIDProcessor):
    rfid = scanners.poll_position("center")
    if rfid is not None:
        return processor.decode_rfid(rfid)[0]
    return None


def get_unit_ids(scanners: Scanners, processor: RFIDProcessor):
    results = {"left": [], "right": []}
    rfids = scanners.poll_all()
    for k, v in rfids.items():
        # these are hardcoded, but idk a cleaner way to to this rn
        if k in ["left_one", "left_two", "left_three"]:
            results["left"].append(processor.decode_rfid(v)[0])
        elif k in ["right_one", "right_two", "right_three"]:
            results["right"].append(processor.decode_rfid(v)[0])
    return results
