#!/usr/bin/env python3
"""ClinicFinderPH: take clinic URLs from the public sitemaps whose slug matches dialysis/renal/kidney/nephro,
fetch each page (robots: Allow /), parse schema.org MedicalClinic JSON-LD.
Output raw/directories/clinicfinderph/clinicfinderph_dialysis.json"""
import re, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fetch import get
urls = [u.strip() for u in open('raw/directories/clinicfinderph/dialysis_urls.txt') if '/clinic/' in u]
out = []
for u in urls:
    slug = u.rstrip('/').split('/')[-1]
    p = f'raw/directories/clinicfinderph/pages/{slug}.html'
    if os.path.exists(p): h = open(p).read()
    else:
        r, st = get(u, 'directories/clinicfinderph/pages', f'{slug}.html', delay=1.2)
        if st != 200: print('ERR', u, st); continue
        h = r.text
    rec = {'url': u}
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: j = json.loads(m)
        except Exception: continue
        if isinstance(j.get('address'), dict) and j.get('@type') not in ('Organization','WebSite'):  # MedicalClinic, Optician, Dentist... (site mis-types many)
            a = j.get('address', {}); g = j.get('geo', {})
            rec.update(name=j.get('name',''), street=a.get('streetAddress',''), city=a.get('addressLocality',''),
                       province=a.get('addressRegion',''), phone=j.get('telephone',''), lat=g.get('latitude',''), lon=g.get('longitude',''),
                       hours='; '.join(f"{o.get('dayOfWeek')} {o.get('opens')}-{o.get('closes')}" for o in j.get('openingHoursSpecification',[])))
        if j.get('@type') == 'BreadcrumbList':
            rec['category'] = ' > '.join(i['name'] for i in j['itemListElement'][1:-1])
    out.append(rec)
json.dump(out, open('raw/directories/clinicfinderph/clinicfinderph_dialysis.json','w'), indent=1, ensure_ascii=False)
print(len(out))
