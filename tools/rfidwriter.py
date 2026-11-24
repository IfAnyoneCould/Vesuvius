from hardware.scanners import Scanners
from hardware.spi import SPIHandler
import hardware.ioconfig as ioconfig
from engine.core.rfid import RFIDProcessor
import engine.core.config as engineconfig


def main():

    config = ioconfig.load_config()
    spi = SPIHandler(config)
    scanners = Scanners(spi, config)
    econfig = engineconfig.load_config()

    while True:
        id = input("id: ")
        piece = input("piece: ")
        region = input("region: ")
        processor = RFIDProcessor(scanners, econfig)
        tag = processor.encode_rfid(int(id), piece, region)
        for s in range(config.scanners.count):
            if scanners.write_index(s, tag):  # just going to write to all of them
                print("success")
                result = True  # dumb way to set it but im being really lazy rn
                break
        else:
            print("failed")


if __name__ == "__main__":
    main()
