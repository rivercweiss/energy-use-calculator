import streamlit as st
import json_manager
import json
import os

# Setup Page Layout
st.set_page_config(layout="wide")

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
                colA.write(item)
                colB.write(EnergyJson["Outputs"][category][item])

with col3:
    st.header("Worst Case Temperature 3 Days")
    st.header("Worst Case Temperature 7 Days")
    st.header("Worst Case Temperature 14 Days")
    
    st.header("Worst Case GHI 3 Days")
    st.header("Worst Case GHI 7 Days")
    st.header("Worst Case GHI 14 Days")

    st.header("Photovoltaic Area Required")
