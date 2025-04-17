# Irrigation Controller for Home Assistant

![Irrigation Controller](https://img.shields.io/github/v/release/Electrostud/Irrigation_Controller)
![HACS Compatible](https://img.shields.io/badge/HACS-Compatible-green)

A smart irrigation controller for Home Assistant that dynamically adjusts watering schedules based on real-time weather data from OpenWeatherMap and integrates with LinkTap devices.

## Features
- **Dynamic Watering**: Automatically calculates irrigation duration based on evapotranspiration (ET), temperature, humidity, and wind speed.
- **Real-Time Weather Data**: Fetches data from OpenWeatherMap to optimize watering.
- **LinkTap Integration**: Works seamlessly with LinkTap irrigation valves.
- **Customizable Settings**: Adjust area, crop coefficient, and flow rate to suit your needs.
- **Dashboard**: Monitor schedules, sensor data, and control irrigation directly from Home Assistant.

## Installation

### HACS (Recommended)
1. Open Home Assistant and go to **HACS** > **Integrations**.
2. Click the 3-dot menu in the top-right corner and select **Custom Repositories**.
3. Add this repository URL: `https://github.com/Electrostud/Irrigation_Controller`.
4. Select **Integration** as the category and click **Add**.
5. Search for "Irrigation Controller" in HACS and install it.

### Manual Installation
1. Clone this repository or download the ZIP file.
2. Copy the `custom_components/irrigation_controller` folder to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

## Configuration
1. Go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for "Irrigation Controller" and follow the setup instructions.
3. Provide your OpenWeatherMap API key, latitude, and longitude.
4. Configure your LinkTap account if using LinkTap.

## Lovelace Dashboard
Add the following to your Lovelace dashboard to monitor and control irrigation:

```yaml
views:
  - title: Irrigation Control
    path: irrigation_control
    badges: []
    cards:
      - type: entities
        entities:
          - entity: sensor.irrigation_duration
            name: Irrigation Duration
          - entity: sensor.evapotranspiration_et
            name: Evapotranspiration (ET)
          - entity: sensor.openweathermap_temperature
            name: Temperature
          - entity: sensor.openweathermap_humidity
            name: Humidity
          - entity: switch.linktap_valve
            name: Irrigation Valve
