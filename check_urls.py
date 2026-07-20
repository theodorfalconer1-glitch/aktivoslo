import subprocess
import json
import re
import urllib.parse

urls = [
    # MUSEUMS
    {"url": "https://www.nasjonalmuseet.no/", "expected": "Nasjonalmuseet Oslo", "category": "MUSEUMS"},
    {"url": "https://www.munch.no/", "expected": "Munchmuseet", "category": "MUSEUMS"},
    {"url": "https://www.frammuseum.no/", "expected": "Frammuseet", "category": "MUSEUMS"},
    {"url": "https://www.kon-tiki.no/", "expected": "Kon-Tiki Museet", "category": "MUSEUMS"},
    {"url": "https://norskfolkemuseum.no/", "expected": "Norsk Folkemuseum", "category": "MUSEUMS"},
    {"url": "https://www.nhm.uio.no/", "expected": "Naturhistorisk museum", "category": "MUSEUMS"},
    {"url": "https://www.af-moma.no/", "expected": "Astrup Fearnley Museet", "category": "MUSEUMS"},
    {"url": "https://ibsenmuseet.no/", "expected": "Ibsenmuseet", "category": "MUSEUMS"},
    {"url": "https://hlsenteret.no/", "expected": "Holocaust-senteret", "category": "MUSEUMS"},
    {"url": "https://www.historiskmuseum.no/", "expected": "Historisk museum UiO", "category": "MUSEUMS"},
    {"url": "https://www.nobelpeacecenter.org/", "expected": "Nobels Fredssenter", "category": "MUSEUMS"},
    {"url": "https://www.tekniskmuseum.no/", "expected": "Norsk Teknisk Museum", "category": "MUSEUMS"},
    {"url": "https://www.oslomuseum.no/", "expected": "Oslo Museum / Bymuseet", "category": "MUSEUMS"},
    {"url": "https://www.hok.no/", "expected": "Henie Onstad Kunstsenter", "category": "MUSEUMS"},
    {"url": "https://grinimuseet.no/", "expected": "Grinimuseet", "category": "MUSEUMS"},
    {"url": "https://www.lommedalsbanen.no/", "expected": "Lommedalsbanen", "category": "MUSEUMS"},
    {"url": "https://www.baerumsverk.no/", "expected": "Bærums Verk", "category": "MUSEUMS"},
    {"url": "https://www.askermuseum.no/", "expected": "Asker museum", "category": "MUSEUMS"},
    {"url": "https://www.oslofjordmuseet.no/", "expected": "Oslofjordmuseet", "category": "MUSEUMS"},
    {"url": "https://www.holmsbubadogkunst.no/", "expected": "Holmsbu Bad og Kunstmuseum", "category": "MUSEUMS"},

    # TENNIS CLUBS
    {"url": "https://www.frognertennis.no", "expected": "Frogner Tennis", "category": "TENNIS CLUBS"},
    {"url": "https://www.oslotennisarena.no", "expected": "Oslo Tennisarena", "category": "TENNIS CLUBS"},
    {"url": "https://www.oslotennis.no", "expected": "Oslo Tennisklubb", "category": "TENNIS CLUBS"},
    {"url": "https://www.grefsentennis.no", "expected": "Grefsen TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.njard.no/tennis", "expected": "Njård Tennis", "category": "TENNIS CLUBS"},
    {"url": "https://www.tasentennis.no", "expected": "Tåsen TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.heming.no/tennis", "expected": "IL Heming Tennis", "category": "TENNIS CLUBS"},
    {"url": "https://www.htktennis.no", "expected": "Holmenkollen TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.eiksmarka-tennis.no", "expected": "Eiksmarka/Bekkestua TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.ullerntennis.no", "expected": "Ullern TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.staber.no/tennis", "expected": "Stabekk TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.bakkelaget.no/tennis", "expected": "Bækkelaget TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.nordstrandtennis.no", "expected": "Nordstrand TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.oppsal.no/tennis", "expected": "Oppsal TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.vbtk.no", "expected": "Vestre Bærum TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.bstk.no", "expected": "Blommenholm og Sandvika TK", "category": "TENNIS CLUBS"},
    {"url": "https://www.askertennis.no", "expected": "Asker TK", "category": "TENNIS CLUBS"},

    # BADSTUER / BOOKING
    {"url": "https://koknorge.no", "expected": "KOK Oslo (Langkaia + Aker Brygge)", "category": "BADSTUER / BOOKING"},
    {"url": "https://oslobadstuforening.no", "expected": "Oslo Badstuforening", "category": "BADSTUER / BOOKING"},
    {"url": "https://badstuvogna.no", "expected": "Badstuvogna", "category": "BADSTUER / BOOKING"},
    {"url": "https://kongenmarina.no", "expected": "Kongen Marina Sauna", "category": "BADSTUER / BOOKING"},
    {"url": "https://oslofjordsauna.no", "expected": "Oslo Fjord Sauna (OBF Grefsenkollen)", "category": "BADSTUER / BOOKING"},
    {"url": "https://fjordtokt.no", "expected": "Fjordtokt", "category": "BADSTUER / BOOKING"},
    {"url": "https://saltos.no", "expected": "SALT (current: FEIL — should be salt.no or saltoslo.no)", "category": "BADSTUER / BOOKING"},

    # ALSO CHECK CORRECT SALT URL
    {"url": "https://www.salt.no", "expected": "SALT Oslo cultural venue + sauna?", "category": "SALT CHK"},
    {"url": "https://saltoslo.no", "expected": "SALT Oslo?", "category": "SALT CHK"},
    {"url": "https://www.saltoslo.no", "expected": "SALT Oslo?", "category": "SALT CHK"}
]

def check_url(item):
    url = item["url"]
    expected = item["expected"]
    
    print(f"Checking {url}...")
    # Execute curl -sI --max-time 8 -L "URL"
    # We want to trace redirects as well, but -sI -L with grep is what the prompt specifies.
    # Let's run:
    # curl -sI --max-time 8 -L "URL"
    try:
        res = subprocess.run(
            ["curl", "-sI", "--max-time", "8", "-L", url],
            capture_output=True, text=True, timeout=10
        )
        stdout = res.stdout
        stderr = res.stderr
    except subprocess.TimeoutExpired:
        return {
            "url": url,
            "status": None,
            "final_url": None,
            "page_title": None,
            "matches_expected": False,
            "issue": "Request timed out"
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "final_url": None,
            "page_title": None,
            "matches_expected": False,
            "issue": f"Execution error: {str(e)}"
        }

    # Now we need to parse status and final url.
    # Let's find HTTP status codes.
    # When curl -sI -L is run, it outputs headers for each hop.
    # E.g.:
    # HTTP/1.1 301 Moved Permanently
    # Location: https://...
    #
    # HTTP/2 200
    # ...
    
    lines = stdout.splitlines()
    status_codes = []
    locations = []
    
    for line in lines:
        if line.startswith("HTTP/"):
            # extract status code
            parts = line.split()
            if len(parts) >= 2:
                status_codes.append(parts[1])
        elif line.lower().startswith("location:"):
            loc = line[len("location:"):].strip()
            locations.append(loc)
            
    # Final status code is the last one in the list (or if none, we didn't get any HTTP status)
    status = int(status_codes[-1]) if status_codes else None
    
    # Final URL:
    # How to trace the final URL? If we followed redirects, the final URL can be determined.
    # Alternatively, we can use curl to print the final URL directly!
    # Let's do a separate curl to get the final URL if it redirects, or we can use:
    # curl -Ls -o /dev/null -w %{url_effective} "URL"
    # This is much cleaner and robust. Let's do that to get the actual final URL and final status!
    try:
        final_info = subprocess.run(
            ["curl", "-Ls", "-o", "/dev/null", "-w", "%{url_effective}\\n%{http_code}", "--max-time", "8", url],
            capture_output=True, text=True, timeout=10
        )
        final_lines = final_info.stdout.strip().splitlines()
        if len(final_lines) >= 2:
            final_url = final_lines[0].strip()
            status = int(final_lines[1].strip())
        else:
            final_url = url
    except Exception as e:
        final_url = url
        
    issue = None
    page_title = None
    
    # If final status is not 200 or 3xx (and actually 200 is expected for the final page)
    # The prompt says: "Does it return HTTP 200 (or 301/302 to valid destination)?"
    # If status is 0 or 4xx or 5xx, or if there's any other error:
    is_suspect = (status is None or status < 200 or status >= 400)
    
    # We should get page title anyway, or especially for suspect URLs. Let's try to get it for all or at least suspect ones.
    # To be extremely robust, let's fetch the page title if we can.
    # Fetch page title command:
    # curl -sL --max-time 8 "URL" | grep -i '<title' | head -1
    # Let's run this for suspect URLs or when we need to verify matches_expected.
    # Actually, we can fetch it for all URLs to check if it matches the expected name!
    try:
        title_res = subprocess.run(
            f"curl -sL --max-time 8 \"{url}\" | grep -i '<title' | head -1",
            shell=True, capture_output=True, text=True, timeout=10
        )
        title_line = title_res.stdout.strip()
        # Parse title
        match = re.search(r'<title[^>]*>(.*?)</title>', title_line, re.IGNORECASE)
        if match:
            page_title = match.group(1).strip()
        else:
            # Maybe the title is multi-line or needs a cleaner extraction.
            # Let's do a simple curl of first 100kb and extract title via python regex
            html_res = subprocess.run(
                ["curl", "-sL", "--max-time", "8", url],
                capture_output=True, timeout=10
            )
            # Decode carefully
            html_content = ""
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
                try:
                    html_content = html_res.stdout.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            if match:
                page_title = " ".join(match.group(1).split())
    except Exception as e:
        pass

    # Let's check matches_expected
    matches_expected = False
    if page_title:
        # Check if expected name is in page title (case insensitive)
        # Or if final url makes sense
        clean_expected = expected.lower().replace("museum", "").replace("museet", "").strip()
        # Simple heuristic:
        if clean_expected in page_title.lower() or expected.lower() in page_title.lower():
            matches_expected = True
        elif "oslo" in expected.lower() and "oslo" in page_title.lower():
            # if they both have oslo and some other word
            expected_words = [w for w in expected.lower().split() if len(w) > 3]
            if any(w in page_title.lower() for w in expected_words):
                matches_expected = True
    
    # If no title or regex match, can we verify by domain/final URL?
    if not matches_expected:
        # e.g., if expected "Frogner Tennis" and final_url is frognertennis.no
        domain = urllib.parse.urlparse(final_url).netloc.lower()
        expected_words = [w for w in expected.lower().split() if len(w) > 3]
        if any(w in domain for w in expected_words):
            matches_expected = True

    # Special logic for issues and status
    if status is None or status == 0:
        issue = "Could not resolve host or connection failed"
        status = 0
    elif status >= 400:
        issue = f"Returns HTTP status {status}"
    
    if not matches_expected and not issue:
        # If title doesn't match expected
        issue = f"Page title '{page_title}' or final URL '{final_url}' does not obviously match expected '{expected}'"
        
    return {
        "url": url,
        "status": status,
        "final_url": final_url,
        "page_title": page_title if page_title else "",
        "matches_expected": matches_expected,
        "issue": issue
    }

results = []
for item in urls:
    res = check_url(item)
    results.append(res)

with open("/tmp/url_check_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done checking. Results written to /tmp/url_check_results.json")
