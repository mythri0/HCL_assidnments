
import requests
import pandas as pd
from pathlib import Path

# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "processed_weather.csv"

API_URL = "https://api.open-meteo.com/v1/forecast"

# City coordinates
CITIES = [
    {"city": "Chennai", "country": "India", "latitude": 13.0827, "longitude": 80.2707},
    {"city": "Bengaluru", "country": "India", "latitude": 12.9716, "longitude": 77.5946},
    {"city": "Mumbai", "country": "India", "latitude": 19.0760, "longitude": 72.8777},
    {"city": "London", "country": "UK", "latitude": 51.5072, "longitude": -0.1276},
    {"city": "New York", "country": "USA", "latitude": 40.7128, "longitude": -74.0060}
]


# ==================================================
# 1. API EXTRACTION FUNCTION
# Retrieve daily temperature in Fahrenheit
# ==================================================

def fetch_weather_data():

    print("\n========== WEATHER API EXTRACTION ==========")

    weather_records = []

    for location in CITIES:

        print(f"Fetching weather for {location['city']}...")

        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "temperature_2m_max",
            "temperature_unit": "fahrenheit",
            "forecast_days": 1,
            "timezone": "auto"
        }

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            raw_data = response.json()

            daily_data = raw_data.get("daily", {})

            dates = daily_data.get("time", [])
            temperatures = daily_data.get("temperature_2m_max", [])

            if not dates or not temperatures:
                print(f"No weather data available for {location['city']}.")
                continue

            weather_records.append({
                "city": location["city"],
                "country": location["country"],
                "date": dates[0],
                "temperature_fahrenheit": temperatures[0]
            })

            print(f"Successfully fetched {location['city']}.")

        except requests.RequestException as error:

            print(f"API request failed for {location['city']}: {error}")

        except (ValueError, KeyError, TypeError) as error:

            print(f"Invalid API response for {location['city']}: {error}")

    if not weather_records:
        raise RuntimeError("No weather records were retrieved.")

    print(f"\nTotal records retrieved: {len(weather_records)}")

    return pd.DataFrame(weather_records)


# ==================================================
# 2. DATA TRANSFORMATION FUNCTION
# Convert Fahrenheit to Celsius
# Filter temperatures above freezing
# ==================================================

def transform_weather_data(df):

    print("\n========== DATA TRANSFORMATION ==========")

    # Convert Fahrenheit to Celsius
    df["temperature_celsius"] = (
        (df["temperature_fahrenheit"] - 32) * 5 / 9
    ).round(2)

    print("Temperature conversion completed.")

    # Filter cities with temperature above 0 Celsius
    processed_df = df[
        df["temperature_celsius"] > 0
    ].copy()

    print("Applied above-freezing temperature filter.")

    print(f"Records before filtering: {len(df)}")
    print(f"Records after filtering: {len(processed_df)}")

    return processed_df


# ==================================================
# 3. SAVE PROCESSED DATA TO CSV
# ==================================================

def save_weather_data(df):

    print("\n========== CSV FILE OUTPUT ==========")

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("CSV file created successfully.")
    print(f"Output location: {OUTPUT_FILE}")


# ==================================================
# 4. MAIN WORKFLOW
# ==================================================

def main():

    print("\n========================================")
    print("       WEATHER DATA ENGINEERING PIPELINE")
    print("========================================")

    try:

        # Step 1: Fetch raw weather data
        raw_df = fetch_weather_data()

        # Step 2: Transform and filter data
        processed_df = transform_weather_data(raw_df)

        # Step 3: Save processed CSV
        save_weather_data(processed_df)

        print("\n========== FINAL PREVIEW ==========")

        if not processed_df.empty:
            print(processed_df.head().to_string(index=False))
        else:
            print("No cities had temperatures above freezing.")

        print("\n========================================")
        print(" WEATHER PIPELINE COMPLETED SUCCESSFULLY!")
        print("========================================")

    except Exception as error:

        print("\nWEATHER PIPELINE FAILED!")
        print(f"Error: {error}")
        raise


# ==================================================
# EXECUTE MAIN FUNCTION
# ==================================================

if __name__ == "__main__":
    main()
