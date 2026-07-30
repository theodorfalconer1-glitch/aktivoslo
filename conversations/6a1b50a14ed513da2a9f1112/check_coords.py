import xml.etree.ElementTree as ET
import math

def distance(lat1, lon1, lat2, lon2):
    R = 6371000 # radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.sin(phi2/2)**2 # wait, standard haversine formula
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

tree = ET.parse('lutvann.osm')
root = tree.getroot()

target_lat = 59.9116
target_lon = 10.8773

print(f"Target: {target_lat}, {target_lon}")

nodes = {}
for node in root.findall('node'):
    nid = node.attrib['id']
    lat = float(node.attrib['lat'])
    lon = float(node.attrib['lon'])
    nodes[nid] = (lat, lon)
    d = distance(target_lat, target_lon, lat, lon)
    if d < 150: # within 150 meters
        tags = {tag.attrib['k']: tag.attrib['v'] for tag in node.findall('tag')}
        print(f"Node {nid}: lat={lat:.6f}, lon={lon:.6f}, dist={d:.1f}m, tags={tags}")

for way in root.findall('way'):
    tags = {tag.attrib['k']: tag.attrib['v'] for tag in way.findall('tag')}
    nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
    coords = [nodes[ref] for ref in nd_refs if ref in nodes]
    if coords:
        min_d = min(distance(target_lat, target_lon, c[0], c[1]) for c in coords)
        if min_d < 150:
            print(f"Way {way.attrib['id']}: min_dist={min_d:.1f}m, tags={tags}")

