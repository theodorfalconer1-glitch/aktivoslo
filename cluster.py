import json
import math

with open('resolved_elements.json') as f:
    elements = json.load(f)

# Haversine distance formula
def distance(lat1, lon1, lat2, lon2):
    R = 6371000 # radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Cluster elements within 100 meters
clusters = []
for el in elements:
    # Skip Oslo
    if el.get('municipality') == 'Oslo':
        continue
    lat = el['lat']
    lng = el['lng']
    found = False
    for cluster in clusters:
        # Check distance to cluster center or any element in cluster
        if any(distance(lat, lng, member['lat'], member['lng']) < 100 for member in cluster['members']):
            cluster['members'].append(el)
            # Recompute center
            cluster['lat'] = sum(m['lat'] for m in cluster['members']) / len(cluster['members'])
            cluster['lng'] = sum(m['lng'] for m in cluster['members']) / len(cluster['members'])
            found = True
            break
    if not found:
        clusters.append({
            'lat': lat,
            'lng': lng,
            'members': [el]
        })

print(f"Found {len(clusters)} clusters out of {len(elements)} elements.")
for idx, c in enumerate(clusters):
    names = [m['tags'].get('name') for m in c['members'] if m['tags'].get('name')]
    types = [m['tags'].get('fitness_station') for m in c['members'] if m['tags'].get('fitness_station')]
    sports = [m['tags'].get('sport') for m in c['members'] if m['tags'].get('sport')]
    muni = c['members'][0]['municipality']
    addr = c['members'][0]['resolved_address']
    postcode = c['members'][0].get('postcode', '')
    road = c['members'][0].get('road', '')
    city = c['members'][0].get('city', '')
    print(f"\nCluster {idx+1}:")
    print(f"  Muni: {muni}")
    print(f"  Coords: {c['lat']}, {c['lng']}")
    print(f"  Names in cluster: {names}")
    print(f"  Sports: {sports}")
    print(f"  Types: {types}")
    print(f"  Address: {road}, {postcode} {city}")
    print(f"  First Member ID: {c['members'][0]['type']}/{c['members'][0]['id']}")
    print(f"  All IDs: {[m['id'] for m in c['members']]}")
