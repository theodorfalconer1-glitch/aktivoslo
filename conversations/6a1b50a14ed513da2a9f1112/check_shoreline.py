import xml.etree.ElementTree as ET

tree = ET.parse('lutvann.osm')
root = tree.getroot()

nodes = {}
for n in root.findall('node'):
    nodes[n.attrib['id']] = (float(n.attrib['lat']), float(n.attrib['lon']))

for w in root.findall('way'):
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    if tags.get('natural') == 'water' or tags.get('water') == 'lake' or 'Lutvann' in tags.get('name', ''):
        print(f"Way {w.attrib['id']}: name={tags.get('name')}")
    if tags.get('natural') == 'cliff':
        print(f"Cliff way {w.attrib['id']}:")
        nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
        for ref in nd_refs:
            if ref in nodes:
                print(f"   node {ref}: {nodes[ref][0]:.6f}, {nodes[ref][1]:.6f}")

for r in root.findall('relation'):
    tags = {t.attrib['k']: t.attrib['v'] for t in r.findall('tag')}
    if 'Lutvann' in tags.get('name', ''):
        print(f"Relation {r.attrib['id']}: tags={tags}")

