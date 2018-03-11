""" The Things Network node setup """

import utime
import usocket
import ustruct
import ubinascii

import settings

from network import LoRa


def setup_abp():
    print('Setup ttn with abp auth')

    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # create an ABP authentication params
    dev_addr = ustruct.unpack(">l", ubinascii.unhexlify(
        settings.TTN_NODE_DEV_ADDR.replace(' ', '')))[0]
    nwk_swkey = ubinascii.unhexlify(
        settings.TTN_NODE_NWK_SWKEY.replace(' ', ''))
    app_swkey = ubinascii.unhexlify(
        settings.TTN_NODE_APP_SWKEY.replace(' ', ''))

    # remove all the non-default channels
    for i in range(3, 16):
        lora.remove_channel(i)

    # set the 3 default channels to the same frequency
    lora.add_channel(0, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)

    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    # create a LoRa socket
    s = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(usocket.SOL_LORA, usocket.SO_DR, settings.LORA_NODE_DR)

    # make the socket blocking
    s.setblocking(False)

    # return LoRa socket
    return s


def setup_otaa():
    print('Join ttn with ota auth')

    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # create an OTA authentication params
    app_eui = ubinascii.unhexlify(settings.TTN_NODE_APP_EUI.replace(' ', ''))
    app_key = ubinascii.unhexlify(settings.TTN_NODE_APP_KEY.replace(' ', ''))

    # remove all the non-default channels
    for i in range(3, 16):
        lora.remove_channel(i)

    # set the 3 default channels to the same frequency (must be before
    # sending the OTAA join request)
    lora.add_channel(0, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=settings.LORA_FREQUENCY, dr_min=0, dr_max=5)

    # join a network using OTAA
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key),
              timeout=0, dr=settings.LORA_NODE_DR)

    # wait until the module has joined the network
    while not lora.has_joined():
        utime.sleep(2.5)
        print('Not joined yet...')

    print('Network joined!')

    # create a LoRa socket
    s = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(usocket.SOL_LORA, usocket.SO_DR, settings.LORA_NODE_DR)

    # make the socket blocking
    s.setblocking(False)

    # return LoRa socket
    return s
