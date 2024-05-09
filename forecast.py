#!./venv/bin/python
import requests,datetime,math,configparser,simple_tray.tray,PyQt5.QtWidgets

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

class Tray(simple_tray.tray.Tray):
  def update(self):
    for r in self.rows:
      r.setVisible(False)
    results=get()
    nresults=len(results)
    for i in range(nresults):
      r=self.rows[i]
      r.setText(results[i])
      r.setVisible(True)
    self.say(results[1] if nresults>1 else results[0])
  
location=configparser.ConfigParser()
location.read('location.ini')
location=location['location']
t=Tray('Weacher forecast',"icon.webp",10*60)
t.rows=[PyQt5.QtWidgets.QAction() for i in range(4)]
for r in t.rows:
  t.menu.addAction(r)
t.start()
