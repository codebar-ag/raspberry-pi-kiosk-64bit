

from utils import rasputils

class Device:
    """QUICK DEVICE CLASS
    To handle states 
    """

    def __init__(self):
        self.ready = True
        self.online = True

    @staticmethod
    def mac_address():
        """Return Mac address of the device"""
        return rasputils.get_mac()

    @staticmethod
    def temperature():
        """Return temperature of the device"""
        return rasputils.get_temperature()


