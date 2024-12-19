import streamlit as st
import json_manager
import json
import solar_data_fetcher
import energy_star_data_fetcher

# Setup Page Layout
st.set_page_config(layout="wide")

# Number of Days to Calculate Array
num_days = [3,7,14,30,90]

# Initialize JSON
fileName = "EnergyUseData.json"
json_manager.calculateOutputsAndUpdateJson()
with open(fileName, "r") as file:
    EnergyJson = json.load(file)

# Save Values to File
def update_value(category, item, uniqueKey):
    # Update Changed Value
    EnergyJson["Inputs"][category][item] = st.session_state[uniqueKey]
    # Save Values to File
    with open(fileName, "w") as file:
        json.dump(EnergyJson, file, indent=4)

def fetchData(latitude,longitude):
    st.write("Fetching Data takes 1-2 minutes (a while :)). Invalid Lat or Long will return an error")
    df = solar_data_fetcher.getGHIAndTemperature(latitude, longitude)
    EnergyJson["Location"]["Latitude"] = latitude
    EnergyJson["Location"]["Longitude"] = longitude
    for days in num_days:
        day_string = str(days) + " Day Period"
        # Search data for rolling average values
        lowest_ghi, temp_during_lowest_ghi, lowest_temp, ghi_during_lowest_temp = solar_data_fetcher.determineLowestTemperatureAndGhi(df, days)
        EnergyJson["Location Data"][day_string]["Lowest GHI Average (w/m^2)"] = lowest_ghi
        EnergyJson["Location Data"][day_string]["Temperature During Lowest GHI"] = temp_during_lowest_ghi
        EnergyJson["Location Data"][day_string]["Lowest Temperature"] = lowest_temp
        EnergyJson["Location Data"][day_string]["GHI During Lowest Temperature"] = ghi_during_lowest_temp

        # Get total solar kwh
        total_kwh_per_ft2_per_day = lowest_ghi * 24 * (1/1000) * (1/10.7)

        # Find Available Solar Thermal Energy
        EnergyJson["Location Data"][day_string]["Total Available Solar Thermal Energy"] = EnergyJson["Outputs"]["HVAC"]["Floor and Roof Area"] * total_kwh_per_ft2_per_day
        # Finding Solar gain through windows
        EnergyJson["Location Data"][day_string]["Solar Gain Through Windows"] = EnergyJson["Inputs"]["HVAC"]["Window Area"] * (EnergyJson["Inputs"]["Solar Gain"]["South Facing Percent"] / 100) * EnergyJson["Inputs"]["Solar Gain"]["Solar Heat Gain Coefficient, SHGC"] * total_kwh_per_ft2_per_day

        # Calculate kwh and solar requirements
        kWhWithoutHvac = EnergyJson["Outputs"]["Total"]["Total kWh Per Day"] - EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"]
        totalHvacKwhLowestTemp = json_manager.calcHVAC(EnergyJson, lowest_temp, lowest_temp)[0]
        totalKwhLowestTemp = kWhWithoutHvac + max((totalHvacKwhLowestTemp - EnergyJson["Location Data"][day_string]["Solar Gain Through Windows"]), 0)
        EnergyJson["Location Data"][day_string]["Total kWh Per Day For Lowest Temperature"] = totalKwhLowestTemp

        # ghi (watts/m^2)
        # (watts/m^2) * (24 h/day) * (1/1000 kw/w) * ( efficiency)= (kwh/m^2/day @ efficiency)
        # (kwh/m^2/day @ efficiency) * (1/10.7 m^2/ft^2) = (kwh/ft^2/day @ efficiency)
        efficiency = EnergyJson["Inputs"]["Irradiance"]["PV Efficiency"]
        kwh_per_ft2_per_day = total_kwh_per_ft2_per_day * efficiency
        pvAreaLowGhiLowTemp = totalKwhLowestTemp / kwh_per_ft2_per_day

        EnergyJson["Location Data"][day_string]["Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature"] = pvAreaLowGhiLowTemp
        totalHvacKwhTempDuringLowestGhi = json_manager.calcHVAC(EnergyJson, temp_during_lowest_ghi, temp_during_lowest_ghi)[0]
        totalKwhLowestGhi = kWhWithoutHvac + totalHvacKwhTempDuringLowestGhi
        pvAreaLowGhiStandardTemp = totalKwhLowestGhi / kwh_per_ft2_per_day
        EnergyJson["Location Data"][day_string]["Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI"] = pvAreaLowGhiStandardTemp

        target_energy_use = kwh_per_ft2_per_day * EnergyJson["Outputs"]["HVAC"]["Floor and Roof Area"] / 2
        EnergyJson["Location Data"][day_string]["Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)"] = target_energy_use

        # Get average values
        avg_ghi,avg_temp = solar_data_fetcher.determineAverageTemperatureAndGhi(df)
        EnergyJson["Location Data"]["Average"]["Temperature F"] = avg_temp
        EnergyJson["Location Data"]["Average"]["GHI"] = avg_ghi

    # Save Values to File
    with open(fileName, "w") as file:
        json.dump(EnergyJson, file, indent=4)

    return avg_ghi, avg_temp

def fetchEnergyStarData():
    EnergyJson["Outputs"]["Refrigerator"]["Min Energy Star Appliance kWh Per Day"], EnergyJson["Outputs"]["Refrigerator"]["Median Energy Star Appliance kWh Per Day"] = energy_star_data_fetcher.getFridgeData()
    EnergyJson["Outputs"]["Cooking"]["Min Energy Star Appliance kWh Per Day"], EnergyJson["Outputs"]["Cooking"]["Median Energy Star Appliance kWh Per Day"] = energy_star_data_fetcher.getStoveData()
    EnergyJson["Outputs"]["Clothes Drying"]["Min Energy Star Appliance kWh Per Day"], EnergyJson["Outputs"]["Clothes Drying"]["Median Energy Star Appliance kWh Per Day"] = energy_star_data_fetcher.getDryerData()
    EnergyJson["Outputs"]["Dishwasher"]["Min Energy Star Appliance kWh Per Day"], EnergyJson["Outputs"]["Dishwasher"]["Median Energy Star Appliance kWh Per Day"] = energy_star_data_fetcher.getDishwasherData()
    EnergyJson["Outputs"]["Hot Water"]["Min Energy Star Appliance kWh Per Day"], EnergyJson["Outputs"]["Hot Water"]["Median Energy Star Appliance kWh Per Day"] = energy_star_data_fetcher.getWaterHeaterData()
    # Save Values to File
    with open(fileName, "w") as file:
        json.dump(EnergyJson, file, indent=4)

if (EnergyJson["Outputs"]["Hot Water"]["Min Energy Star Appliance kWh Per Day"] == 0):
    fetchEnergyStarData()

# Display
colA, colB, colC = st.columns(3)

with colA:
    latitude = st.number_input("Input Latitude", value=None, placeholder="Ex. 36.60", help= 'Find a location in google maps and right click to access coordinates. Two decimal places are accurate to 1.1 km')
with colB:
    longitude = st.number_input("Input Longitude", value=None, placeholder="Ex. -121.85", help= 'Find a location in google maps and right click to access coordinates. Two decimal places are accurate to 1.1 km')
with colC:
    if ((longitude != None) and (longitude != EnergyJson["Location"]["Longitude"])) and ((latitude != None) and (latitude != EnergyJson["Location"]["Latitude"])):
        submitted = st.button("Fetch Location Data", on_click= fetchData(latitude,longitude))
    else:
        st.write("Input Lat and Long to fetch location data")

# Display
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Inputs")

    for category in EnergyJson["Inputs"]:
        with st.expander(category + " Inputs"):
            for item in EnergyJson["Inputs"][category]:
                uniqueKey = str(category + item)
                if uniqueKey not in st.session_state:
                    st.session_state[uniqueKey] = EnergyJson["Inputs"][category][item]
                number = st.number_input(item, key=uniqueKey, on_change=update_value(category, item, uniqueKey))

with col2:
    st.header("Energy Use")

    for category in EnergyJson["Outputs"]:
        with st.expander(category + " Energy Use"):
            colA, colB = st.columns(2)
            for item in EnergyJson["Outputs"][category]:
                value = round(EnergyJson["Outputs"][category][item], 2)
                colA.write(f"{item}")
                colB.write(value)

with col3:
    st.header("Location Outputs", help= "Calculated with NREL data from 2001-2020. Calculations assume ground temperature is the same as worst case air temperature")

    colA, colB = st.columns(2)
    colA.write("Previously Input Latitude: ")
    colA.write(EnergyJson["Location"]["Latitude"])
    colB.write("Previously Input Longitude: ")
    colB.write(EnergyJson["Location"]["Longitude"])

    for days in num_days:
        day_string = str(days) + " Day Period"
        with st.expander(day_string):
            for item in EnergyJson["Location Data"][day_string]:
                st.write(f"{item}")
                value = round(EnergyJson["Location Data"][day_string][item], 2)
                st.write(value)
    
    with st.expander("Summary Of Target Energy Use"):
        for days in num_days:
            day_string = str(days) + " Day Period"
            day_title = str(days) + " Day Period Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2"
            st.write(f"{day_title}")
            value = round(EnergyJson["Location Data"][day_string]["Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)"], 2)
            st.write(value)

        st.write("Input Appliance Energy Use + Misc Energy Use")
        st.write(round(EnergyJson["Outputs"]["Total"]["Total kWh Per Day"] - EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"], 2))
        st.write("Min Energy Star Appliance Energy Use")
        min_energy_star_use = round(EnergyJson["Outputs"]["Lighting"]["Lighting kWh Per Day"] + EnergyJson["Outputs"]["Refrigerator"]["Min Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Cooking"]["Min Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Clothes Drying"]["Min Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Dishwasher"]["Min Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Hot Water"]["Min Energy Star Appliance kWh Per Day"], 2)
        st.write(min_energy_star_use)
        st.write("Median Energy Star Appliance Energy Use")
        st.write(round(EnergyJson["Outputs"]["Lighting"]["Lighting kWh Per Day"] + EnergyJson["Outputs"]["Refrigerator"]["Median Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Cooking"]["Median Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Clothes Drying"]["Median Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Dishwasher"]["Median Energy Star Appliance kWh Per Day"] + EnergyJson["Outputs"]["Hot Water"]["Median Energy Star Appliance kWh Per Day"], 2))
        st.write("HVAC Energy Use")
        st.write(round(EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"], 2))
        st.write("Minimum Energy Star and HVAC Energy Use")
        st.write(round(EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] + min_energy_star_use, 2))

    with st.expander("Averages"):
        st.write("Average Temperature F")
        st.write(round(EnergyJson["Location Data"]["Average"]["Temperature F"], 2))
        st.write("Average GHI")
        st.write(round(EnergyJson["Location Data"]["Average"]["GHI"], 2))
        st.write("Lowest 90 Day Average Temperature")
        st.write(round(EnergyJson["Location Data"]["90 Day Period"]["Lowest Temperature"], 2))        
        st.write("Lowest 90 Day Average GHI")
        st.write(round(EnergyJson["Location Data"]["90 Day Period"]["Lowest GHI Average (w/m^2)"], 2))
        st.write("Average US Home Energy Use (2000 sqft) kWh/day")
        st.write(EnergyJson['Outputs']["Total"]["Average US Home Energy Use (2000 sqft) kWh/day"])

    # PV System Sizing and Costs
    for item in ["input", "energy_star"]:
        energy_required = 0
        title = ""
        if item == "input":
            title = "System PV Sizing And Costs for Total Energy Use as Input"
            energy_required = round(EnergyJson["Outputs"]["Total"]["Total kWh Per Day"], 2)
        else:
            title = "System PV Sizing And Costs for Total Minimum Energy Star Appliance, Input Lighting and HVAC"
            energy_required = round(EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] + min_energy_star_use, 2)

        with st.expander(title):
            st.write("Energy Required kWh/day")
            st.write(energy_required)

            st.write("Max Available Roof Area")
            st.write(round(EnergyJson["Outputs"]["HVAC"]["Floor and Roof Area"], 2))

            st.write("Solar Panel Area Required for Minimum 14 Day GHI")
            pv_conversion = 24 / 10.7 / 1000 * EnergyJson["Inputs"]["Irradiance"]["PV Efficiency"]
            kwh_per_sqft = EnergyJson["Location Data"]["14 Day Period"]["Lowest GHI Average (w/m^2)"] * pv_conversion
            sqft_required = round(energy_required/kwh_per_sqft, 2)
            st.write(sqft_required)

            st.write("Cost for Solar Panels for 14 Day GHI")
            st.write(round(sqft_required * EnergyJson["Inputs"]["Cost"]["PV Cost Per Square Foot"], 2))
            # "Battery Cost Per kWh": 1000,
            # "Generator Cost Per kW": 

            st.write("Solar Panel Area Required for Average GHI")
            kwh_per_sqft = EnergyJson["Location Data"]["Average"]["GHI"] * pv_conversion
            sqft_required = round(energy_required/kwh_per_sqft, 2)
            st.write(sqft_required)

            st.write("Cost for Solar Panels for Average GHI")
            st.write(round(sqft_required * EnergyJson["Inputs"]["Cost"]["PV Cost Per Square Foot"], 2))

    # Battery System Sizing and Costs
    for item in ["input", "energy_star"]:
        energy_required = 0
        title = ""
        if item == "input":
            title = "System Battery Sizing And Costs for Total Energy Use as Input"
            energy_required = round(EnergyJson["Outputs"]["Total"]["Total kWh Per Day"], 2)
        else:
            title = "System Battery Sizing And Costs for Total Minimum Energy Star Appliance, Input Lighting and HVAC"
            energy_required = round(EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] + min_energy_star_use, 2)

        with st.expander(title):
            st.write("Energy Required kWh/day")
            st.write(energy_required)

            st.write("Solar Energy Available for Lowest 14 Day Period 1/2 Roof Area kwh/day")
            solar_energy_available = round(EnergyJson["Location Data"]["14 Day Period"]["Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)"], 2)
            st.write(solar_energy_available)

            st.write("Battery Storage Required for 14 Day Period With Solar kWh")
            battery_kwh_required_solar = (energy_required - solar_energy_available) * 14
            st.write(battery_kwh_required_solar)

            st.write("Battery Storage Required for 14 Day Period No Solar kWh")
            battery_kwh_required = (energy_required) * 14
            st.write(battery_kwh_required)

            st.write("Cost for Battery Storage With Solar")
            st.write(round(battery_kwh_required_solar * EnergyJson["Inputs"]["Cost"]["Battery Cost Per kWh"], 2))
            # "Generator Cost Per kW": 

            st.write("Cost for Battery Storage No Solar")
            st.write(round(battery_kwh_required * EnergyJson["Inputs"]["Cost"]["Battery Cost Per kWh"], 2))
            # "Generator Cost Per kW": 

    # Generator System Sizing and Costs
    for item in ["input", "energy_star"]:
        energy_required = 0
        title = ""
        if item == "input":
            title = "System Generator Sizing And Costs for Total Energy Use as Input"
            energy_required = round(EnergyJson["Outputs"]["Total"]["Total kWh Per Day"], 2)
        else:
            title = "System Generator Sizing And Costs for Total Minimum Energy Star Appliance, Input Lighting and HVAC"
            energy_required = round(EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"] + min_energy_star_use, 2)

        with st.expander(title):
            st.write("Energy Required kWh/day")
            st.write(energy_required)

            st.write("Peak Power / Generator Size Estimate Assuming All Daily Energy Used in 2 hours kW")
            peak_power_estimate = round(energy_required / 2, 2)
            st.write(peak_power_estimate)

            st.write("Average Power / Generator Size Required kW")
            average_power = round(energy_required / 24, 2)
            st.write(average_power)

            for power in [average_power, peak_power_estimate]:
                if power == average_power:
                    st.markdown("***Average Power Generator Calculations***")
                else:
                    st.markdown("***Peak Power Generator Calculations***")
    
                st.write("Generator Purchase Cost")
                st.write(round(power * EnergyJson["Inputs"]["Cost"]["Generator Cost Per kW"], 2))

                st.write("Generator Fuel Storage Required For 14 Day Outage")
                fuel_used = round(power * EnergyJson["Inputs"]["Cost"]["Generator Propane Fuel Use (Gallons/day/kW)"] * 14, 2)
                st.write(fuel_used)

                st.write("Cost of Fuel For 14 Day Outage")
                st.write(round(fuel_used * EnergyJson["Inputs"]["Cost"]["Generator Propane Cost per Gallon"], 2))

                st.write("Yearly Propane Use To Exercise Generator Gallons")
                yearly_fuel_used_exercising = round(power * EnergyJson["Inputs"]["Cost"]["Generator Exercising Propane Fuel Use (Gallons/day/kW)"] * 365, 2)
                st.write(yearly_fuel_used_exercising)

                st.write("Yearly Cost To Exercise Generator")
                yearly_cost_exercising = round(yearly_fuel_used_exercising * EnergyJson["Inputs"]["Cost"]["Generator Propane Cost per Gallon"], 2)
                st.write(yearly_cost_exercising)


# JSON upload and download
with open(fileName) as f:
   st.download_button('Download JSON of Data To Save For Later', f)

def processFile(fileKey):
    if (st.session_state[fileKey] != None) and (st.session_state["file_uploaded"] == 0):
        EnergyJson = json.load(st.session_state[fileKey])
        with open(fileName, "w") as file:
            json.dump(EnergyJson, file, indent=4)
        with open(fileName, "r") as file:
            EnergyJson = json.load(file)
        json_manager.calculateOutputsAndUpdateJson()
        for category in EnergyJson["Inputs"]:
            for item in EnergyJson["Inputs"][category]:
                uniqueKey = str(category + item)
                del st.session_state[uniqueKey]
        st.session_state["file_uploaded"] += 1
    elif (st.session_state[fileKey] == None):
        st.session_state["file_uploaded"] = 0        
    
fileKey = str("uploaded_file")
if fileKey not in st.session_state:
    st.session_state[fileKey] = None

if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = 0

try:
    st.file_uploader("Upload JSON file to Update JSON", key = fileKey, type = ["json", "txt"], on_change=processFile(fileKey))

    if st.button("Reset to Default Values"):
        json_manager.writeDefaultJson()
        for category in EnergyJson["Inputs"]:
            for item in EnergyJson["Inputs"][category]:
                uniqueKey = str(category + item)
                del st.session_state[uniqueKey]
        st.write("Reset JSON Values to Default")

    if st.button("Update Application with JSON Values"):
        st.write("Updated Values")
except:
    st.write("Reload to Upload JSON File")
    # st.rerun()

