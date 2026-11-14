#!/usr/bin/env python3
"""Scrape NephroPlus Philippines clinic list from nephroplus.ph city listing pages
(/our-clinics/<city>), city slugs taken from the live sitemap. Output: raw/operators/nephroplus/nephroplus_branches.json"""
import re, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fetch import get
from bs4 import BeautifulSoup as B
sm = open('raw/operators/nephroplus/nephroplus_ph_sitemap_live.xml').read()
locs = re.findall(r'<loc>([^<]+)</loc>', sm)
cities = sorted({u.split('/')[4] for u in locs if re.search(r'/(our-)?clinics/[^/]+', u) and len(u.split('/'))>4})
out = []
for c in cities:
    url = f'https://nephroplus.ph/our-clinics/{c}'
    p = f'raw/operators/nephroplus/city_{c}.html'
    if os.path.exists(p): html = open(p).read()
    else:
        r, st = get(url, 'operators/nephroplus', f'city_{c}.html', delay=1.5)
        if st != 200: print(c, st); continue
        html = r.text
    s = B(html, 'lxml')
    for a in s.find_all('a', href=re.compile(r'^/our-clinics/[^/]+/[^/]+$')):
        h3 = a.find('h3'); ad = a.find('address')
        out.append({'city_slug': c, 'href': 'https://nephroplus.ph' + a['href'], 'name': h3.get_text(' ',strip=True) if h3 else '',
                    'address': ad.get_text(' ',strip=True) if ad else '', 'list_url': url})
    print(c, sum(1 for o in out if o['city_slug']==c))
seen=set(); ded=[]
for o in out:
    if o['href'] in seen: continue
    seen.add(o['href']); ded.append(o)
json.dump(ded, open('raw/operators/nephroplus/nephroplus_branches.json','w'), indent=1, ensure_ascii=False)
print(len(ded))
