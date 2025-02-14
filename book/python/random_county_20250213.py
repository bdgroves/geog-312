import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import random

# List of state FIPS codes and their corresponding state names
state_fips_to_name = {
    "01": "Alabama", "02": "Alaska", "04": "Arizona", "05": "Arkansas", "06": "California", "08": "Colorado", "09": "Connecticut",
    "10": "Delaware", "11": "District of Columbia", "12": "Florida", "13": "Georgia", "15": "Hawaii", "16": "Idaho", "17": "Illinois",
    "18": "Indiana", "19": "Iowa", "20": "Kansas", "21": "Kentucky", "22": "Louisiana", "23": "Maine", "24": "Maryland", "25": "Massachusetts",
    "26": "Michigan", "27": "Minnesota", "28": "Mississippi", "29": "Missouri", "30": "Montana", "31": "Nebraska", "32": "Nevada", 
    "33": "New Hampshire", "34": "New Jersey", "35": "New Mexico", "36": "New York", "37": "North Carolina", "38": "North Dakota", 
    "39": "Ohio", "40": "Oklahoma", "41": "Oregon", "42": "Pennsylvania", "44": "Rhode Island", "45": "South Carolina", "46": "South Dakota",
    "47": "Tennessee", "48": "Texas", "49": "Utah", "50": "Vermont", "51": "Virginia", "53": "Washington", "54": "West Virginia", 
    "55": "Wisconsin", "56": "Wyoming", "72": "Puerto Rico", "78": "American Samoa"
}

# Randomly select a state FIPS code
random_state_fips = random.choice(list(state_fips_to_name.keys()))
state_name = state_fips_to_name[random_state_fips]

# Census Bureau API endpoint for 2020 county boundaries
url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2020/MapServer/82/query"

# Parameters to get counties for the randomly selected state
params = {
    "where": f"STATE='{random_state_fips}'",  # Use the random state FIPS code
    "outFields": "*",
    "f": "geojson"
}

# Fetch county data from the Census API
response = requests.get(url, params=params)

if response.status_code == 200:
    county_data = response.json()
    
    # Load into a GeoDataFrame
    counties = gpd.GeoDataFrame.from_features(county_data["features"])
    
    # Ensure CRS is set
    counties = counties.set_crs(epsg=4326)

    # Print the columns to inspect available data
    print(counties.columns)

    # Randomly select a county from the state's counties
    random_county = counties.sample(n=1)

    # Check available column names to find the county name
    print(random_county)

    # Assuming 'NAME' is the column that contains the county name
    county_name = random_county.iloc[0]['NAME']  # Update this based on the column name

    # Plot the map
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot all counties with a lighter color
    counties.plot(ax=ax, edgecolor="gray", facecolor="lightblue", alpha=0.5)

    # Highlight the randomly selected county with a bold color
    random_county.plot(ax=ax, edgecolor="black", facecolor="red", alpha=0.7)

    # Add the title at the top with a clean font style
    ax.set_title(f"Random County from {state_name} - {county_name} Highlighted", fontsize=16, fontweight='bold', color="darkblue", pad=20)

    # Turn off the axis to make the plot look cleaner
    ax.set_axis_off()

    # Tight layout to make sure the plot looks well-spaced
    plt.tight_layout()

    # Show the plot
    plt.show()

else:
    print("❌ Error fetching county data:", response.status_code)
