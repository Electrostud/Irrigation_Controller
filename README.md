# Irrigation Controller for Home Assistant

![Irrigation Controller](https://img.shields.io/github/v/release/Electrostud/Irrigation_Controller)
![HACS Compatible](https://img.shields.io/badge/HACS-Compatible-green)

A Home Assistant integration to dynamically control irrigation schedules based on real-time weather data from OpenWeatherMap and integrate with LinkTap irrigation devices.

## Features
- **Dynamic Watering**: Automatically calculates irrigation duration using evapotranspiration (ET).
- **Weather Integration**: Uses OpenWeatherMap for temperature, humidity, and wind data.
- **LinkTap Integration**: Works seamlessly with LinkTap irrigation devices.
- **Dashboard**: Monitor and control irrigation schedules with a custom Home Assistant dashboard.
- **Rain Skip Logic**: Skips watering when rain is expected.
- **Weekly Schedules**: Set and view weekly schedules for irrigation.

## Installation

### HACS (Recommended)
1. Open Home Assistant and go to **HACS** > **Integrations**.
2. Click the 3-dot menu in the top-right corner and select **Custom Repositories**.
3. Add this repository URL: `https://github.com/Electrostud/Irrigation_Controller`.
4. Select **Integration** as the category and click **Add**.
5. Search for "Irrigation Controller" in HACS, install it, and restart Home Assistant.

### Manual Installation
1. Clone this repository or download the ZIP file.
2. Copy the `custom_components/irrigation_controller` folder to your Home Assistant `config/custom_components` directory.
3. Restart Home Assistant.

## Configuration
1. Go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for "Irrigation Controller" and follow the setup instructions.
3. Provide your OpenWeatherMap API key, latitude, and longitude.
4. Configure your LinkTap account if using LinkTap.

## Lovelace Dashboard
To monitor and control irrigation, add the following to your Lovelace dashboard:

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
          - entity: sensor.openweathermap_wind_speed
            name: Wind Speed
          - entity: switch.linktap_valve
            name: Irrigation Valve


---

### **2. Create a Dashboard for Irrigation Schedules and Controls**
#### **Steps to Create the Dashboard**
1. Go to **Settings** > **Dashboards** in Home Assistant.
2. Add a new dashboard named `Irrigation Control`.
3. Use the provided Lovelace YAML code from the `README.md` file to configure the dashboard.

---

### **3. Enhance Scheduling Logic**
You can add the following features to improve the scheduling logic:
1. **Weekly Schedule**:
   - Create a `schedule.yaml` file to define irrigation times/days.
   - Use the `input_datetime` and `input_select` entities in Home Assistant to allow users to configure schedules via the UI.

2. **Rain Skip Logic**:
   - Use OpenWeatherMap’s precipitation forecast to skip watering if rain is expected in the next 24 hours.
   - Modify the existing automation to include a condition for rain.

#### **Example Automation with Rain Check**
```yaml
automation:
  - alias: Dynamic Hourly Irrigation Adjustment with Rain Check
    trigger:
      - platform: time_pattern
        hours: "/1"
    condition:
      - condition: numeric_state
        entity_id: sensor.evapotranspiration_et
        above: 0.1
      - condition: numeric_state
        entity_id: sensor.openweathermap_rain_forecast
        below: 1  # Skip irrigation if rain > 1mm is forecasted
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.linktap_valve
        data:
          duration: "{{ states('sensor.irrigation_duration') | int }}"
