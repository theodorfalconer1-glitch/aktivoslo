import urllib.request
import json

# Let's search overpass for any fitness_station near Gjønnesjordet coordinates (59.9177, 10.5750)
query = """
[out:json][timeout:25];
(
  node(around:200, 59.9177437, 10.5750702);
  way(around:200, 59.9177437, 10.5750702);
);
out center;
"""
url = "https://overpass-api.de/api/interpreter"
req = urllib.request.Request(url, data=urllib.parse.urlencode({'data': query}).encode('utf-8'), headers={'User-Agent': 'AktivOslo/1.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for e in data.get('elements', []):
            tags = e.get('tags', {})
            if 'leisure' in tags or 'sport' in tags or 'fitness' in tags or 'name' in tags:
                print(f"ID: {e.get('type')}/{e.get('id')}")
                print(f"  Coords: {e.get('lat') or e.get('center', {}).get('lat')}, {e.get('lon') or e.get('center', {}).get('lon')}")
                print(f"  Tags: {json.dumps(tags, indent=2)}")
except Exception as e:
    print(f"Error: {e}")
