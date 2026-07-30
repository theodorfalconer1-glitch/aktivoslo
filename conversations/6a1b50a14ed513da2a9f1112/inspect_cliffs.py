import xml.etree.ElementTree as ET

def get_nodes(root):
    nodes = {}
    for node in root.findall('node'):
        nid = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        nodes[nid] = (lat, lon)
    return nodes

def inspect_file(filename):
    print(f"\n==================== {filename} ====================")
    tree = ET.parse(filename)
    root = tree.getroot()
    nodes = get_nodes(root)
    
    for way in root.findall('way'):
        tags = {tag.attrib['k']: tag.attrib['v'] for tag in way.findall('tag')}
        nd_refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        
        # Check if way is cliff, beach, dam, etc.
        if any(k in tags for k in ['natural', 'waterway', 'man_made', 'leisure', 'tourism']):
            print(f"\nWay ID {way.attrib['id']}: tags={tags}")
            coords = [nodes[ref] for ref in nd_refs if ref in nodes]
            if coords:
                min_lat = min(c[0] for c in coords)
                max_lat = max(c[0] for c in coords)
                min_lon = min(c[1] for c in coords)
                max_lon = max(c[1] for c in coords)
                avg_lat = sum(c[0] for c in coords) / len(coords)
                avg_lon = sum(c[1] for c in coords) / len(coords)
                print(f"   Nodes count: {len(coords)}")
                print(f"   Avg coord: lat={avg_lat:.6f}, lon={avg_lon:.6f}")
                print(f"   Bounding box: lat {min_lat:.6f}..{max_lat:.6f}, lon {min_lon:.6f}..{max_lon:.6f}")
                for i, c in enumerate(coords[:5]):
                    print(f"     node {nd_refs[i]}: {c[0]:.6f}, {c[1]:.6f}")

inspect_file('lutvann.osm')
inspect_file('osternvann.osm')
