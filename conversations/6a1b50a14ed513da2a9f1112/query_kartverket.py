import urllib.request
import json

# Let's query Kartverket API for stedsnavn / elevation or features around 59.9116, 10.8773
url = "https://api.kartverket.no/stedsnavn/v1/punkt?nord=59.9116&ost=10.8773&koordsys=4258&radius=500"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Kartverket stedsnavn near Lutvann 59.9116, 10.8773:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Kartverket error:", e)

# Also check Østernvann 59.9686, 10.5867
url_o = "https://api.kartverket.no/stedsnavn/v1/punkt?nord=59.9686&ost=10.5867&koordsys=4258&radius=500"
req_o = urllib.request.Request(url_o, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req_o) as resp:
        data_o = json.loads(resp.read().decode('utf-8'))
        print("\nKartverket stedsnavn near Østernvann 59.9686, 10.5867:")
        print(json.dumps(data_o, indent=2, ensure_ascii=False))
except Exception as e:
    print("Kartverket error:", e)

