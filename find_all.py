import urllib.request
import urllib.parse
import json

def overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    data = urllib.parse.urlencode({'data': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Base44-Data-Research-Agent/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error querying Overpass: {e}")
        return None

routes_info = [
    {"id": "slottsparken", "name": "Slottsparken løperute", "lat": 59.91761, "lng": 10.72791},
    {"id": "bygdoy_runden", "name": "Bygdøy-runden (8 km)", "lat": 59.9181808, "lng": 10.6876051},
    {"id": "bogstadvannet_rundt", "name": "Bogstadvannet rundt (9 km)", "lat": 59.97175, "lng": 10.61791},
    {"id": "akerselva_nedover", "name": "Akerselva nedover (7 km)", "lat": 59.96676, "lng": 10.77394},
    {"id": "noklevann_rundt", "name": "Nøklevann rundt (8 km)", "lat": 59.8723, "lng": 10.8601},
    {"id": "sognsvann_rundt", "name": "Sognsvann rundt (3.3 km)", "lat": 59.9752, "lng": 10.7291},
    {"id": "maridalsvannet_rundt", "name": "Maridalsvannet rundt (15 km)", "lat": 59.9829, "lng": 10.78001},
    {"id": "frognerparken", "name": "Frognerparken løperute", "lat": 59.9263, "lng": 10.6978},
    {"id": "frognerkilen_tjuvholmen", "name": "Frognerkilen og Tjuvholmen (flat 5 km)", "lat": 59.916768, "lng": 10.68701},
    {"id": "ostensjovannet_rundt", "name": "Østensjøvannet rundt (7 km)", "lat": 59.8822, "lng": 10.8348}
]

for route in routes_info:
    print(f"\n--- Exploring route: {route['name']} ({route['id']}) ---")
    # Query features around lat, lng
    # We look for:
    # 1. Any relation with 'route' or 'boundary' or name matching
    # 2. Any way with name matching
    # Let's search around 1km
    query = f"""
    [out:json];
    (
      relation(around:1000, {route['lat']}, {route['lng']})["name"~"({route['name'].split()[0]}|rundt|rute|sti)",i];
      way(around:500, {route['lat']}, {route['lng']})["name"~"({route['name'].split()[0]})",i];
      relation(around:1000, {route['lat']}, {route['lng']})["boundary"="national_park"];
      relation(around:1000, {route['lat']}, {route['lng']})["leisure"="park"];
      way(around:1000, {route['lat']}, {route['lng']})["leisure"="park"];
      relation(around:1000, {route['lat']}, {route['lng']})["water"="lake"];
      way(around:1000, {route['lat']}, {route['lng']})["water"="lake"];
      relation(around:1000, {route['lat']}, {route['lng']})["natural"="water"];
      way(around:1000, {route['lat']}, {route['lng']})["natural"="water"];
    );
    out tags;
    """
    res = overpass_query(query)
    if res and 'elements' in res:
        print(f"Found {len(res['elements'])} matches:")
        for elem in res['elements'][:15]: # Show first 15
            print(f"  Type: {elem['type']}, ID: {elem['id']}, Tags: {list(elem.get('tags', {}).items())[:5]}")
    else:
        print("No matches or error")
