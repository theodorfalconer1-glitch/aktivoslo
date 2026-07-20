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

# Let's test a simple query
# Search for relations/ways near Sognsvann (lat=59.9752, lng=10.7291)
query = """
[out:json];
(
  relation["route"="running"](around:1000, 59.9752, 10.7291);
  relation["route"="foot"](around:1000, 59.9752, 10.7291);
  way["name"~"Sognsvann rundt",i];
  relation["name"~"Sognsvann rundt",i];
);
out tags;
"""
res = overpass_query(query)
print(json.dumps(res, indent=2))
