import sys
import json
import time
import math
import urllib.request
import urllib.parse

places = [
    {"id": "p80", "name": "Discgolf Sognsvann", "lat": 59.9752, "lng": 10.72909},
    {"id": "bt11", "name": "Bordtennis Sognsvann", "lat": 59.9663, "lng": 10.7206},
    {"id": "bt20", "name": "Bordtennis Kampen Park", "lat": 59.915, "lng": 10.77909},
    {"id": "bk2", "name": "Tøyenparken Basketballbane", "lat": 59.9131, "lng": 10.775},
    {"id": "park_middelalder", "name": "Middelalderparken", "lat": 59.904, "lng": 10.7598},
    {"id": "bp_tjuvholmen", "name": "Tjuvholmen sjøbad", "lat": 59.9065, "lng": 10.721},
    {"id": "bp_operastranda", "name": "Operastranda", "lat": 59.907, "lng": 10.753},
    {"id": "bp_frysja", "name": "Frysja badeplass", "lat": 59.9664, "lng": 10.781},
    {"id": "p100", "name": "Holmenkollen utsikt", "lat": 59.962, "lng": 10.6673},
    {"id": "p103", "name": "Stovnertårnet", "lat": 59.9503, "lng": 10.916},
    {"id": "p104", "name": "Torshovdalen øvre utsikt", "lat": 59.935, "lng": 10.7777},
    {"id": "p105", "name": "St. Hanshaugen toppunkt", "lat": 59.9279, "lng": 10.739},
    {"id": "p136", "name": "Deichman Bjørvika skøyteis", "lat": 59.909, "lng": 10.7504},
    {"id": "p141", "name": "Torshovdalen skøyteis", "lat": 59.935, "lng": 10.7777},
    {"id": "bb161", "name": "Sofienbergparken balløkke", "lat": 59.921, "lng": 10.763},
    {"id": "bb162", "name": "Torshovdalen balløkke", "lat": 59.9368, "lng": 10.768},
    {"id": "museum_oslofjord", "name": "Oslofjordmuseet", "lat": 59.625, "lng": 10.4},
    {"id": "vb_sorenga", "name": "Sørenga sandvolleyball", "lat": 59.9018, "lng": 10.755},
    {"id": "p122", "name": "Skibakketrappa Nydalen", "lat": 59.953, "lng": 10.7668},
    {"id": "p124", "name": "Ilatrappa/Ulvetrappa", "lat": 59.928, "lng": 10.7285}
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def query_nominatim_with_retry(query, retries=5, backoff=3.0):
    encoded_query = urllib.parse.quote(query)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
    headers = {
        'User-Agent': 'AktivOslo-DataVerification/1.0'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    for attempt in range(retries):
        try:
            # Always wait at least 3 seconds before making a request to be extremely respectful
            time.sleep(3.0)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                sleep_time = backoff * (2 ** attempt)
                print(f"Received HTTP 429. Sleeping for {sleep_time:.1f} seconds before retry...")
                time.sleep(sleep_time)
            else:
                print(f"HTTP Error {e.code} for query '{query}': {e.reason}")
                return None
        except Exception as e:
            print(f"Error querying '{query}': {e}")
            return None
    print(f"Max retries exceeded for query '{query}'")
    return None

results = []

for idx, place in enumerate(places):
    print(f"Processing {idx+1}/20: {place['name']}...")
    
    # Base query formulation
    if place["id"] == "museum_oslofjord":
        # Oslofjordmuseet is in Asker, so we search without "Oslo" or with "Asker"
        query = "Oslofjordmuseet"
    else:
        query = f"{place['name']} Oslo"
        
    data = query_nominatim_with_retry(query)
    
    if data and len(data) > 0:
        res = data[0]
        new_lat = float(res['lat'])
        new_lng = float(res['lon'])
        
        # Calculate distance between current coordinates and Nominatim's coordinates
        dist = haversine(place['lat'], place['lng'], new_lat, new_lng)
        
        # Check if difference > 300 meters
        changed = dist > 300
        
        # Determine confidence based on importance returned by Nominatim
        importance = float(res.get('importance', 0))
        if importance > 0.6:
            confidence = "high"
        elif importance > 0.3:
            confidence = "medium"
        else:
            confidence = "low"
            
        # If the coordinates are close to the old coordinates, increase confidence
        if dist < 500:
            confidence = "high"
            
        results.append({
            "id": place["id"],
            "name": place["name"],
            "old_lat": place["lat"],
            "old_lng": place["lng"],
            "new_lat": round(new_lat, 6) if changed else place["lat"],
            "new_lng": round(new_lng, 6) if changed else place["lng"],
            "changed": changed,
            "source": "nominatim",
            "confidence": confidence
        })
        print(f"  Found: '{res['display_name']}'")
        print(f"  Result: {new_lat:.6f}, {new_lng:.6f} (dist: {dist:.1f}m) - changed: {changed} (confidence: {confidence})")
    else:
        # Keep current coordinates and mark as 'not_found'
        results.append({
            "id": place["id"],
            "name": place["name"],
            "old_lat": place["lat"],
            "old_lng": place["lng"],
            "new_lat": place["lat"],
            "new_lng": place["lng"],
            "changed": False,
            "source": "not_found",
            "confidence": "low"
        })
        print(f"  Result: Not found in Nominatim")

# Save results to /tmp/verified_coords.json
with open("/tmp/verified_coords.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nAll coordinates processed. Output saved to /tmp/verified_coords.json")
