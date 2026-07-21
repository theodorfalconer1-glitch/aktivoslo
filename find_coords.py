import urllib.request
import json
import urllib.parse

locations = [
    "Tufteparken Fornebu",
    "Jarmyra Trimpark",
    "Gjønnesjordet",
    "Helset nærmiljøanlegg",
    "Tufteparken Gjønnesjordet",
    "Oksenøyveien 14",
    "Bærumsveien 106",
    "Bekkestien 11",
    "Nyveien 24 Stabekk",
    "Ankerveien 150 Bærum"
]

for loc in locations:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(loc)}&format=json&countrycodes=no"
    req = urllib.request.Request(url, headers={'User-Agent': 'AktivOslo/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data:
                print(f"Location '{loc}': {data[0]['lat']}, {data[0]['lon']} ({data[0]['display_name']})")
            else:
                print(f"Location '{loc}' not found")
    except Exception as e:
        print(f"Location '{loc}' error: {e}")
