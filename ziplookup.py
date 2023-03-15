import pandas as pd
import googlemaps
import os


API_KEY = os.getenv("YOUR_API_KEY") 
# Replace YOUR_API_KEY with your Google Maps API key
# A more ideal way to do this would be to add the key to your environment variables, then use os.getenv() to get it.
gmaps = googlemaps.Client(key=API_KEY)
file_path = "path/to/file.xlsx"
# Load addresses from Excel file and save to a new file with only the addresses in column A
df = pd.read_excel(file_path + 'addresses.xlsx', usecols=['Serial Number(No Duplicates)','Address'])

# Create a new column for the county
df['Zip Code'] = ''

# Loop through each row and get the county for each address
for i, row in df.iterrows():
    address = row['Address']
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        for component in geocode_result[0]['address_components']:
            if 'postal_code' in component['types']:
                df.at[i, 'Zip Code'] = component['long_name']
                break

# Save the updated dataframe to a new file
df.to_excel(file_path + 'addresses_with_zip.xlsx', index=False)
