import json

with open('resolved_elements.json') as f:
    elements = json.load(f)

# Group elements by their cluster or location
# We can load the previous cluster output or recompute it and examine the elements in each cluster
# Let's inspect each cluster and see what facilities are there.

import math
def distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

clusters = []
for el in elements:
    if el.get('municipality') == 'Oslo':
        continue
    lat = el['lat']
    lng = el['lng']
    found = False
    for cluster in clusters:
        if any(distance(lat, lng, member['lat'], member['lng']) < 100 for member in cluster['members']):
            cluster['members'].append(el)
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

print(f"Total clusters: {len(clusters)}")
for idx, c in enumerate(clusters):
    m = c['members'][0]
    muni = m['municipality']
    addr = m['resolved_address']
    tags_list = [memb['tags'] for m in c['members'] for memb in [m]] # just unique tags
    print(f"\nCluster {idx+1}: {muni} | Coords: {c['lat']}, {c['lng']}")
    print(f"  Address: {addr}")
    print(f"  Tags: {json.dumps([me['tags'] for me in c['members']], indent=2)}")
    print(f"  IDs: {[(me['type'], me['id']) for me in c['members']]}")
