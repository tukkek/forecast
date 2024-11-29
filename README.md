# Forecast
A naive weather forecast tray-cion. Useful for running in the background to keep track of the temperature.

# Installation

```
git clone --recurse-submodules https://github.com/tukkek/forecast
cd forecast/
python3 -m venv .venv/
.venv/bin/pip install -r requirements.txt
```

Before launching, enter into `location.ini` your local coordinates (which you can find at sites such as https://www.latlong.net).

If you'd like, create also a menu-launcher using your operating-system's tools that executes the command `/path/to/forecast/.venv/bin/python /path/to/forecast/forecast.py`.

## Credits
* Weather data provided by https://Open-Meteo.com 
