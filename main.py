import pandas as pd 
import numpy as np 
import os

OUTPUT_PATH = '../../data/preprocessed/alldata_merged.csv'


def run():
    solar = load_solar_data()
    meta = load_meta_data()
    weather = load_weather_data()
    full_data = merge_files(solar_data=solar, meta_data=meta, weather_data=weather, output_path=OUTPUT_PATH)

def load_solar_data():
    file_path = "../../data/raw/solar/PV Plants Datasets.xlsx"
    xlsx = pd.ExcelFile(file_path)
    data = pd.DataFrame()
    for name in xlsx.sheet_names: 
        df_add = pd.read_excel(xlsx, name)
        df_add['serial_number'] = name
        df_add.drop(columns=['CO2 Avoided (tons)'], inplace=True)
        data = pd.concat([data, df_add], ignore_index=True, axis=0)

    data.rename(columns={'Date':'date', 'Produced Energy (kWh)':'produced_energy_kwh', 'Specific Energy (kWh/kWp)':'specific_energy_kwh/kwp'}, inplace=True)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%y %H:%M', errors='coerce')
    data['serial_number'] = data['serial_number'].astype(str)
    return data

def load_meta_data():
    file_path = "../../data/raw/solar/PV Plants Metadata.xlsx"
    xlsx = pd.ExcelFile(file_path)
    meta_data = pd.read_excel(xlsx, xlsx.sheet_names[0])
    meta_data.columns = meta_data.iloc[0]
    meta_data.drop(columns=[meta_data.columns[0], 'From date', 'To date'], inplace=True)
    meta_data.drop(0, inplace=True)
    meta_data.rename(columns={'PV Serial Number' : 'serial_number', 'Location' : 'location', 'Latitude' : 'latitude', 'Longitude': 'longitude', 'Installed Power (kWp)':'installed_power_kwp', 'Connection Power (kWn)':'connection_power_kwh'}, inplace=True)
    meta_data['serial_number'] = meta_data['serial_number'].astype(str)
    meta_data['location']= meta_data['location'].str.lower()
    return meta_data

def load_weather_data():
    path = "../../data/raw/weather_files"
    files = ['Lisbon_weather.csv', 'Braga_weather.csv', 'Tavira_weather.csv', 'Faro_weather.csv', 'Loule_weather.csv', 'Setubal_weather.csv']
    cities = ['lisbon', 'braga', 'tavira', 'faro', 'loule', 'setubal']

    weather_data = pd.DataFrame()
    for i in range(0,len(cities)):
        df_add = pd.read_csv(f"{path}/{files[i]}")
        df_add['location'] = cities[i]
        weather_data = pd.concat([weather_data, df_add], ignore_index=True)
        print(weather_data.shape)
    weather_data.rename(columns={'temperature_2m (°C)':'temperature_2m_celsius', 'relative_humidity_2m (%)':'relative_humidity_2m_%',
       'dew_point_2m (°C)':'dew_point_2m_celsius', 'apparent_temperature (°C)':'apparent_temperature_celsius', 'cloud_cover (%)':'cloud_cover_%',
       'wind_speed_10m (km/h)':'wind_speed_10m_km/h', 'wind_direction_10m (°)':'wind_direction_10m_degree', 'time':'date',
       'shortwave_radiation (W/m²)':'shortwave_radiation_w/m2'}, inplace=True)
    
    weather_data['date'] = pd.to_datetime(weather_data['date'], format='%m/%d/%y %I:%M %p', errors='coerce')
    return weather_data

def merge_files(solar_data, meta_data, weather_data, output_path):
    print(meta_data.head())
    print(f"shapes of data: solar {solar_data.shape}, meta {meta_data.shape}, weather {weather_data.shape}")
    full_data = pd.merge(left=solar_data, right=meta_data, on='serial_number',how='left')
    print(f"Shape of full data {full_data.shape}")
    print(f"columns {full_data.columns}, weather {weather_data.columns}")
    print(full_data.head())
    full_data = pd.merge(left=full_data, right=weather_data, on=['location', 'date'],how='left')
    print(f"Shape of full data {full_data.shape}")
    print(full_data.head())


    full_data.to_csv(output_path, index=False)

    return full_data

if __name__ == "__main__": 
    run()
        