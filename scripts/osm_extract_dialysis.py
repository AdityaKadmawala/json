#!/usr/bin/env python3
"""Extract dialysis-related OSM features from a Philippines .osm.pbf extract.
Criteria: healthcare=dialysis, healthcare:speciality~dialysis|nephrology, amenity=dialysis,
or any name/name:*/operator/brand/description matching dialysis|renal|kidney|nephro|hemodialysis.
usage: osm_extract_dialysis.py PBF raw/geo/osm_dialysis_all_unfiltered.csv ACCESS_DATE"""
import sys, re, csv, osmium
PAT = re.compile(r'dialys|renal|kidney|nephro|hemodial|haemodial|diálisis', re.I)
KEYS_NAME = ('name','name:en','official_name','alt_name','old_name','operator','brand','description','short_name')
def hit(t):
    hc = t.get('healthcare',''); sp = t.get('healthcare:speciality','')
    if hc == 'dialysis' or t.get('amenity') == 'dialysis' or re.search(r'dialysis|nephrolog', sp): return True
    return any(PAT.search(t.get(k,'')) for k in KEYS_NAME)
rows = []
class H(osmium.SimpleHandler):
    def node(self, n):
        if n.tags and hit(n.tags): rows.append(('node', n.id, n.location.lat, n.location.lon, dict(n.tags)))
    def way(self, w):
        if w.tags and hit(w.tags):
            try:
                pts=[(nd.lat,nd.lon) for nd in w.nodes if nd.location.valid()]
                lat=sum(p[0] for p in pts)/len(pts); lon=sum(p[1] for p in pts)/len(pts)
            except Exception: lat=lon=''
            rows.append(('way', w.id, lat, lon, dict(w.tags)))
    def relation(self, r):
        if r.tags and hit(r.tags): rows.append(('relation', r.id, '', '', dict(r.tags)))
H().apply_file(sys.argv[1], locations=True, idx='flex_mem')
cols = ['osm_type','osm_id','name','lat','lon','amenity','healthcare','healthcare_speciality','operator','brand',
        'addr_housenumber','addr_street','addr_barangay','addr_city','addr_province','addr_postcode','addr_full',
        'phone','website','opening_hours','email','dialysis_match_reason','source_url','access_date','all_tags']
with open(sys.argv[2],'w',newline='') as f:
    w = csv.writer(f); w.writerow(cols)
    for typ,i,lat,lon,t in sorted(rows,key=lambda r:(r[0],r[1])):
        reason = 'tag' if (t.get('healthcare')=='dialysis' or t.get('amenity')=='dialysis' or re.search('dialysis|nephrolog',t.get('healthcare:speciality',''))) else 'name/operator regex'
        g=lambda k: t.get(k,'')
        w.writerow([typ,i,g('name'),f"{lat:.7f}" if lat!='' else '',f"{lon:.7f}" if lon!='' else '',g('amenity'),g('healthcare'),
            g('healthcare:speciality'),g('operator'),g('brand'),g('addr:housenumber'),g('addr:street'),
            g('addr:suburb') or g('addr:village') or g('addr:barangay'),g('addr:city') or g('addr:municipality') or g('addr:town'),
            g('addr:province') or g('addr:state'),g('addr:postcode'),g('addr:full'),g('phone') or g('contact:phone'),
            g('website') or g('contact:website') or g('contact:facebook'),g('opening_hours'),g('email') or g('contact:email'),reason,
            f"https://www.openstreetmap.org/{typ}/{i}",sys.argv[3] if len(sys.argv)>3 else '',
            ';'.join(f"{k}={v}" for k,v in sorted(t.items()))])
print(len(rows))
