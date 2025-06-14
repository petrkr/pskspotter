#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys
import json
import time
import argparse
from colorama import Fore, Style
from pyhamtools import LookupLib, Callinfo
from pyhamtools.locator import calculate_distance as qth_distance


args = None
cinfo = None


freqs = {
    "2m"  : { "FT8": 144_174_000 },
    "6m"  : { "FT8":  50_313_000 },
    "10m" : { "FT4":  28_180_000,
              "FT8":  28_074_000 },
    "15m" : { "FT4":  21_140_000,
              "FT8":  21_074_000 },
    "17m" : { "FT4":  18_104_000,
              "FT8":  18_100_000 },
    "20m" : { "FT4":  14_080_000,
              "FT8":  14_074_000 },
    "30m" : { "FT4":  10_140_000,
              "FT8":  10_136_000 },
    "40m" : { "FT4":   7_047_500,
              "FT8":   7_074_000 },
    "80m" : { "FT4":   3_575_000,
              "FT8":   3_573_000 }
    }


def get_base_freq(band, mode):
    if not band in freqs:
        return 0
    
    if not mode in freqs[band]:
        return 0
    
    return freqs[band][mode]


def get_freq_offset(freq, band, mode):
    base = get_base_freq(band, mode)
    return freq - base


def get_country_text(call):
    try:
        return cinfo.get_country_name(call)
    except:
        return "Unknown"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("pskr/filter/v2/+/+/{}/#".format(args.call.upper()))
    client.subscribe("pskr/filter/v2/+/+/+/{}/#".format(args.call.upper()))


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(payload['t']))
        scall = payload['sc'].replace(".", "/")

        if scall == args.call.replace(".", "/").upper():
            call = payload['rc'].replace(".", "/")
            loc = payload['rl']
            color = Fore.RED + "| TX"
        else:
            call = scall
            loc = payload['sl']
            color = Fore.GREEN + "| RX"

        country = get_country_text(call)

        print("{} | {:19} | {:10} | {:10} | {:3} dB | {:20} | {:4} Hz | {:5} km | {:5} | {:4} |{}".format(
            color,
            timestamp,
            call,
            loc,
            payload['rp'],
            country,
            get_freq_offset(payload['f'], payload['b'], payload['md']),
            int(qth_distance(payload['sl'], payload['rl'])),
            payload['md'],
            payload['b'],
            Style.RESET_ALL
            ))
            
    except Exception as e:
        print("Error processing message:", str(e))


def main():
    global args
    global cinfo

    parser = argparse.ArgumentParser()
    parser.add_argument("--call", required=True, help="Call sign")
    parser.add_argument("--cty-plist", required=False, default=None, help="Local filename of CTY Plist from country-code")
    args = parser.parse_args()

    print(args)

    print("Loading lookup directory")
    lookuplib = LookupLib(lookuptype="countryfile", filename=args.cty_plist)
    cinfo = Callinfo(lookuplib)

    if not cinfo.is_valid_callsign(args.call.replace(".", "/")):
        print("Error: Callsign {} is not valid!".format(args.call))
        sys.exit(1)


    print("Connecting to MQTT server")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    broker_address = "mqtt.pskreporter.info"
    broker_port = 1883
    
    client.connect(broker_address, broker_port, 60)
    
    client.loop_forever()

if __name__ == "__main__":
    main()
