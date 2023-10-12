#!/usr/bin/python3
#docs https://open-meteo.com/en/docs
import requests,datetime,math,configparser

URL='https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true'
ROUND=datetime.timedelta(hours=+1)
HOUR=datetime.timedelta(hours=1)
NOW=datetime.datetime.now()
PARTS={
  6:'Morning',
  9:'Late morning',
  12:'Afternoon',
  15:'Late afternoon',
  18:'Evening',
  21:'Late evening',
  0:'Night',
  3:'Late night',
}

temperature=None

def enbolden(text):
  return f'\033[1m{text}\033[0m'
                             
def message(status,temperature,when,hours):
  p=PARTS[3*math.floor(when.hour/3)].lower()
  return f'Will {status} to {enbolden(temperature)} at {enbolden(p)}.'

def predict():
  now=NOW
  if now.minute>=30:
    now+=ROUND
  predictions=[]
  t=temperature
  when=now
  if now.hour>=6:
    for i in range(now.hour+1,16+1):
      when+=HOUR
      t+=1
      if temperature<30 and t>=30 and len(predictions)==0:
        hours=t-temperature
        predictions.append(message('raise','30°',when,hours))
  targets=[target for target in [30,20] if target<t]
  for t in range(t,20,-1):
    when+=HOUR
    target=targets[0]
    t-=1
    if t<=target or when.hour==6:
      hours=when-now
      hours=hours.seconds/(60*60)
      predictions.append(message('drop',f'{t}°',when,hours))
      targets.pop(0)
      if len(targets)==0:
        break
  return predictions

location=configparser.ConfigParser()
location.read('location.ini')
location=location['location']
json=requests.get(URL.format(location['latitude'],location['longitude'])).json()
temperature=round(float(json['current_weather']['temperature']))
current=f'{temperature}°'
output=[f'Current temperature is {enbolden(current)}.']+predict()
print('\n'.join(output))
