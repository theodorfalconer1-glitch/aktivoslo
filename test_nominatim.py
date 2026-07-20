import sys
import json
import urllib.request
import urllib.parse
import time

test_queries = [
    "Discgolf Sognsvann",
    "Sognsvann frisbeegolf",
    "Sognsvann discgolf",
    "Bordtennis Sognsvann",
    "Bordtennis Kampen Park",
    "Kampen Park bordtennis",
    "Tøyenparken Basketballbane",
    "Tøyenparken basketball",
    "Frysja badeplass",
    "Frysja",
    "Holmenkollen utsikt",
    "Holmenkollen",
    "Torshovdalen øvre utsikt",
    "Torshovdalen",
    "St. Hanshaugen toppunkt",
    "St. Hanshaugen",
    "Deichman Bjørvika skøyteis",
    "Deichman Bjørvika",
    "Torshovdalen skøyteis",
    "Sofienbergparken balløkke",
    "Sofienbergparken",
    "Torshovdalen balløkke",
    "Sørenga sandvolleyball",
    "Skibakketrappa Nydalen",
    "Skibakketrappa",
    "Ilatrappa",
    "Ulvetrappa",
    "Ilatrappa/Ulvetrappa"
]

headers = {'User-Agent': 'AktivOslo-DataVerification/1.0'}

for q in test_queries:
    encoded_query = urllib.parse.quote(q + " Oslo")
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(1.0)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data:
                print(f"Query: '{q} Oslo' -> Found: '{data[0]['display_name']}' at ({data[0]['lat']}, {data[0]['lon']})")
            else:
                # try without Oslo
                time.sleep(1.0)
                encoded_query_no_oslo = urllib.parse.quote(q)
                url_no_oslo = f"https://nominatim.openstreetmap.org/search?q={encoded_query_no_oslo}&format=json&limit=1"
                req_no_oslo = urllib.request.Request(url_no_oslo, headers=headers)
                with urllib.request.urlopen(req_no_oslo) as resp_no_oslo:
                    data_no_oslo = json.loads(resp_no_oslo.read().decode())
                    if data_no_oslo:
                        print(f"Query: '{q}' -> Found: '{data_no_oslo[0]['display_name']}' at ({data_no_oslo[0]['lat']}, {data_no_oslo[0]['lon']})")
                    else:
                        print(f"Query: '{q}' -> NOT FOUND")
    except Exception as e:
        print(f"Error for '{q}': {e}")
