import streamlit as st
import json_manager
import json
import solar_data_fetcher

# Setup Page Layout
st.set_page_config(layout="wide")

# Number of Days to Calculate Array
num_days = [3,7,14,30]

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
        EnergyJson["Location Data"][day_string]["Lowest GHI"] = lowest_ghi
        EnergyJson["Location Data"][day_string]["Temperature During Lowest GHI"] = temp_during_lowest_ghi
        EnergyJson["Location Data"][day_string]["Lowest Temperature"] = lowest_temp
        EnergyJson["Location Data"][day_string]["GHI During Lowest Temperature"] = ghi_during_lowest_temp

        # Calculate kwh and solar requirements
        kWhWithoutHvac = EnergyJson["Outputs"]["Total"]["Total kWh Per Day"] - EnergyJson["Outputs"]["HVAC"]["Total HVAC kWh Per Day"]
        totalHvacKwhLowestTemp = json_manager.calcHVAC(EnergyJson, lowest_temp, lowest_temp)[0]
        totalKwhLowestTemp = kWhWithoutHvac + totalHvacKwhLowestTemp
        EnergyJson["Location Data"][day_string]["Total kWh Per Day For Lowest Temperature"] = totalKwhLowestTemp

        # ghi (watts/m^2)
        # (watts/m^2) * (24 h/day) * (1/1000 kw/w) * (.21 efficiency)= (kwh/m^2/day @ 21% efficiency)
        # (kwh/m^2/day @ 21% efficiency) * (1/10.7 m^2/ft^2) = (kwh/ft^2/day @ 21% efficiency)
        efficiency = .21
        kwh_per_ft2_per_day = lowest_ghi * 24 * (1/1000) * efficiency * (1/10.7)
        pvAreaLowGhiLowTemp = totalKwhLowestTemp / kwh_per_ft2_per_day

        EnergyJson["Location Data"][day_string]["Total PV Panel Area ft^2 For Lowest GHI at Lowest Temperature"] = pvAreaLowGhiLowTemp
        totalHvacKwhTempDuringLowestGhi = json_manager.calcHVAC(EnergyJson, temp_during_lowest_ghi, temp_during_lowest_ghi)[0]
        totalKwhLowestGhi = kWhWithoutHvac + totalHvacKwhTempDuringLowestGhi
        pvAreaLowGhiStandardTemp = totalKwhLowestGhi / kwh_per_ft2_per_day
        EnergyJson["Location Data"][day_string]["Total PV Panel Area ft^2 For Lowest GHI at Temperature During Lowest GHI"] = pvAreaLowGhiStandardTemp

        target_energy_use = kwh_per_ft2_per_day * EnergyJson["Inputs"]["HVAC"]["Floor Area"] / 2
        EnergyJson["Location Data"][day_string]["Total kWh per Day at Lowest GHI and 1/2 Floor Area ft^2 (Target Energy Use)"] = target_energy_use

    # Save Values to File
    with open(fileName, "w") as file:
        json.dump(EnergyJson, file, indent=4)

# Display
colA, colB, colC = st.columns(3)

with colA:
    latitude = st.number_input("Input Latitude", value=None, placeholder="Ex. 36.60", help= 'Find a location in google maps and right click to access coordinates. Two decimal places are accurate to 1.1 km')
with colB:
    longitude = st.number_input("Input Longitude", value=None, placeholder="Ex. -121.85", help= 'Find a location in google maps and right click to access coordinates. Two decimal places are accurate to 1.1 km')
with colC:
    if (longitude != None) and (latitude != None):
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
                number = st.number_input(item, key=uniqueKey, value=st.session_state[uniqueKey], on_change=update_value(category, item, uniqueKey))

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

with open(fileName) as f:
   st.download_button('Download JSON of Data', f)