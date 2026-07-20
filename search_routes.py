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

# Let's search for relations matching any of the names in Oslo
query = """
[out:json][timeout:180];
(
  relation["name"~"Slottsparken|Bygdøy|Bogstadvannet|Akerselva|Nøklevann|Sognsvann|Maridalsvannet|Frognerparken|Frognerkilen|Tjuvholmen|Østensjøvannet",i];
  way["name"~"Slottsparken|Bygdøy|Bogstadvannet|Akerselva|Nøklevann|Sognsvann|Maridalsvannet|Frognerparken|Frognerkilen|Tjuvholmen|Østensjøvannet",i]["route"="running"];
  way["name"~"Slottsparken|Bygdøy|Bogstadvannet|Akerselva|Nøklevann|Sognsvann|Maridalsvannet|Frognerparken|Frognerkilen|Tjuvholmen|Østensjøvannet",i]["route"="hiking"];
);
out tags;
"""

print("Running search query for all keywords...")
res = overpass_query(query)
if res and 'elements' in res:
    print(f"Found {len(res['elements'])} matching relations/ways:")
    for elem in res['elements']:
        tags = elem.get('tags', {})
        print(f"- Type: {elem['type']}, ID: {elem['id']}, Name: {tags.get('name')}, Route: {tags.get('route')}, Type_tag: {tags.get('type')}, Leisure: {tags.get('leisure')}, Natural: {tags.get('natural') or tags.get('water')}")
else:
    print("No results or error.")
