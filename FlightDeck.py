#!/usr/bin/env python
#
# Flight Computer Suite for High-Altitude Ballooning using GrovePi sensors

import time
import datetime
import grovepi
from grovepi import *
from subprocess import call
from Adafruit_BMP085 import BMP085

buzzer_port    = 2
temphum_port   = 4
vibration_port = 8
hightemp_port  = 2
barometer      = BMP085(0x77)

last_photo_time    = 0
time_lapse_seconds = 10

buzzer_meters = 500

def soundBuzzer():
  altitude = barometer.readAltitude()
  if altitude < buzzer_meters:
    grovepi.pinMode(buzzer_port,"OUTPUT")
    grovepi.digitalWrite(buzzer_port,1)
    time.sleep(1)
    grovepi.digitalWrite(buzzer_port,0)
    time.sleep(1)

def logInternalTemp():
  [ ctemp,hum ] = dht(temphum_port,0)
  temp = (ctemp * 1.8) + 32
  line = getTimestamp() + "," + str(temp) + "," + "F\n"
  log  = open("/root/logs/internal_temp.log", "a")
  log.write(line)
  time.sleep(1)

def logInternalHumidity():
  [ temp,hum ] = dht(temphum_port,0)
  line = getTimestamp() + "," + str(hum) + "," + "%\n"
  log  = open("/root/logs/internal_humidity.log", "a")
  log.write(line)
  time.sleep(1)

def logVibrations():
  vibro = grovepi.digitalRead(vibration_port)
  line = getTimestamp() + "," + str(vibro) + "," + "degree\n"
  log  = open("/root/logs/vibration.log", "a")
  log.write(line)
  time.sleep(1)

def logBarometricPressure():
  pressure = barometer.readPressure()
  line = getTimestamp() + "," + str(pressure) + "," + "Pa\n"
  log  = open("/root/logs/barometric_pressure.log", "a")
  log.write(line)
  time.sleep(1)

def logBarometricAltitude():
  altitude = barometer.readAltitude()
  line = getTimestamp() + "," + str(altitude) + "," + "m\n"
  log  = open("/root/logs/barometric_altitude.log", "a")
  log.write(line)
  time.sleep(1)

def logBarometricTemp():
  ctemp = barometer.readTemperature()
  temp  = (ctemp * 1.8) + 32
  line  = getTimestamp() + "," + str(temp) + "," + "F\n"
  log   = open("/root/logs/barometric_temp.log", "a")
  log.write(line)
  time.sleep(1)

def logExternalTemp():
  ext_temp = grovepi.analogRead(hightemp_port)
  line = getTimestamp() + "," + str(ext_temp) + "," + "F\n"
  log  = open("/root/logs/external_temp.log", "a")
  log.write(line)
  time.sleep(1)

def logPhoto():
  global last_photo_time
  secs  = time.time()
  since = (secs - last_photo_time)
  if since >= time_lapse_seconds:
    stamp    = getTimestamp()
    filename = "/root/images/" + stamp + ".jpg"
    cmd      = "raspistill -o " + filename
    call(cmd, shell=True)
    last_photo_time = secs

def getTimestamp():
  secs  = time.time()
  stamp = datetime.datetime.fromtimestamp(secs).strftime('%Y-%m-%d_%H:%M:%S')
  return stamp

while True:
  try:
    soundBuzzer()
    logInternalTemp()
    logInternalHumidity()
    logVibrations()
    logBarometricPressure()
    logBarometricAltitude()
    logBarometricTemp()
    logExternalTemp()
    logPhoto()
  except KeyboardInterrupt:
    grovepi.digitalWrite(buzzer_port,0)
    break
  except IOError:
    print "Error"
