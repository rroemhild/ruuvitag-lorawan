import utime
import usocket
import ubinascii

from network import LoRa


class LoRaWANNode:

    def __init__(self, app_eui, app_key, frequency=868100000, dr=5):
        '''setup LoRaWAN for the European 868 MHz region with OTAA'''
        self.dr = dr
        self.frequency = frequency
        self.app_eui = ubinascii.unhexlify(app_eui)
        self.app_key = ubinascii.unhexlify(app_key)

        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        self.socket = None

        self.setup()

    @property
    def has_joined(self):
        return self.lora.has_joined()

    def default_channels(self):
        ''''
        Remove all non-default channels and set the 3 default channels to the
        same frequency (must be before ending the OTAA join request)
        '''
        for i in range(3, 16):
            self.lora.remove_channel(i)

        self.lora.add_channel(0, frequency=self.frequency,
                              dr_min=0, dr_max=self.dr)
        self.lora.add_channel(1, frequency=self.frequency,
                              dr_min=0, dr_max=self.dr)
        self.lora.add_channel(2, frequency=self.frequency,
                              dr_min=0, dr_max=self.dr)

    def setup(self):
        '''Try to restore from nvram or join the network with otaa'''
        self.default_channels()
        self.lora.nvram_restore()

        if not self.has_joined:
            self.join()
        else:
            self.open_socket()

    def join(self, timeout=10):
        try:
            timeout = timeout * 1000
            self.lora.join(activation=LoRa.OTAA,
                           auth=(self.app_eui, self.app_key),
                           timeout=timeout, dr=self.dr)

            if self.has_joined:
                self.lora.nvram_save()
                self.open_socket()
        except TimeoutError:
            pass

    def open_socket(self, timeout=6):
        self.socket = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)
        self.socket.setsockopt(usocket.SOL_LORA, usocket.SO_DR,
                               self.dr)
        self.socket.settimeout(timeout)

    def reset(self):
        self.socket.close()
        self.lora.nvram_erase()
        self.join()

    def send(self, data):
        '''Send out data as bytes'''
        if self.has_joined:
            if isinstance(data, (float, str, int)):
                data = bytes([data])
            self.socket.send(data)
            utime.sleep(2)
            self.lora.nvram_save()
