import json
import os

def writeDefaultJson():
    EnergyJsonDefault = {
    "Inputs": {
        "Irradiance": {
            "GHI Watts/m^2 Average": 200,
            "PV Efficiency": 0.20
        },
        "HVAC": {
            "Floor 1 Area": 750,
            "Floor 2 Area": 350,
            "Wall Height": 10,
            "Window Area": 200,
            "Roof R Value": 30,
            "Wall R Value": 19,
            "Floor R Value": 19,
            "Window R Value": 4,
            "Ground Temperature F": 60,
            "Outdoor Air Temperature F": 58,
            "Indoor Air Temperature F": 68,
            "HVAC Efficiency Percent": 100,
            "Air Changes Per Hour": 3,
            "Ventilation Recovery Percent": 25
        },
        "Solar Gain": {
            "South Facing Percent": 25,
            "Solar Heat Gain Coefficient, SHGC": 0.5
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
            "Lights On Hours Per Day": 2
        },
        "Cooking": {
            "Cooking Appliance Wattage": 2500,
            "Cooking Hours Per Day": 1.5
        },
        "Clothes Drying": {
            "Clothes Drying Wattage": 2500,
            "Clothes Drying Hours Per Day": 0.5
        },
        "Dishwasher": {
            "Dishwasher Wattage": 2500,
            "Dishwasher Hours Per Day": 0.5
        },
        "Refrigerator": {
            "Refrigerator kWh Per Year": 400
        },
        "Electric Car": {
            "Electric Car kWh Per Day": 0
        },
        "Misc Plug Load": {
            "Misc Plug Load kWh Per Day": 5
        },
        "Cost": {
            "PV Cost Per Square Foot": 43,
            "Battery Cost Per kWh": 1000,
            "Generator Cost Per kW": 600
        }
    },
    "Outputs": {
        "Total": {
            "Total kWh Per Day": 0
        },
        "HVAC": {
            "Total HVAC kWh Per Day": 0,
            "Ventilation kWh Per Day": 0,
            "Roof kWh Per Day": 0,
            "Wall kWh Per Day": 0,
            "Window kWh Per Day": 0,
            "Floor kWh Per Day": 0,
            "Wall Area sqft": 0,
            "Floor and Roof Area": 0,
            "Total Floor Area": 0
        },
        "Hot Water": {
            "Total Hot Water kWh Per Day": 0,
            "Min Energy Star Appliance kWh Per Day": 0,
            "Median Energy Star Appliance kWh Per Day": 0
        },
        "Lighting": {
            "Lighting kWh Per Day": 0,
        },
        "Cooking": {
            "Cooking kWh Per Day": 0,
            "Min Energy Star Appliance kWh Per Day": 0,
            "Median Energy Star Appliance kWh Per Day": 0
        },
        "Clothes Drying": {
            "Clothes Drying kWh Per Day": 0,
            "Min Energy Star Appliance kWh Per Day": 0,
            "Median Energy Star Appliance kWh Per Day": 0
        },
        "Dishwasher": {
            "Dishwasher kWh Per Day": 0,
            "Min Energy Star Appliance kWh Per Day": 0,
            "Median Energy Star Appliance kWh Per Day": 0
        },
        "Refrigerator": {
            "Refrigerator kWh Per Day": 0,
            "Min Energy Star Appliance kWh Per Day": 0,
            "Median Energy Star Appliance kWh Per Day": 0
        },
        "Electric Car": {
            "Electric Car kWh Per Day": 0
        },
        "Misc Plug Load": {
            "Misc Plug Load kWh Per Day": 0
        }
    },
    "Location": {
        "Latitude": 36.6,
        "Longitude": -121.85
    },
    "Location Data": {
        "3 Day Period": {
            "Lowest GHI Average (w/m^2)": 20.875,
            "Temperature During Lowest GHI": 57.525000000000006,
            "Lowest Temperature": 44.125,
            "GHI During Lowest Temperature": 142.27777777777777,
            "Total kWh Per Day For Lowest Temperature": 35.90378658627375,
            "Total Available Solar Thermal Energy": 35.11682242990655,
            "Solar Gain Through Windows": 1.1705607476635516,
            "Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature": 3651.4638957620864,
            "Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI": 3164.0936789952984,
            "Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)": 3.6872663551401876
        },
        "7 Day Period": {
            "Lowest GHI Average (w/m^2)": 40.88095238095238,
            "Temperature During Lowest GHI": 57.40357142857143,
            "Lowest Temperature": 45.949999999999996,
            "GHI During Lowest Temperature": 138.74404761904762,
            "Total kWh Per Day For Lowest Temperature": 33.96986913219112,
            "Total Available Solar Thermal Energy": 68.7716955941255,
            "Solar Gain Through Windows": 2.2923898531375166,
            "Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature": 1764.1118215610804,
            "Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI": 1618.4840420134785,
            "Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)": 7.221028037383178
        },
        "14 Day Period": {
            "Lowest GHI Average (w/m^2)": 57.333333333333336,
            "Temperature During Lowest GHI": 58.10000000000001,
            "Lowest Temperature": 48.77857142857143,
            "GHI During Lowest Temperature": 135.95238095238096,
            "Total kWh Per Day For Lowest Temperature": 31.788648234656623,
            "Total Available Solar Thermal Energy": 96.44859813084113,
            "Solar Gain Through Windows": 3.2149532710280377,
            "Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature": 1177.1128741376863,
            "Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI": 1142.5683728802283,
            "Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)": 10.12710280373832
        },
        "30 Day Period": {
            "Lowest GHI Average (w/m^2)": 72.18194444444444,
            "Temperature During Lowest GHI": 57.565000000000005,
            "Lowest Temperature": 50.3675,
            "GHI During Lowest Temperature": 139.18333333333334,
            "Total kWh Per Day For Lowest Temperature": 30.248974531996666,
            "Total Available Solar Thermal Energy": 121.42757009345796,
            "Solar Gain Through Windows": 4.047585669781932,
            "Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature": 889.6830581130804,
            "Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI": 914.5315782224696,
            "Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)": 12.749894859813084
        },
        "90 Day Period": {
            "Lowest GHI Average (w/m^2)": 95.90648148148148,
            "Temperature During Lowest GHI": 55.344166666666666,
            "Lowest Temperature": 52.538333333333334,
            "GHI During Lowest Temperature": 117.77638888888889,
            "Total kWh Per Day For Lowest Temperature": 27.952649424173917,
            "Total Available Solar Thermal Energy": 161.3380062305296,
            "Solar Gain Through Windows": 5.3779335410176525,
            "Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature": 618.7685910657447,
            "Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI": 710.1781495622402,
            "Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)": 16.940490654205608
        },
        "Average": {
            "Temperature F": 59.56536746575342,
            "GHI": 198.68394406392693
        }
    }
}

    fileName = "EnergyUseData.json"

    with open(fileName, "w") as file:
        json.dump(EnergyJsonDefault, file, indent=4)

def calcHVAC(EnergyJson, temp, groundTemp):
    # HVAC
    EnergyJson["Outputs"]["HVAC"]["Total Floor Area"] = EnergyJson["Inputs"]["HVAC"]["Floor 1 Area"] + EnergyJson["Inputs"]["HVAC"]["Floor 2 Area"]
    AirVolume = EnergyJson["Inputs"]["HVAC"]["Wall Height"] * EnergyJson["Outputs"]["HVAC"]["Total Floor Area"]
    WallArea1 = EnergyJson["Inputs"]["HVAC"]["Wall Height"] * EnergyJson["Inputs"]["HVAC"]["Floor 1 Area"]**0.5 * 4
    WallArea2 = EnergyJson["Inputs"]["HVAC"]["Wall Height"] * EnergyJson["Inputs"]["HVAC"]["Floor 2 Area"]**0.5 * 4
    EnergyJson["Outputs"]["HVAC"]["Wall Area sqft"] = WallArea1 + WallArea2
    EnergyJson["Outputs"]["HVAC"]["Floor and Roof Area"] = max(EnergyJson["Inputs"]["HVAC"]["Floor 1 Area"], EnergyJson["Inputs"]["HVAC"]["Floor 2 Area"])
    AirTemperatureDifference = abs(EnergyJson["Inputs"]["HVAC"]["Indoor Air Temperature F"] - temp)
    GroundTemperatureDifference = abs(EnergyJson["Inputs"]["HVAC"]["Indoor Air Temperature F"] - groundTemp)
    SpecificHeatCapacityAir = 0.00001180556 # kWh/(ft^3*F)
    BTUPerHourToKwhPerDay = 0.00703371

    if EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"] != 0:
        ventilationKwh = (EnergyJson["Inputs"]["HVAC"]["Air Changes Per Hour"] * AirVolume * AirTemperatureDifference * SpecificHeatCapacityAir * (1-EnergyJson["Inputs"]["HVAC"]["Ventilation Recovery Percent"]/100) ) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
        roofKwh = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Roof R Value"]) * EnergyJson["Outputs"]["HVAC"]["Floor and Roof Area"]* AirTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
        wallKwh = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Wall R Value"]) * EnergyJson["Outputs"]["HVAC"]["Wall Area sqft"] * AirTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
        windowKwh = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Window R Value"]) * EnergyJson["Inputs"]["HVAC"]["Window Area"] * AirTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
        floorKwh = (BTUPerHourToKwhPerDay * (1/EnergyJson["Inputs"]["HVAC"]["Floor R Value"]) * EnergyJson["Outputs"]["HVAC"]["Floor and Roof Area"] * GroundTemperatureDifference) / (EnergyJson["Inputs"]["HVAC"]["HVAC Efficiency Percent"]/100)
        totalKwh= ventilationKwh + roofKwh + wallKwh + windowKwh + floorKwh

    return totalKwh, ventilationKwh, roofKwh, wallKwh, windowKwh, floorKwh

def calculateOutputsAndUpdateJson():
    fileName = "EnergyUseData.json"

    if not os.path.exists(fileName):
        with open(fileName, "w") as f:
            writeDefaultJson()

    # Open file and load values
    with open(fileName, "r") as file:
        EnergyJson = json.load(file)

    totalKwh, ventilationKwh, roofKwh, wallKwh, windowKwh, floorKwh = calcHVAC(EnergyJson, EnergyJson["Inputs"]["HVAC"]["Outdoor Air Temperature F"], EnergyJson["Inputs"]["HVAC"]["Ground Temperature F"])

    EnergyJson["Outputs"]["HVAC"]["Ventilation kWh Per Day"] = ventilationKwh
    EnergyJson["Outputs"]["HVAC"]["Roof kWh Per Day"] = roofKwh
    EnergyJson["Outputs"]["HVAC"]["Wall kWh Per Day"] = wallKwh
    EnergyJson["Outputs"]["HVAC"]["Window kWh Per Day"] = windowKwh
    EnergyJson["Outputs"]["HVAC"]["Floor kWh Per Day"] = floorKwh
    EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] = totalKwh

    # Hot Water
    SpecificHeatCapacityWater = 0.00116 #kWh/(liter*C)
    WaterTemperatureDifferenceC = EnergyJson["Inputs"]["Hot Water"]["Water Heater Temperature C"] - EnergyJson["Inputs"]["Hot Water"]["Water Inlet Temperature C"] 
    EnergyJson["Outputs"]["Hot Water"]["Total Hot Water kWh Per Day"] = EnergyJson["Inputs"]["Hot Water"]["Water Use Per Day Liters"] * WaterTemperatureDifferenceC * SpecificHeatCapacityWater / (EnergyJson["Inputs"]["Hot Water"]["Water Heater Efficiency Percent"]/100) * (1-EnergyJson["Inputs"]["Hot Water"]["Water Heat Recovery Efficiency Percent"]/100)

    # Lighting
    EnergyJson["Outputs"]["Lighting"]["Lighting kWh Per Day"] = (EnergyJson["Inputs"]["Lighting"]["Lumens Per Square Foot"] * EnergyJson["Outputs"]["HVAC"]["Total Floor Area"]) / EnergyJson["Inputs"]["Lighting"]["Lumens Per Watt"] * EnergyJson["Inputs"]["Lighting"]["Lights On Hours Per Day"] / 1000

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

    with open(fileName, "w") as file:
        json.dump(EnergyJson, file, indent=4)
