import pandas as pd
import requests
import io
import time
import numpy as np
import matplotlib.pyplot as plt

def getGHIAndTemperature(latitude, longitude):
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
    # df = pd.DataFrame()
    dfs = []
    # Define the lat, long of the location and the year
    # Go to google maps and right click on the location
    # lat, lon = 36.606841513598376, -121.85034252078556
    # You must request an NSRDB api key from the link above
    api_key = "Ad1qlGIShmsjx7RiNp3P02bRFeGb4PX4FDGFkqNN"
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,air_temperature'
    # Choose year of data
    years = []
    for year in range(2001,2021):
        years.append(str(year))
    # Set leap year to true or false. True will return leap day data if present, false will not.
    leap_year = 'false'
    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '60'
    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'false'
    # Your full name, use '+' instead of spaces.
    your_name = 'River+Weiss'
    # Your reason for using the NSRDB.
    reason_for_use = 'solar+modeling'
    # Your affiliation
    your_affiliation = 'my+institution'
    # Your email address
    your_email = 'riverwiess@gmail.com'
    # Please join our mailing list so we can keep you up-to-date on new developments.
    mailing_list = 'false'

    # Declare url string
    for year in years:
        url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=latitude, lon=longitude, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
        response = requests.get(url)
        time.sleep(1)
        dfs.append(pd.read_csv(io.StringIO(response.text), skiprows=2))

    df = pd.concat(dfs, ignore_index=True)
    df['Temperature'] = df['Temperature'] * 1.8 + 32
    return df

def determineLowestTemperatureAndGhi(df, num_days):
    window_size = 24 * num_days

    rolling_avg_ghi = df['GHI'].rolling(window=window_size).mean()

    # Get the index of the minimum average value
    lowest_avg_index_ghi = rolling_avg_ghi.idxmin()
    # Access the corresponding date range for the period with the lowest average
    start_index_ghi = df.index[lowest_avg_index_ghi - window_size + 1]

    rolling_avg_temp = df['Temperature'].rolling(window=window_size).mean()

    # Get the index of the minimum average value
    lowest_avg_index_temp = rolling_avg_temp.idxmin()
    # Access the corresponding date range for the period with the lowest average
    start_index_temp = df.index[lowest_avg_index_temp - window_size + 1]

    lowest_ghi = rolling_avg_ghi[lowest_avg_index_ghi]
    temp_during_lowest_ghi = rolling_avg_temp[lowest_avg_index_ghi]

    lowest_temp = rolling_avg_temp[lowest_avg_index_temp]
    ghi_during_lowest_temp = rolling_avg_ghi[lowest_avg_index_temp]


    return lowest_ghi, temp_during_lowest_ghi, lowest_temp, ghi_during_lowest_temp

def determineAverageTemperatureAndGhi(df):

    avg_ghi = df['GHI'].mean()
    avg_temp = df['Temperature'].mean()

    return avg_ghi, avg_temp

def getTempAndGhiPercentiles(full_df):
    average_df = full_df.groupby(np.arange(len(full_df))//24).mean()
    
    df = average_df[["Temperature", "GHI"]]
    percentiles = [1,5,10,25,50,75,90,95,99]
    distribution = pd.DataFrame(percentiles)
    distribution.rename(columns={0: "Percentiles"}, inplace=True)

    temperature = np.percentile(df["Temperature"], percentiles)
    ghi = np.percentile(df["GHI"], percentiles)

    distribution["Temperature"] = temperature
    distribution["GHI"] = ghi
    distribution['Percentiles'] = distribution['Percentiles'].astype(str) 

    plt.bar(distribution['Percentiles'], distribution['Temperature'])

    plt.xlabel('Percentiles')
    plt.ylabel('Temperature F')
    plt.title('Percentiles of Daily Average Temperature')
    plt.ylim(min(distribution['Temperature'] - 2), max(distribution['Temperature'] + 2))
    plt.locator_params(axis='y', nbins=15)

    plt.savefig('average_temperature_percentiles.png')
    plt.clf()  # Clear the entire figure

    plt.bar(distribution['Percentiles'], distribution['GHI'])

    plt.xlabel('Percentiles')
    plt.ylabel('GHI W/m^2')
    plt.title('Percentiles of Daily Average GHI')
    plt.ylim(min(distribution['GHI'] - 2), max(distribution['GHI'] + 2))
    plt.locator_params(axis='y', nbins=15)
    plt.savefig('average_ghi_percentiles.png')
    plt.clf()  # Clear the entire figure

def getTempAndGhiDistribution(full_df):
    average_df = full_df.groupby(np.arange(len(full_df))//24).mean()
    
    average_df['Temperature'].hist(bins=50)

    plt.xlabel('Temperature')
    plt.ylabel('Frequency')
    plt.title('Distribution of Daily Average Temperature')
    plt.locator_params(axis='x', nbins=15)

    plt.savefig('average_temperature_distribution.png')
    plt.clf()  # Clear the entire figure

    average_df['GHI'].hist(bins=50)

    plt.xlabel('GHI')
    plt.ylabel('Frequency')
    plt.title('Distribution of Daily Average GHI')
    plt.locator_params(axis='x', nbins=15)

    plt.savefig('average_ghi_distribution.png')
    plt.clf()  # Clear the entire figure
    