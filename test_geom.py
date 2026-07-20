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
        print(f"Error: {e}")
        return None

query = """
[out:json];
relation(2910680);
out geom;
"""
res = overpass_query(query)
if res and 'elements' in res:
    elem = res['elements'][0]
    print(f"Type: {elem['type']}, ID: {elem['id']}")
    print(f"Tags: {elem.get('tags')}")
    members = elem.get('members', [])
    print(f"Number of members: {len(members)}")
    if members:
        print(f"First member keys: {members[0].keys()}")
        if 'geometry' in members[0]:
            print(f"First member geometry length: {len(members[0]['geometry'])}")
            print(f"First member geometry points: {members[0]['geometry'][:3]}")
else:
    print("No elements.")
