import urllib.request
import urllib.parse
import json

def get_overpass(bbox_str):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""[out:json][timeout:25];
(
  node({bbox_str});
  way({bbox_str});
  relation({bbox_str});
);
out body;
>;
out skel qt;"""
    data = urllib.parse.urlencode({'data': query}).encode('utf-8')
    req = urllib.request.Request(
        overpass_url, 
        data=data,
        headers={'User-Agent': 'Mozilla/5.0 (Python script)'}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

lutvann_bbox = "59.9031,10.8734,59.9201,10.8826"
print("Fetching Lutvann OSM...")
lutvann_data = get_overpass(lutvann_bbox)
with open("lutvann_osm.json", "w") as f:
    json.dump(lutvann_data, f)

osternvann_bbox = "59.9662,10.5712,59.9711,10.5955"
print("Fetching Østernvann OSM...")
osternvann_data = get_overpass(osternvann_bbox)
with open("osternvann_osm.json", "w") as f:
    json.dump(osternvann_data, f)

print("Done downloading OSM data.")
