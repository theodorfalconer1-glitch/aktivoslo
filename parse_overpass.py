import json

with open("overpass_raw.json", "r") as f:
    data = json.load(f)

elements = data.get("elements", [])
print(f"Total elements: {len(elements)}")

# Existing parks to filter out (lowercase strings for matching)
existing_keywords = [
    "frognerbadet",
    "voldsløkka",
    "st. hanshaugen", "geitmyrsveien",
    "marienlyst", "sophus bugges",
    "torshovdalen",
    "filipstad", "skur 13",
    "løren",
    "lambertseter",
    "skullerud",
    "linderud", "naboparken",
    "tåsen",
    "kristparken",
    "tinkern", "framnesveien",
    "kollenparken", "kongeveien 5",
    "forskningsparken", "kollparken",
    "ekeberg",
    "ensjø",
    "bærum idrettspark", "hauger skolevei",
    "kadettangen",
    "vardåsen"
]

named_elements = []
unnamed_elements = []

for el in elements:
    tags = el.get("tags", {})
    name = tags.get("name")
    
    # Coordinates are either 'lat'/'lon' or inside 'center' for ways
    lat = el.get("lat")
    lon = el.get("lon")
    if lat is None or lon is None:
        center = el.get("center", {})
        lat = center.get("lat")
        lon = center.get("lon")
    
    if lat is None or lon is None:
        continue
        
    el_info = {
        "id": el.get("id"),
        "type": el.get("type"),
        "lat": lat,
        "lng": lon,
        "name": name,
        "tags": tags
    }
    
    if name:
        # Check if it matches any existing park
        name_lower = name.lower()
        is_existing = False
        for kw in existing_keywords:
            if kw in name_lower:
                is_existing = True
                break
        
        # Also check other tags for existing keywords just in case
        tags_str = str(tags).lower()
        for kw in existing_keywords:
            if kw in tags_str:
                is_existing = True
                break
                
        if not is_existing:
            named_elements.append(el_info)
    else:
        # Check if any tag matches existing keywords
        tags_str = str(tags).lower()
        is_existing = False
        for kw in existing_keywords:
            if kw in tags_str:
                is_existing = True
                break
        if not is_existing:
            unnamed_elements.append(el_info)

print(f"Named elements (not in existing list): {len(named_elements)}")
print(f"Unnamed elements (not in existing list): {len(unnamed_elements)}")

print("\n--- Named Elements Samples ---")
for el in named_elements[:15]:
    print(f"ID: {el['id']}, Name: {el['name']}, Lat: {el['lat']}, Lng: {el['lng']}")
    print(f"  Tags: {el['tags']}")

print("\n--- Unnamed Elements Samples ---")
for el in unnamed_elements[:5]:
    print(f"ID: {el['id']}, Lat: {el['lat']}, Lng: {el['lng']}")
    print(f"  Tags: {el['tags']}")
