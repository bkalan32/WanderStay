import requests
import json
import pandas as pd

# URL for the API 
url = "https://example.com/hotels?city=New+York"

# GET request to the URL using the requests module, stored in a variable
response = requests.get(url)

# Check the response status code is 200 (OK),if not  raise an exception or return an error message
if response.status_code != 200:
    raise Exception(f"Request failed with status code {response.status_code}")

# Parse and store, then convert to df
data = json.loads(response.content)
df = pd.DataFrame(data)

# Sort and filter based off ratings and availability
sorted_df = df.sort_values(by="rating", ascending=False)
filtered_df = sorted_df[sorted_df["availability"] == True]

# Select the top 5 rows and store 
top_5_df = filtered_df.head(5)

# Convert the top 5 rows to a JSON object using the pandas module, and store it in a variable
top_5_json = top_5_df.to_json(orient="records")
return top_5_json