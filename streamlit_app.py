import streamlit as st
import json_manager
import json
import os
import solar_data_fetcher

# Setup Page Layout
st.set_page_config(layout="wide")

# Number of Days to Calculate Array
num_days = [3,7,14,30]

# Initialize JSON
fileName = "/workspaces/energy-use-calculator/EnergyUseData.json"
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

def fetchData(latitude,longitude, num_days):
    st.write("Fetching Data takes 1-2 minutes, invalid Lat or Long will return an error")
    df = solar_data_fetcher.getGHIAndTemperature(latitude, longitude)
    lowest_ghi, temp_during_lowest_ghi, lowest_temp, ghi_during_lowest_temp = solar_data_fetcher.determineLowestTemperatureAndGhi(df, num_days)
    EnergyJson["Location"]["Lowest GHI"] = lowest_ghi
    EnergyJson["Location"]["Temperature During Lowest GHI"] = temp_during_lowest_ghi
    EnergyJson["Location"]["Lowest Temperature"] = lowest_temp
    EnergyJson["Location"]["GHI During Lowest Temperature"] = ghi_during_lowest_temp
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
        submitted = st.button("Fetch Location Data", on_click= fetchData(latitude,longitude, 14))
    else:
        st.write("Input Lat and Long to fetch location data")


# Display
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Inputs")

    with st.expander("Select Location"):
        LocationOptions = ["None"]
        for item in EnergyJson["Locations"]:
            LocationOptions.append(item)
        
        option = st.selectbox(
            "Locations",
            LocationOptions,
        )
        if option != "None":
            EnergyJson["Inputs"]["HVAC"]["Outdoor Air Temperature F"] = EnergyJson["Locations"][option]["Minimum Temperature F"]
            EnergyJson["Inputs"]["Irradiance"]["GHI Watts/m^2 Average"] = EnergyJson["Locations"][option]["Minimum GHI Watts/m^2 Average"]

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
    st.header("Location Outputs")

    st.write("Latitude: ")
    st.write(EnergyJson["Location"]["Latitude"])
    st.write("Longitude: ")
    st.write(EnergyJson["Location"]["Longitude"])

    for days in num_days:
        day_string = str(days) + " Day Period"
        with st.expander(day_string):
            for item in EnergyJson["Location Data"][day_string]:
                st.write(f"{item}")
                value = round(EnergyJson["Location Data"][day_string][item], 2)
                st.write(value)
