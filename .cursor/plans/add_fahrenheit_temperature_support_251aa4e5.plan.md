---
name: Add Fahrenheit Temperature Support
overview: Add configurable temperature unit support (Celsius/Fahrenheit) by extending the configuration menu, storing the preference in .env, and updating the main weather display logic to show temperatures in the selected unit.
todos:
  - id: update-config
    content: Add temperature unit option to config.py setup menu and store preference in .env
    status: completed
  - id: update-main
    content: Update main.py to read TEMPERATURE_UNIT, extract both temp_c/temp_f from API, and conditionally set temperature values
    status: completed
  - id: update-translations
    content: Update all 12 locale JSON files to use {temp_unit} in temperature format strings
    status: completed
    dependencies:
      - update-main
---

# Add Configurable Fahrenheit Temperature Support

## Overview

Add the ability to configure temperature display units (Celsius or Fahrenheit) through the `weather-config` command, similar to how language preferences are configured.

## Changes Required

### 1. Update Configuration Module (`weather_cli/config.py`)

- Add a third menu option "Temperature Unit" to the setup choices
- Add a new menu section `menu-temp-unit` in translations with message, choices, and confirmation
- Store the preference as `TEMPERATURE_UNIT` in `.env` file (values: "celsius" or "fahrenheit")
- Set default to "celsius" if not configured

### 2. Update Main Weather Module (`weather_cli/main.py`)

- Read `TEMPERATURE_UNIT` from environment (default to "celsius")
- Extract both `temp_c`/`feelslike_c` and `temp_f`/`feelslike_f` from API response
- Add `temp_f` and `feelslike_f` to `weather_data` dictionary
- Conditionally set `temp` and `feels_like` values based on `TEMPERATURE_UNIT` preference
- Add `temp_unit` symbol ("°C" or "°F") to `weather_data` for use in format strings

### 3. Update Translation Files (all 12 locale files)

Update the `temperature` format string in each locale file to use `{temp_unit}` instead of hardcoded "°C":

- `locales/en.json` - Change from `{temp}°C` to `{temp}°{temp_unit}` (or use `{temp_unit}` as full string)
- Apply same change to: `ar.json`, `de.json`, `es.json`, `fr.json`, `it.json`, `ja.json`, `pl.json`, `pt.json`, `ro.json`, `ru.json`, `zh.json`

**Note**: The format string approach needs refinement - we'll use `{temp_unit}` as a placeholder that will be replaced with "C" or "F", and keep the "°" symbol in the format string, OR include the full "°C"/"°F" in the unit variable.

### 4. Implementation Details

- WeatherAPI provides both `temp_c`/`feelslike_c` and `temp_f`/`feelslike_f` in the response
- The temperature format string will be: `"🌡️ Temperature: {temp}°{temp_unit} (Feels like: {feels_like}°{temp_unit})"`
- Where `temp_unit` will be "C" or "F" based on configuration

## Files to Modify

1. `weather_cli/config.py` - Add temperature unit configuration option
2. `weather_cli/main.py` - Read unit preference and conditionally set temperature values
3. All 12 files in `locales/` directory - Update temperature format strings