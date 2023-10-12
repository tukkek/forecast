#!/usr/bin/python3
import os,time

MINUTE=60

while True:
  os.system('clear')
  os.system('./forecast.py')
  time.sleep(10*MINUTE)
