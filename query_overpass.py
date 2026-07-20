import urllib.request
import urllib.parse
import json

overpass_url = "https://overpass.kumi.systems/api/interpreter"

# Overpass query to get fitness stations in Oslo, Bærum, and Asker municipalities
overpass_query = """
[out:json][timeout:90];
(
  area["name"="Oslo"]->.oslo;
  area["name"="Bærum"]->.baerum;
  area["name"="Asker"]->.asker;
);
(
  node(area.oslo)["leisure"="fitness_station"];
  way(area.oslo)["leisure"="fitness_station"];
  node(area.oslo)["amenity"="fitness_station"];
  way(area.oslo)["amenity"="fitness_station"];
  
  node(area.baerum)["leisure"="fitness_station"];
  way(area.baerum)["leisure"="fitness_station"];
  node(area.baerum)["amenity"="fitness_station"];
  way(area.baerum)["amenity"="fitness_station"];

  node(area.asker)["leisure"="fitness_station"];
  way(area.asker)["leisure"="fitness_station"];
  node(area.asker)["amenity"="fitness_station"];
  way(area.asker)["amenity"="fitness_station"];
);
out center;
"""

print("Sending query to Overpass API (kumi.systems)...")
try:
    data = urllib.parse.urlencode({'data': overpass_query}).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = urllib.request.Request(overpass_url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        res_data = response.read().decode('utf-8')
        json_data = json.loads(res_data)
        elements = json_data.get('elements', [])
        print(f"Received {len(elements)} elements.")
        with open("overpass_raw.json", "w") as f:
            json.dump(json_data, f, indent=2)
        print("Saved raw data to overpass_raw.json")
except Exception as e:
    print("Error querying Overpass:", e)
