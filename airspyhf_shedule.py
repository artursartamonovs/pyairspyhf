#!/usr/bin/python3

import os
from airspyhf import *
from ctypes import *
import time
import sys
import argparse
import configparser
import re

class Station:
    name = "NoName"
    frequency = 4000000
    time = 0
    duration = 300 #in seconds
    day = []
    month = []
    def __init__(self):
        pass

    def readConfig(self,config):
        if "name" in config:
            self.name = config["name"]

        if "frequency" in config:
            self.frequency = int(config["frequency"])

        if "time" in config:
            m = re.match(r"(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2})",config["time"]).groupdict()
            m_hour = int(m["hour"])
            m_minute = int(m["minute"])
            #what format should be time
            self.time = m_hour*3600+m_minute*60

        if "duration" in config:
            s_duration = str(config["duration"])
            # Supported
            # 6m
            # 1h30m
            # 1m30s
            # 0m1s
            # 0h5m10s
            m = re.match(r"((?P<hour>[0-9]{1,2})h)?((?P<minute>[0-9]{1,2})m)?((?P<second>[0-9]{1,2})s)?",s_duration).groupdict()
            print(m)
            time_in_sec = 0
            if m["hour"]:
                time_in_sec += int(m["hour"])*3600
            if m["minute"]:
                time_in_sec += int(m["minute"])*60
            if m["second"]:
                time_in_sec += int(m["second"])
            self.duration = time_in_sec

        if "day" in config:
            self.day = config["day"]

        if "month" in config:
            self.month = config["month"]


class StationCollection:
    stations = []
    def __init__(self):
        pass

    def addStation(self,station:Station):
        self.stations.append(station)

    def listall(self):
        print("List of stations")
        for s in self.stations:
            print(s)

    def listToday(self):
        print("Today will broadcast")

class RadioConfig:
    samplerate = 192000
    def __init__(self):
        pass

    def readConfig(self, config):
        if "samplerate" in config:
            self.samplerate = int(config["samplerate"])

parser = argparse.ArgumentParser()
parser.add_argument("-c","--configfile")
parser.add_argument("-d","--debug",help="Output extra logs to see whats happening")
args = parser.parse_args()

debug = False
if args.debug:
    debug = True
config = configparser.ConfigParser()
if args.configfile:
    config.read(args.configfile)
else:
    config.read("number.ini")

print(config.sections())
radio_config = RadioConfig()
station_config = StationCollection()

for section in config.sections():
    #print(section)
    if section == "radio":
        radio_config.readConfig(config[section])
    elif section[0:7] == "station":
        station = Station()
        station.readConfig(config[section])
        station_config.addStation(station)

#print list of all stations
station_config.listall()

#print list of todays stations to record
station_config.listToday()
