#!/usr/bin/env python3

import signal
import requests 
import logging
import sys
import unicornhat as unicorn
from math import floor
from time import sleep

logging.basicConfig(
        filename='log/blinky.log', 
        filemode='a', 
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
)

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

light_order = ['wind', 'solar', 'hydro', 'gas', 'coal', 'nuclear', 'imports', 'biomass']

class ServiceLoop:
    stopping = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGHUP, self.stop)

    def stop(self, *args):
        unicorn.clear()
        unicorn.show()
        self.stopping = True
        sleep(1)
        sys.exit()


class Light:
    def __init__(self, colour):
        self.colour = colour

class EnergyType:

    COLS = {
        'nuclear': [255,110,255],
        'biomass': [110,255,255],
        'wind': [0,255,0],
        'solar': [255,173,45],
        'imports': [255,255,255],
        'gas': [0,0,255],
        'coal': [255,0,0],
        'hydro': [47,141,255],
        'other': [0,0,0],

    }

    LOWCOLS = {
        'nuclear': [95,60,95],
        'biomass': [60,95,95],
        'wind': [0,95,60],
        'solar': [150,105,30],
        'imports': [110,110,110],
        'gas': [0,0,110],
        'coal': [110,0,0],
        'hydro': [17,111,200],
        'other': [0,0,0],
    }

    def __init__(self, name, percent):
        self.name = name
        self.percent = floor(percent)

    def getColour(self):
        return self.COLS[self.name]

    def getLights(self):
        lights = []

        if self.percent > 0 and self.percent <= 12:
            lights.append(Light(self.LOWCOLS[self.name]))
        if self.percent > 12 and self.percent <= 25:
            lights.append(Light(self.COLS[self.name]))
        if self.percent > 25 and self.percent <= 37:
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.LOWCOLS[self.name]))
        if self.percent > 37 and self.percent <= 50:
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
        if self.percent > 50 and self.percent <= 62:
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.LOWCOLS[self.name]))
        if self.percent > 62 and self.percent <= 75:
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
        if self.percent > 75 and self.percent <= 87:
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.LOWCOLS[self.name]))
        if self.percent > 87 and self.percent <= 100:
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))
            lights.append(Light(self.COLS[self.name]))

        return lights


url = "https://api.carbonintensity.org.uk/regional/regionid/" 
region_code = "12"
refresh_time = 1800
headers = {'Accept': 'application/json', 'User-Agent': 'curl/7.53'}

if __name__ == '__main__':
    service_loop = ServiceLoop()

    while not service_loop.stopping:
        logging.info("Updating intensity data")
        get_request = url + region_code

        try:
            response = requests.get(url + region_code, headers = headers)
        except:
            logging.error("Failed to get light data - trying again in a minute")
            sleep(60)
            response = requests.get(url + region_code, headers = headers)

        json = response.json()

        generationmix = json['data'][0]['data'][0]['generationmix']

        energy_types = {}

        for mix in generationmix:
            energy_types[mix['fuel']] = EnergyType(mix['fuel'], mix['perc'])

        x = 0
        for fuel in light_order:
            energy_type = energy_types[fuel]
            logging.info('{:s} => {:d}%'.format(energy_type.name, energy_type.percent))
            lights = energy_type.getLights()
            if len(lights) > 0:
                for y in range(len(lights)): 
                    row = 3 - y
                    unicorn.set_pixel(x, row, lights[y].colour[0], lights[y].colour[1], lights[y].colour[2])

            x = x + 1

        unicorn.show()

        sleep(refresh_time)

