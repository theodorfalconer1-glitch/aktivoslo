import urllib.request
import urllib.parse
import json
import time

def overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    data = urllib.parse.urlencode({'data': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Base44-Data-Research-Agent/1.0'})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"Rate limited (429). Waiting {5 * (attempt + 1)} seconds and retrying...")
                time.sleep(5 * (attempt + 1))
            else:
                print(f"HTTP Error {e.code}: {e.reason}")
                return None
        except Exception as e:
            print(f"Error querying Overpass: {e}")
            return None
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

# Let's search for each route with customized queries to find relations or ways
# We sleep 2s between queries to avoid rate limit
for r in routes_info:
    print(f"\n==================== SEARCHING: {r['name']} ====================")
    # Search for:
    # - relations with route=hiking/running/foot containing name keywords
    # - relations with leisure=park / water=lake containing name keywords
    # - ways with leisure=park / water=lake containing name keywords
    kw = r['name'].split()[0].replace("-", " ") # first word
    if r['id'] == 'bygdoy_runden':
        kw = "Bygdøy"
    elif r['id'] == 'frognerkilen_tjuvholmen':
        kw = "Frognerkilen"
    
    query = f"""
    [out:json];
    (
      relation(around:1500, {r['lat']}, {r['lng']})["route"~"running|hiking|foot|walking",i];
      relation(around:1500, {r['lat']}, {r['lng']})["name"~"{kw}",i];
      way(around:1000, {r['lat']}, {r['lng']})["name"~"{kw}",i]["leisure"="park"];
      way(around:1000, {r['lat']}, {r['lng']})["name"~"{kw}",i]["natural"="water"];
      relation(around:1500, {r['lat']}, {r['lng']})["name"~"{kw}",i]["natural"="water"];
    );
    out tags;
    """
    res = overpass_query(query)
    if res and 'elements' in res:
        print(f"Found {len(res['elements'])} results:")
        for elem in res['elements'][:15]:
            t = elem.get('tags', {})
            print(f"  - {elem['type'].upper()} ID={elem['id']}: name='{t.get('name')}', route='{t.get('route')}', type='{t.get('type')}', leisure='{t.get('leisure')}', natural='{t.get('natural') or t.get('water')}'")
    else:
        print("  No results found.")
    time.sleep(2)
