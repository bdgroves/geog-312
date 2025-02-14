import geopandas as gpd
import requests
import random
import matplotlib.pyplot as plt

# URL to get all counties from the Census TIGERweb service
COUNTY_URL = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Census2020/MapServer/82/query"

# Step 1: Get all counties
params = {
    "where": "1=1",  # Get all counties
    "outFields": "STATE_NAME,NAME,GEOID",
    "f": "geojson"
}

response = requests.get(COUNTY_URL, params=params)
data = response.json()

# Extract counties
features = data['features']
counties = [(f['properties']['STATE_NAME'], f['properties']['NAME'], f['properties']['GEOID']) for f in features]

# Step 2: Pick a random county
random_state, random_county, county_geoid = random.choice(counties)
print(f"Selected County: {random_county}, {random_state}")

# Step 3: Fetch county boundary
params = {
    "where": f"GEOID='{county_geoid}'",
    "outFields": "STATE_NAME,NAME,GEOID",
    "geometryType": "esriGeometryPolygon",
    "returnGeometry": "true",
    "f": "geojson"
}

response = requests.get(COUNTY_URL, params=params)
county_data = gpd.read_file(response.text)

# Step 4: Plot the county
fig, ax = plt.subplots(figsize=(8, 6))
county_data.plot(ax=ax, edgecolor="black", facecolor="lightblue")
ax.set_title(f"{random_county}, {random_state}")
plt.show()
