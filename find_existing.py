import urllib.request
import json
import urllib.parse

queries = [
    "Tuftepark Bærum idrettspark",
    "Bærum idrettspark",
    "Tuftepark Kadettangen",
    "Kadettangen",
    "Tuftepark Vardåsen",
    "Vardåsen Asker",
    "Tinkern",
    "Filipstad"
]

for q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json&countrycodes=no"
    req = urllib.request.Request(url, headers={'User-Agent': 'AktivOslo/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data:
                print(f"Query '{q}':")
                for item in data[:3]:
                    print(f"  Name: {item.get('display_name')}")
                    print(f"  Coords: {item.get('lat')}, {item.get('lon')}")
                    print(f"  ID: {item.get('osm_type')}/{item.get('osm_id')}")
            else:
                print(f"Query '{q}' returned no results")
    except Exception as e:
        print(f"Query '{q}' error: {e}")
