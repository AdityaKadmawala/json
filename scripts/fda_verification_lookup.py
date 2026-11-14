"""Query the public FDA Philippines verification search (https://verification.fda.gov.ph/, JSON endpoint
/api/search?q=...) for operator names, and flatten establishment licence (LTO) hits.
The endpoint is the one the public verification page itself calls; no login or challenge.
Rate-limited (2 s between requests). Raw JSON saved under raw/corporate/fda_verification/.

Usage: python3 -I scripts/fda_verification_lookup.py queries.txt data/corporate/fda_lto_lookups.csv
"""
import csv, json, os, re, sys, time, urllib.parse, urllib.request, datetime

RAW = 'raw/corporate/fda_verification'
LTO_KEYS = ('lto_food', 'lto_drugs', 'lto_medicaldevice', 'lto_healthrelateddevice', 'lto_pco', 'lto_cosmetics')

def main(src, dst, delay=2.0):
    os.makedirs(RAW, exist_ok=True)
    today = datetime.date.today().isoformat()
    qs = [l.strip() for l in open(src, encoding='utf-8') if l.strip() and not l.startswith('#')]
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['query', 'register', 'lto_number', 'establishment_name', 'establishment_owner', 'primary_activity',
                    'additional_activities', 'address', 'region', 'lto_validity', 'status', 'source_url', 'access_date'])
        for q in qs:
            url = 'https://verification.fda.gov.ph/api/search?' + urllib.parse.urlencode({'q': q})
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (research; rate-limited)', 'Accept': 'application/json'})
                with urllib.request.urlopen(req, timeout=40) as r:
                    body = r.read().decode('utf-8', 'ignore')
                d = json.loads(body)
            except Exception as e:
                print('STOP', q, e); break
            open(os.path.join(RAW, re.sub(r'[^A-Za-z0-9]+', '_', q)[:60] + '.json'), 'w', encoding='utf-8').write(body)
            n = 0
            for k in LTO_KEYS:
                for it in d.get(k) or []:
                    w.writerow([q, k, it.get('LTO_NUMBER', ''), it.get('ESTABLISHMENT_NAME', ''), it.get('ESTABLISHMENT_OWNER', ''),
                                it.get('PRIMARY_ACTIVITY', ''), it.get('ADDITIONAL_ACTIVITIES', ''), it.get('ADDRESS', ''),
                                it.get('REGION', ''), it.get('LTO_VALIDITY', ''), it.get('ESTABLISHMENT_STATUS', ''), url, today])
                    n += 1
            if n == 0:
                w.writerow([q, '', '', '', '', '', '', '', '', '', 'no establishment LTO hit', url, today])
            f.flush()
            print(q, '->', n)
            time.sleep(delay)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
