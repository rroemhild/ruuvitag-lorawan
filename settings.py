""" RuuviTag to LoRaWAN settings file """

LORA_FREQUENCY = 868100000
LORA_NODE_DR = 5

# ABP auth
NODE_DEV_ADDR = ''  # Device Address
NODE_NWK_SWKEY = ''  # Network Session Key
NODE_APP_SWKEY = ''  # App Session Key

# OTAA auth
NODE_APP_EUI = ''
NODE_APP_KEY = ''

NODE_DEEPSLEEP = 300000  # milliseconds

# RuuviTags whitelist, other tags will be ignored
RUUVITAGS = (b'00:01:02:03:04:05', b'10:11:12:13:14:15')
