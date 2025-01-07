import pandas as pd 
import pvlib


def calculate_solar_position(serial_locations, INPUT_PATH, OUTPUT_PATH):

    df = pd.read_csv(INPUT_PATH)
    
    df['date'] = pd.to_datetime(df['date'])
 
    azimuths = []
    zeniths = []
    altitudes = []

    for serial, coords in serial_locations.items():
        
        serial_data = df[df['serial_number'] == serial]
        
        latitude, longitude = coords['latitude'], coords['longitude']

        
        solar_position = pvlib.solarposition.get_solarposition(
            serial_data['date'],
            latitude=latitude,
            longitude=longitude
        )

        azimuths.extend(solar_position['azimuth'].values)
        zeniths.extend(solar_position['zenith'].values)
        altitudes.extend(90 - solar_position['zenith'].values)
        

    if len(azimuths) == len(df) and len(zeniths) == len(df) and len(altitudes) == len(df):
        df['solar_azimuth'] = azimuths
        df['solar_zenith'] = zeniths
        df['solar_altitude'] = altitudes 
    else:
        raise ValueError("Die Anzahl der berechneten Werte stimmt nicht mit den Daten überein!")

    
    df.to_csv(OUTPUT_PATH, index=False)

df = pd.read_csv('data/preprocessed/alldata_merged.csv')
serial_locations = df[['serial_number', 'latitude', 'longitude']].drop_duplicates()
serial_locations = serial_locations.set_index('serial_number')[['latitude', 'longitude']].to_dict('index')

INPUT_PATH = 'data/preprocessed/alldata_merged.csv'
OUTPUT_PATH = 'data/feature_extraction/anglecalc.csv'

calculate_solar_position(serial_locations, INPUT_PATH, OUTPUT_PATH)




