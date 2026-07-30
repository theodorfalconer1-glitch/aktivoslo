import xml.etree.ElementTree as ET

def analyze_osm(filename):
    print(f"=== Analyzing {filename} ===")
    tree = ET.parse(filename)
    root = tree.getroot()
    
    tags_of_interest = []
    
    for elem in root:
        tags = {tag.attrib['k']: tag.attrib['v'] for tag in elem.findall('tag')}
        if not tags:
            continue
        
        # Print elements with relevant tags or names
        name = tags.get('name', '')
        ref = tags.get('ref', '')
        desc = tags.get('description', '')
        note = tags.get('note', '')
        natural = tags.get('natural', '')
        sport = tags.get('sport', '')
        leisure = tags.get('leisure', '')
        tourism = tags.get('tourism', '')
        waterway = tags.get('waterway', '')
        man_made = tags.get('man_made', '')
        
        relevant = False
        if any(k in tags for k in ['natural', 'sport', 'leisure', 'tourism', 'waterway', 'man_made', 'cliff', 'diving', 'swimming']):
            relevant = True
        if any(term in (name + desc + note).lower() for term in ['stup', 'hopp', 'klippe', 'bade', 'dam', 'demning', 'dive', 'cliff', 'jump']):
            relevant = True
            
        if relevant:
            elem_type = elem.tag
            elem_id = elem.attrib.get('id')
            lat = elem.attrib.get('lat', '')
            lon = elem.attrib.get('lon', '')
            if elem_type != 'node':
                # find first node lat/lon if way
                pass
            print(f"[{elem_type} {elem_id}] lat={lat} lon={lon}")
            for k, v in tags.items():
                print(f"   {k} = {v}")

analyze_osm('lutvann.osm')
analyze_osm('osternvann.osm')

