import pandas as pd
import requests
import io

def getWaterHeaterData():
    response = requests.get("https://data.energystar.gov/resource/pbpq-swnu.json")
    waterHeaters = pd.read_json(io.StringIO(response.text))
    waterHeaters = waterHeaters[waterHeaters['fuel'] == "Electric"]
    waterHeaters = waterHeaters[waterHeaters['electric_usage_kwh_yr'].notna()]

    min, max, median = waterHeaters['electric_usage_kwh_yr'].min(), waterHeaters['electric_usage_kwh_yr'].max(), waterHeaters['electric_usage_kwh_yr'].median()
    return float(min / 365), float(median / 365)

def getFridgeData():
    response = requests.get("https://data.energystar.gov/resource/p5st-her9.json?$limit=4000")
    fridges = pd.read_json(io.StringIO(response.text))
    fridges = fridges[fridges["capacity_total_volume_ft3"] > 16]
    fridges = fridges[fridges["defrost_type"] == "Automatic"]
    fridges = fridges[fridges["type"] != "Freezerless and Single Door"]

    min, max, median = fridges['annual_energy_use_kwh_yr'].min(), fridges['annual_energy_use_kwh_yr'].max(), fridges['annual_energy_use_kwh_yr'].median()
    return float(min / 365), float(median / 365)


def getStoveData():
    response = requests.get("https://data.energystar.gov/resource/m6gi-ng33.json")
    stoves = pd.read_json(io.StringIO(response.text))
    
    min, max, median = stoves['annual_energy_consumption_kwh_yr'].min(), stoves['annual_energy_consumption_kwh_yr'].max(), stoves['annual_energy_consumption_kwh_yr'].median()
    return float(min / 365), float(median / 365)


def getDishwasherData():
    response = requests.get("https://data.energystar.gov/resource/q8py-6w3f.json")
    dishwashers = pd.read_json(io.StringIO(response.text))
    dishwashers = dishwashers[dishwashers["capacity_maximum_number_of_place_settings"] > 6]
    dishwashers = dishwashers[dishwashers["type"] == "Standard"]

    min, max, median = dishwashers['annual_energy_use_kwh_year'].min(), dishwashers['annual_energy_use_kwh_year'].max(), dishwashers['annual_energy_use_kwh_year'].median()
    return float(min / 365), float(median / 365)

    
def getDryerData():
    response = requests.get("https://data.energystar.gov/resource/t9u7-4d2j.json")
    dryers = pd.read_json(io.StringIO(response.text))
    dryers = dryers[dryers["type"] == "Electric"]
    dryers = dryers[dryers["drum_capacity_cu_ft"] >= 5.8]

    min, max, median = dryers['estimated_annual_energy_use_kwh_yr'].min(), dryers['estimated_annual_energy_use_kwh_yr'].max(), dryers['estimated_annual_energy_use_kwh_yr'].median()
    return float(min / 365), float(median / 365)

