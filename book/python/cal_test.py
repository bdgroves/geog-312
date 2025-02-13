import requests
import geopandas as gpd
import matplotlib.pyplot as plt

# Census Bureau API endpoint for 2020 county boundaries
url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2020/MapServer/82/query"

# Parameters to get only California counties (STATE='06')
params = {
    "where": "STATE='06'",  # California's FIPS code is '06'
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

    # Find Tuolumne County (FIPS Code: 109)
    tuolumne = counties[counties["COUNTY"] == "109"]

    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 12))

    # Plot all counties
    counties.plot(ax=ax, edgecolor="gray", facecolor="lightblue", alpha=0.5)

    # Highlight Tuolumne County
    tuolumne.plot(ax=ax, edgecolor="black", facecolor="red", alpha=0.7)

    # Add title
    ax.set_title("California Counties with Tuolumne Highlighted", fontsize=14)
    ax.set_axis_off()

    plt.show()

else:
    print("❌ Error fetching county data:", response.status_code)
