import json
import os

def writeDefaultJson():
    EnergyJsonDefault = {
        "Inputs": {
            "Irradiance": {
                "GHI Watts/m^2 Average": 128
            },
            "HVAC": {
                "Roof R Value": 30,
                "Floor Area": 2000,
                "Wall R Value": 15,
                "Wall Height": 10,
                "Floor R Value": 15,
                "Window R Value": 4,
                "Window Area Percent": 15,
                "Ground Temperature F": 60,
                "Outdoor Air Temperature F": 58,
                "Indoor Air Temperature F": 72,
                "HVAC Efficiency Percent": 100,
                "Air Changes Per Hour": 3,
                "Ventilation Recovery Percent": 25,
            },
            "Hot Water": {
                "Water Use Per Day Liters": 230,
                "Water Heater Temperature C": 55,
                "Water Inlet Temperature C": 10,
                "Water Heater Efficiency Percent": 95,
                "Water Heat Recovery Efficiency Percent": 0
            },
            "Lighting": {
                "Lumens Per Square Foot": 50,
                "Lumens Per Watt": 75,
                "Lights On Hours Per Day": 2,
            },
            "Cooking": {
                "Cooking Appliance Wattage": 2500,
                "Cooking Hours Per Day": 1.5,
            },
            "Clothes Drying": {
                "Clothes Drying Wattage": 2500,
                "Clothes Drying Hours Per Day": 0.5,
            },
            "Dishwasher": {
                "Dishwasher Wattage": 2500,
                "Dishwasher Hours Per Day": 0.5,
            },
            "Refrigerator": {
                "Refrigerator kWh Per Year": 400,
            },         
            "Electric Car": {
                "Electric Car kWh Per Day": 12.0,
            },         
            "Misc Plug Load": {
                "Misc Plug Load kWh Per Day": 5.0,
            }
        },
        "Outputs": {
            "Total": {
                "Total kWh Per Day": 0.0,
            },
            "HVAC": {
                "Total HVAC kWh Per Day": 0.0,
                "Ventilation kWh Per Day": 0.0,
                "Roof kWh Per Day": 0.0,
                "Wall kWh Per Day": 0.0,
                "Window kWh Per Day": 0.0,
                "Floor kWh Per Day": 0.0,
                "Wall Area sqft": 0.0,
                "Window Area sqft": 0.0
            },
            "Hot Water": {
                "Total Hot Water kWh Per Day": 0.0,
            },
            "Lighting": {
                "Lighting kWh Per Day": 0.0,
            },
            "Cooking": {
                "Cooking kWh Per Day": 0.0,
            },
            "Clothes Drying": {
                "Clothes Drying kWh Per Day": 0.0,
            },        
            "Dishwasher": {
                "Dishwasher kWh Per Day": 0.0,
            },
            "Refrigerator": {
                "Refrigerator kWh Per Day": 0.0,
            },        
            "Electric Car": {
                "Electric Car kWh Per Day": 0.0,
            },
            "Misc Plug Load": {
                "Misc Plug Load kWh Per Day": 0.0,
            }
        },
        "Locations":{
            "Monterey":{
                "Minimum Temperature F": 58,
                "Minimum GHI Watts/m^2 Average": 128,
            }
        },
        "Solar": {
            "Solar Area Required": 0.0,
            "Cost Of Solar Required": 0.0,
        }
    }

    fileName = "/workspaces/energy-use-calculator/EnergyUseData.json"

    with open(fileName, "w") as file:
        json.dump(EnergyJsonDefault, file, indent=4)


def calculateOutputsAndUpdateJson():
    fileName = "/workspaces/energy-use-calculator/EnergyUseData.json"

    if not os.path.exists(fileName):
        with open(fileName, "w") as f:
            writeDefaultJson()

    # Open file and load values
    with open(fileName, "r") as file:
        EnergyJson = json.load(file)
    
    # HVAC
    AirVolume = EnergyJson["Inputs"]["HVAC"]["Wall Height"] * EnergyJson["Inputs"]["HVAC"]["Floor Area"]
    WallArea = EnergyJson["Inputs"]["HVAC"]["Wall Height"] * EnergyJson["Inputs"]["HVAC"]["Floor Area"]**0.5 * 4
    EnergyJson["Outputs"]["HVAC"]["Wall Area sqft"] = WallArea
    WindowArea = WallArea * EnergyJson["Inputs"]["HVAC"]["Window Area Percent"]/100
    EnergyJson["Outputs"]["HVAC"]["Window Area sqft"] = WindowArea
    AirTemperatureDifference = abs(EnergyJson["Inputs"]["HVAC"]["Indoor Air Temperature F"] - EnergyJson["Inputs"]["HVAC"]["Outdoor Air Temperature F"])
    GroundTemperatureDifference = abs(EnergyJson["Inputs"]["HVAC"]["Indoor Air Temperature F"] - EnergyJson["Inputs"]["HVAC"]["Ground Temperature F"])
    SpecificHeatCapacityAir = 0.00001180556 # kWh/(ft^3*F)
    BTUPerHourToKwhPerDay = 0.00703371

    EnergyJson["Outputs"]["HVAC"]["Ventilation kWh Per Day"] = (EnergyJson["Inputs"]["HVAC"]["Air Changes Per Hour"] * AirVolume * AirTemperatureDifference * SpecificHeatCapacityAir * (1-EnergyJson["Inputs"]["HVAC"]["Ventilation Recovery Percent"]/100) ) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
    EnergyJson["Outputs"]["HVAC"]["Roof kWh Per Day"] = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Roof R Value"]) * EnergyJson["Inputs"]["HVAC"]["Floor Area"] * AirTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
    EnergyJson["Outputs"]["HVAC"]["Wall kWh Per Day"] = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Wall R Value"]) * WallArea * AirTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
    EnergyJson["Outputs"]["HVAC"]["Window kWh Per Day"] = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Window R Value"]) * WindowArea * AirTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
    EnergyJson["Outputs"]["HVAC"]["Floor kWh Per Day"] = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Floor R Value"]) * EnergyJson["Inputs"]["HVAC"]["Floor Area"] * GroundTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
    EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] = EnergyJson["Outputs"]["HVAC"]["Ventilation kWh Per Day"] + EnergyJson["Outputs"]["HVAC"]["Roof kWh Per Day"] + EnergyJson["Outputs"]["HVAC"]["Wall kWh Per Day"] + EnergyJson["Outputs"]["HVAC"]["Window kWh Per Day"] + EnergyJson["Outputs"]["HVAC"]["Floor kWh Per Day"]

    # Hot Water
    SpecificHeatCapacityWater = 0.00116 #kWh/(liter*C)
    WaterTemperatureDifferenceC = EnergyJson["Inputs"]["Hot Water"]["Water Heater Temperature C"] - EnergyJson["Inputs"]["Hot Water"]["Water Inlet Temperature C"] 
    EnergyJson["Outputs"]["Hot Water"]["Total Hot Water kWh Per Day"] = EnergyJson["Inputs"]["Hot Water"]["Water Use Per Day Liters"] * WaterTemperatureDifferenceC * SpecificHeatCapacityWater / (EnergyJson["Inputs"]["Hot Water"]["Water Heater Efficiency Percent"]/100) * (1-EnergyJson["Inputs"]["Hot Water"]["Water Heat Recovery Efficiency Percent"]/100)

    # Lighting
    EnergyJson["Outputs"]["Lighting"]["Lighting kWh Per Day"] = (EnergyJson["Inputs"]["Lighting"]["Lumens Per Square Foot"] * EnergyJson["Inputs"]["HVAC"]["Floor Area"]) / EnergyJson["Inputs"]["Lighting"]["Lumens Per Watt"] * EnergyJson["Inputs"]["Lighting"]["Lights On Hours Per Day"] / 1000

    # Cooking
    EnergyJson["Outputs"]["Cooking"]["Cooking kWh Per Day"] = EnergyJson["Inputs"]["Cooking"]["Cooking Appliance Wattage"] * EnergyJson["Inputs"]["Cooking"]["Cooking Hours Per Day"] / 1000

    # Clothes Drying
    EnergyJson["Outputs"]["Clothes Drying"]["Clothes Drying kWh Per Day"] = EnergyJson["Inputs"]["Clothes Drying"]["Clothes Drying Wattage"] * EnergyJson["Inputs"]["Clothes Drying"]["Clothes Drying Hours Per Day"] / 1000

    # Dishwasher
    EnergyJson["Outputs"]["Dishwasher"]["Dishwasher kWh Per Day"] = EnergyJson["Inputs"]["Dishwasher"]["Dishwasher Wattage"] * EnergyJson["Inputs"]["Dishwasher"]["Dishwasher Hours Per Day"] / 1000

    # Refrigerator
    EnergyJson["Outputs"]["Refrigerator"]["Refrigerator kWh Per Day"] = EnergyJson["Inputs"]["Refrigerator"]["Refrigerator kWh Per Year"] / 365

    # Electric Car
    EnergyJson["Outputs"]["Electric Car"]["Electric Car kWh Per Day"] = EnergyJson["Inputs"]["Electric Car"]["Electric Car kWh Per Day"]

    # Misc Plug Load
    EnergyJson["Outputs"]["Misc Plug Load"]["Misc Plug Load kWh Per Day"] = EnergyJson["Inputs"]["Misc Plug Load"]["Misc Plug Load kWh Per Day"]

    #Total
    EnergyJson["Outputs"]["Total"]["Total kWh Per Day"] =  EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] + EnergyJson["Outputs"]["Hot Water"]["Total Hot Water kWh Per Day"] + EnergyJson["Outputs"]["Lighting"]["Lighting kWh Per Day"] + EnergyJson["Outputs"]["Cooking"]["Cooking kWh Per Day"] + EnergyJson["Outputs"]["Clothes Drying"]["Clothes Drying kWh Per Day"] + EnergyJson["Outputs"]["Dishwasher"]["Dishwasher kWh Per Day"] + EnergyJson["Outputs"]["Refrigerator"]["Refrigerator kWh Per Day"] + EnergyJson["Outputs"]["Electric Car"]["Electric Car kWh Per Day"] + EnergyJson["Outputs"]["Misc Plug Load"]["Misc Plug Load kWh Per Day"] 

    # Solar Area Required
    EnergyJson["Solar"]["Solar Area Required"] = EnergyJson["Outputs"]["Total"]["Total kWh Per Day"] / (EnergyJson["Locations"]["Monterey"]["Minimum GHI Watts/m^2 Average"] * 24 / 1000) * 10.7 / 0.21
    EnergyJson["Solar"]["Cost Of Solar Required"] = EnergyJson["Solar"]["Solar Area Required"] * 10

    with open(fileName, "w") as file:
        json.dump(EnergyJson, file, indent=4)