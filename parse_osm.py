import urllib.request
import json
import time

elements = [
{"id": 3464038364, "type": "node", "lat": 59.9264917, "lng": 10.6180428, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 10303422907, "type": "node", "lat": 59.8688825, "lng": 10.4819903, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 11111250763, "type": "node", "lat": 59.8849786, "lng": 10.5353978, "tags": {"leisure": "fitness_station"}},
{"id": 11605785338, "type": "node", "lat": 59.8916976, "lng": 10.6079909, "tags": {"fitness_station": "horizontal_ladder", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 11605785339, "type": "node", "lat": 59.8915554, "lng": 10.6081131, "tags": {"fitness_station": "parallel_bars", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 11605785340, "type": "node", "lat": 59.8914668, "lng": 10.6081775, "tags": {"fitness_station": "push-up", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 11608864334, "type": "node", "lat": 59.8351723, "lng": 10.427227, "tags": {"fitness_station": "stairs", "leisure": "fitness_station", "sport": "fitness", "wheelchair": "no"}},
{"id": 12163025146, "type": "node", "lat": 59.8839104, "lng": 10.5423173, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 12351017047, "type": "node", "lat": 59.7780599, "lng": 10.4865321, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 12463936635, "type": "node", "lat": 59.9367143, "lng": 10.6025635, "tags": {"fitness_station": "horizontal_ladder", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 12463936636, "type": "node", "lat": 59.9367261, "lng": 10.6026635, "tags": {"fitness_station": "parallel_bars", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 12463936637, "type": "node", "lat": 59.9366972, "lng": 10.6026307, "tags": {"fitness_station": "yes", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 12544098756, "type": "node", "lat": 59.9325961, "lng": 10.4813393, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13056666797, "type": "node", "lat": 59.9077499, "lng": 10.6121056, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13359192694, "type": "node", "lat": 59.910266, "lng": 10.4972718, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643896, "type": "node", "lat": 59.9228581, "lng": 10.5858363, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643897, "type": "node", "lat": 59.922835, "lng": 10.5858918, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643898, "type": "node", "lat": 59.9227609, "lng": 10.5860643, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643899, "type": "node", "lat": 59.9227338, "lng": 10.5861275, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643900, "type": "node", "lat": 59.9227018, "lng": 10.5859465, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643901, "type": "node", "lat": 59.9226524, "lng": 10.5860743, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13435643902, "type": "node", "lat": 59.9226045, "lng": 10.5861976, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13436088575, "type": "node", "lat": 59.9250491, "lng": 10.5723908, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13436088576, "type": "node", "lat": 59.9250681, "lng": 10.5724557, "tags": {"fitness_station": "horizontal_bar", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 13653202689, "type": "node", "lat": 59.9059975, "lng": 10.5085978, "tags": {"fitness_station": "parallel_bars", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 13653202690, "type": "node", "lat": 59.9058999, "lng": 10.5086009, "tags": {"fitness_station": "horizontal_ladder", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 13653202691, "type": "node", "lat": 59.9059534, "lng": 10.5087114, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 13868663556, "type": "node", "lat": 59.9009955, "lng": 10.525477, "tags": {"fitness_station": "horizontal_ladder", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 13868663557, "type": "node", "lat": 59.9009502, "lng": 10.5255003, "tags": {"fitness_station": "horizontal_bar", "leisure": "fitness_station", "sport": "fitness"}},
{"id": 13990214896, "type": "node", "lat": 59.8300943, "lng": 10.4035326, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 685033983, "type": "way", "lat": 59.9101355, "lng": 10.6114894, "tags": {"leisure": "fitness_station", "source": "Norge i Bilder", "sport": "fitness"}},
{"id": 796545131, "type": "way", "lat": 59.9139026, "lng": 10.5063984, "tags": {"leisure": "fitness_station"}},
{"id": 807327337, "type": "way", "lat": 59.9049208, "lng": 10.6221509, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 852330597, "type": "way", "lat": 59.9540502, "lng": 10.6477989, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 890128939, "type": "way", "lat": 59.9087817, "lng": 10.4992833, "tags": {"leisure": "fitness_station", "lit": "yes"}},
{"id": 890128940, "type": "way", "lat": 59.9084737, "lng": 10.4992933, "tags": {"leisure": "fitness_station", "sport": "parkour"}},
{"id": 917832923, "type": "way", "lat": 59.823187, "lng": 10.4435555, "tags": {"fitness_station": "yes", "leisure": "fitness_station", "name": "Tufteparken Risenga", "sport": "fitness"}},
{"id": 971649662, "type": "way", "lat": 59.7873151, "lng": 10.4430887, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 972252494, "type": "way", "lat": 59.9303124, "lng": 10.4741317, "tags": {"leisure": "fitness_station"}},
{"id": 1020208049, "type": "way", "lat": 59.9601443, "lng": 10.6110075, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 1060530730, "type": "way", "lat": 59.8521778, "lng": 10.4809982, "tags": {"leisure": "fitness_station", "name": "Tufteparken Holmen idrettspark", "sport": "fitness"}},
{"id": 1248328804, "type": "way", "lat": 59.888722, "lng": 10.5960694, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 1248330390, "type": "way", "lat": 59.8971182, "lng": 10.6128142, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 1250027627, "type": "way", "lat": 59.8958025, "lng": 10.6109833, "tags": {"leisure": "fitness_station", "sport": "fitness"}},
{"id": 1413199312, "type": "way", "lat": 59.9299488, "lng": 10.4816272, "tags": {"leisure": "fitness_station"}},
{"id": 1465306868, "type": "way", "lat": 59.9049712, "lng": 10.5706678, "tags": {"leisure": "fitness_station", "sport": "fitness"}}
]

results = []
for idx, el in enumerate(elements):
    lat = el['lat']
    lng = el['lng']
    # Query nominatim reverse
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=18"
    req = urllib.request.Request(url, headers={'User-Agent': 'AktivOslo/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            address = data.get('address', {})
            muni = address.get('municipality', address.get('city_district', address.get('city', address.get('town', address.get('suburb', '')))))
            road = address.get('road', '')
            postcode = address.get('postcode', '')
            city = address.get('city', address.get('town', address.get('village', address.get('suburb', ''))))
            full_address = f"{road}, {postcode} {city}".strip(", ")
            print(f"{idx+1}/{len(elements)}: ID {el['id']} ({el['tags'].get('name', 'no name')}) -> Municipality: {muni} | Address: {full_address}")
            el['resolved_address'] = data.get('display_name')
            el['municipality'] = muni
            el['postcode'] = postcode
            el['road'] = road
            el['city'] = city
            results.append(el)
    except Exception as e:
        print(f"Error for {el['id']}: {e}")
    time.sleep(1.2)

with open('resolved_elements.json', 'w') as f:
    json.dump(results, f, indent=2)
