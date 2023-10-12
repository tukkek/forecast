#!/usr/bin/python3
import os,time

MINUTE=60
HOUR=10*MINUTE

while True:
  os.system('clear')
  os.system('./forecast.py')
  time.sleep(HOUR)
