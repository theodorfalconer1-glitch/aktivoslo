import subprocess
import json
import re
import urllib.parse

urls_to_verify = [
    {"club_name": "Grefsen Tennisklubb", "url": "https://www.grefsentennis.no"},
    {"club_name": "Tåsen Tennisklubb", "url": "https://www.tasentennis.no"},
    {"club_name": "IL Heming Tennis", "url": "https://www.heming.no/tennis"},
    {"club_name": "Ullern TK", "url": "https://www.ullerntennis.no"},
    {"club_name": "Nordstrand TK", "url": "https://www.nordstrandtennis.no"},
    {"club_name": "Vestre Bærum TK", "url": "https://www.vbtk.no"},
    {"club_name": "Blommenholm/Sandvika TK", "url": "https://www.bstk.no"},
    {"club_name": "Asker TK", "url": "https://www.askertennis.no"},
    {"club_name": "Stabekk TK", "url": "https://www.stabekktennis.no"},
    {"club_name": "Frogner Tennis", "url": "https://www.frognertennis.no"},
    {"club_name": "Oslo Tennisklubb", "url": "https://www.oslotennis.no"},
    {"club_name": "Njård Tennis", "url": "https://tennis.njaard.no"},
    {"club_name": "Oslo Tennisarena", "url": "https://www.oslotennisarena.no"},
    {"club_name": "Oppsal IL", "url": "https://www.oppsal.no", "check_section": True},
    {"club_name": "Holmenkollen TK alternative 1", "url": "https://www.holmenkollen-tk.no"},
    {"club_name": "Holmenkollen TK alternative 2", "url": "https://www.htkoslo.no"},
    {"club_name": "Bekkestua TK alternative", "url": "https://www.bekkestua-tk.no"},
    {"club_name": "Bækkelaget TK alternative 1", "url": "https://www.bakkelagettennis.no"},
    {"club_name": "Bækkelaget TK alternative 2", "url": "https://btk.no"},
    {"club_name": "Sinsen TK", "url": "https://www.sinsen-tk.no"}
]

results = []

def verify_url(club_name, url, check_section=False):
    print(f"Verifying {club_name}: {url}")
    # run first command: curl -sIL --max-time 8 "URL" | grep -E '^HTTP|^Location' | head -3
    cmd1 = f'curl -sIL --max-time 8 "{url}" | grep -E \'^HTTP|^Location\' | head -3'
    # run second command: curl -sL --max-time 8 "URL" | grep -i \'<title\' | head -1
    cmd2 = f'curl -sL --max-time 8 "{url}" | grep -i \'<title\' | head -1'
    
    p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout1, stderr1 = p1.communicate()
    out1 = stdout1.decode('utf-8', errors='ignore').strip()
    
    p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout2, stderr2 = p2.communicate()
    out2 = stdout2.decode('utf-8', errors='ignore').strip()
    
    # parse status
    http_status = None
    # Look for last HTTP status line in case of redirects
    http_lines = [line for line in out1.split('\n') if line.startswith('HTTP/')]
    if http_lines:
        last_http_line = http_lines[-1]
        m = re.search(r'HTTP/\S+\s+(\d+)', last_http_line)
        if m:
            http_status = int(m.group(1))
            
    # If http_status is None, maybe there was no redirect and we just have one HTTP line, or we can check the first line
    if http_status is None and out1:
        m = re.search(r'HTTP/\S+\s+(\d+)', out1)
        if m:
            http_status = int(m.group(1))
            
    # parse title
    title = ""
    if out2:
        # Extract content between <title> and </title> or just use grep result trimmed
        m_title = re.search(r'<title[^>]*>(.*?)</title>', out2, re.IGNORECASE)
        if m_title:
            title = m_title.group(1).strip()
        else:
            # Clean HTML tags if any or just keep out2
            title = re.sub('<[^<]+?>', '', out2).strip()
            
    valid = False
    notes = ""
    if http_status and 200 <= http_status < 400:
        valid = True
    else:
        notes = f"HTTP Status {http_status}" if http_status else "Failed to connect"
        
    if check_section and valid:
        # Check if they have tennis section
        # Fetch page source and check if 'tennis' is mentioned
        cmd_src = f'curl -sL --max-time 8 "{url}"'
        p_src = subprocess.Popen(cmd_src, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        src_out, _ = p_src.communicate()
        src_text = src_out.decode('utf-8', errors='ignore').lower()
        if 'tennis' in src_text:
            notes = "Oppsal IL has tennis section (found 'tennis' in source code)"
        else:
            valid = False
            notes = "Oppsal IL has website but no apparent tennis section in main page source code"
            
    return {
        "club_name": club_name,
        "url": url,
        "http_status": http_status,
        "page_title": title if title else None,
        "valid": valid,
        "notes": notes if notes else None,
        "raw_headers": out1,
        "raw_title_line": out2
    }

for item in urls_to_verify:
    res = verify_url(item["club_name"], item["url"], item.get("check_section", False))
    results.append(res)
    
print(json.dumps(results, indent=2))
with open('initial_results.json', 'w') as f:
    json.dump(results, f, indent=2)
