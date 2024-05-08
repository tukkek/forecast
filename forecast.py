#docs https://open-meteo.com/en/docs
import requests,datetime,math,configparser

URL='https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current_weather=true'
ROUND=datetime.timedelta(hours=+1)
HOUR=datetime.timedelta(hours=1)
PARTS={
  6:'Morning',
  12:'Afternoon',
  18:'Evening',
  0:'Night',
}

def message(status,temperature,when,hours):
  p=PARTS[6*math.floor(when.hour/6)].lower()
  return f'Will {status} to {temperature} at {p}.'

def predict(temperature):
  now=datetime.datetime.now()
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
        predictions.append(message('rise','30°',when,hours))
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

def get():
  json=requests.get(URL.format(location['latitude'],location['longitude'])).json()
  temperature=round(float(json['current_weather']['temperature']))
  return [f'Current temperature is {temperature}°.']+predict(temperature)
  
location=configparser.ConfigParser()
location.read('location.ini')
location=location['location']
