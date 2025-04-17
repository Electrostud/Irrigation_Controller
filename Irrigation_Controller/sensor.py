from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
import requests

API_URL = "http://api.openweathermap.org/data/2.5/weather"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    openweathermap_api_key = config.get("api_key")
    latitude = config.get("latitude")
    longitude = config.get("longitude")

    sensors = [
        OpenWeatherMapSensor(openweathermap_api_key, latitude, longitude, "temperature"),
        OpenWeatherMapSensor(openweathermap_api_key, latitude, longitude, "humidity"),
        EvapotranspirationSensor(),
        IrrigationDurationSensor(),
    ]
    async_add_entities(sensors, True)

class OpenWeatherMapSensor(SensorEntity):
    def __init__(self, api_key, latitude, longitude, sensor_type):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.sensor_type = sensor_type
        self._state = None

    @property
    def name(self):
        return f"OpenWeatherMap {self.sensor_type.capitalize()}"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        if self.sensor_type == "temperature":
            return TEMP_CELSIUS
        elif self.sensor_type == "humidity":
            return PERCENTAGE

    async def async_update(self):
        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": self.api_key,
            "units": "metric",
        }
        response = requests.get(API_URL, params=params)
        data = response.json()
        if self.sensor_type == "temperature":
            self._state = data["main"]["temp"]
        elif self.sensor_type == "humidity":
            self._state = data["main"]["humidity"]

class EvapotranspirationSensor(SensorEntity):
    def __init__(self):
        self._state = None

    @property
    def name(self):
        return "Evapotranspiration (ET)"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "mm/day"

    async def async_update(self):
        temp = float(self.hass.states.get("sensor.openweathermap_temperature").state)
        humidity = float(self.hass.states.get("sensor.openweathermap_humidity").state)
        wind_speed = 1.5  # Assume a constant wind speed for simplicity
        solar_radiation = 20  # Assume a constant solar radiation for simplicity

        # Simplified ET formula
        self._state = round(0.0023 * (temp + 17.8) * (100 - humidity) * (solar_radiation + wind_speed), 2)

class IrrigationDurationSensor(SensorEntity):
    def __init__(self):
        self._state = None

    @property
    def name(self):
        return "Irrigation Duration"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "minutes"

    async def async_update(self):
        et = float(self.hass.states.get("sensor.evapotranspiration_et").state)
        area = 248  # Square feet
        crop_coefficient = 0.9
        flow_rate = 7.82  # GPM

        irrigation_gallons = area * et * crop_coefficient * 0.623
        self._state = round(irrigation_gallons / flow_rate)