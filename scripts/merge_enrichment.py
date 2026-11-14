"""Merge workstream outputs into the master table.

Run after scripts/build_master.py:
    python3 scripts/merge_enrichment.py
Output: data/dialysis_centers_philippines.csv  (one row per known/candidate dialysis center)
"""
import re
import pandas as pd
from rapidfuzz import fuzz, process
from build_master import norm_name, PROV2REG

M = pd.read_csv('data/master_dialysis_centers.csv', dtype=str).fillna('')
M['coverage_status'] = 'Confirmed: in PhilHealth accredited list (2026-09-30)'
M['lat'] = M['lon'] = M['coord_source'] = ''
M['operator'] = M['operator_parent'] = M['hd_stations'] = M['services'] = M['web_source_urls'] = ''

def city_key(s):
    s = str(s or '').upper().replace('Ñ', 'N')
    if s.endswith(', MANILA'):
        s = 'MANILA'  # district names (Tondo, Paco, ...) -> City of Manila
    s = re.sub(r'\bSTA\.?\s', 'SANTA ', s); s = re.sub(r'\bSTO\.?\s', 'SANTO ', s); s = re.sub(r'\bGEN\.?\s', 'GENERAL ', s)
    s = re.sub(r'\(.*?\)|\bSCIENCE CITY OF\b|\bCITY OF\b|\bCITY\b|\bMUNICIPALITY OF\b', '', s)
    s = {'BALIUAG': 'BALIWAG', 'ZARAGOSA': 'ZARAGOZA', 'PARACELIS PARACALES': 'PARACELIS'}.get(s.strip(), s)
    return re.sub(r'[^A-Z]', '', s)

# ---- 1. operator / chain branches (rows matched to PhilHealth seq) ----
cb = pd.read_csv('data/operators/chain_branches.csv', dtype=str).fillna('')
ops = pd.read_csv('data/operators/operators.csv', dtype=str).fillna('')
parent = dict(zip(ops.operator, ops.parent))
fdc_idx = {r.philhealth_seq: i for i, r in M[M.center_id.str.startswith('FDC')].iterrows()}
for _, b in cb[cb.philhealth_seq != ''].iterrows():
    seq = str(int(float(b.philhealth_seq)))
    i = fdc_idx.get(seq)
    if i is None:
        continue
    M.at[i, 'operator'] = b.operator
    M.at[i, 'operator_parent'] = parent.get(b.operator, '')
    for col in ['hd_stations', 'services']:
        if b[col] and not M.at[i, col]:
            M.at[i, col] = b[col]
    if b.lat and b.lon and not M.at[i, 'lat']:
        M.at[i, 'lat'], M.at[i, 'lon'], M.at[i, 'coord_source'] = b.lat, b.lon, 'operator website'
    if b.source_url and 'philhealth' not in b.source_url:
        M.at[i, 'web_source_urls'] = '; '.join(filter(None, [M.at[i, 'web_source_urls'], b.source_url]))

# ---- 2. OSM coordinates: name match >= 90 within the same municipality ----
osm = pd.read_csv('data/geo/osm_dialysis.csv', dtype=str).fillna('')
osm = osm[(osm.lat != '') & (osm.name != '')]
M['_ck'] = M.municipality.map(city_key)
for _, o in osm.iterrows():
    ck = city_key(o.addr_city)
    pool = M[(M._ck == ck) & (M.lat == '')] if ck else pd.DataFrame()
    if pool.empty:
        continue
    hit = process.extractOne(norm_name(o['name']), pool.name_key.to_dict(), scorer=fuzz.token_set_ratio)
    if hit and hit[1] >= 90:
        i = hit[2]
        M.at[i, 'lat'], M.at[i, 'lon'], M.at[i, 'coord_source'] = o.lat, o.lon, f'OpenStreetMap {o.osm_type}/{o.osm_id}'

# ---- 3. legal / regulatory events, attached by entity name ----
lg = pd.read_csv('data/legal/legal_regulatory_events.csv', dtype=str).fillna('')
M['legal_regulatory_events'] = ''
for _, e in lg[lg.matched_center_name != ''].iterrows():
    for nm in e.matched_center_name.split(';'):
        key = norm_name(nm)
        hits = M.index[M.name_key == key]
        tag = f"{e.event_type} ({e.date[:10]}, {e.finding_level})"
        for i in hits:
            M.at[i, 'legal_regulatory_events'] = '; '.join(filter(None, [M.at[i, 'legal_regulatory_events'], tag]))
M['legal_event_count'] = M.legal_regulatory_events.map(lambda s: len(s.split('; ')) if s else 0)

# ---- 4. candidates not in the freestanding list ----
cand = pd.read_csv('data/operators/not_in_philhealth_candidates.csv', dtype=str).fillna('')
hosp = pd.read_csv('data/philhealth_hospitals_2026-09-30.csv', dtype=str).fillna('')
hosp['name_key'] = hosp.name.map(norm_name)
hosp_keys = hosp.name_key.to_dict()
new = []
for _, c in cand.iterrows():
    key = norm_name(c['name'])
    hh = process.extractOne(key, hosp_keys, scorer=fuzz.token_sort_ratio)
    base = dict(name=c['name'], street=c.address, municipality=c.city, province=c.province.upper(),
                phones=c.phone, lat=c.lat, lon=c.lon, coord_source='candidate sources' if c.lat else '',
                operator=c.operator, hd_stations=c.machines, web_source_urls=c.evidence_urls,
                name_key=key, hd_unit_evidence=f'{c.sources} (n_sources={c.n_sources})', legal_event_count=0)
    if hh and hh[1] >= 92:
        h = hosp.loc[hh[2]]
        if h.category == 'LEVEL 3':
            continue  # already in master as a Level 3 hospital unit
        base.update(center_id=f'HOSP-{int(h.seq):04d}', facility_type='Hospital-based dialysis unit', name=h['name'],
                    street=h.street, municipality=h.municipality, province=h.province, sector=h.sector,
                    philhealth_region=h.region, philhealth_accredited='Yes (as hospital)', philhealth_list='HOSP 2026-09-30',
                    philhealth_seq=h.seq, philhealth_accreditation_expiry=h.accreditation_expiry,
                    hospital_level=h.category, hospital_beds=h.beds, phones=h.tel, emails=h.email,
                    entity_type='government hospital' if h.sector == 'Government' else 'private hospital',
                    coverage_status='Confirmed hospital (PhilHealth) + web evidence of dialysis unit')
    else:
        likely_h = c.likely_hospital_based == 'yes'
        base.update(center_id=f'CAND-{c.candidate_id}',
                    facility_type='Hospital-based dialysis unit (unverified)' if likely_h else 'Dialysis center (unverified)',
                    philhealth_accredited='Not found in PhilHealth lists',
                    coverage_status={'no_match': 'Candidate: not in PhilHealth lists',
                                     'possible_match': f'Candidate: possible duplicate of PhilHealth #{c.best_philhealth_seq} {c.best_philhealth_name} (score {c.best_score})',
                                     'generic_name_unmatched': 'Candidate: generic name, unmatched'}[c.match_status])
    new.append(base)
N = pd.DataFrame(new).drop_duplicates('center_id')
out = pd.concat([M.drop(columns=['_ck']), N], ignore_index=True).fillna('')
out['admin_region'] = [r or PROV2REG.get(str(p).upper(), '') for r, p in zip(out.admin_region, out.province)]

# ---- 5. corporate / ownership (if the workstream produced it) ----
ent = pd.read_csv('data/corporate/entities.csv', dtype=str).fillna('')
ent = ent.set_index(ent.seq.astype(int).astype(str))
for c in ['legal_entity_name', 'operator_entity', 'ultimate_owner', 'group_link_confidence', 'entity_notes']:
    out[c] = ''
for i, r in out[out.center_id.str.startswith('FDC')].iterrows():
    e = ent.loc[str(int(r.philhealth_seq))]
    out.at[i, 'entity_type'] = e.entity_type or r.entity_type
    out.at[i, 'legal_entity_name'] = e.legal_entity_name_guess
    out.at[i, 'operator_entity'] = e.operator_entity
    out.at[i, 'ultimate_owner'] = e.ultimate_owner
    out.at[i, 'group_link_confidence'] = e.group_link_confidence
    out.at[i, 'entity_notes'] = e.notes
    if e.operator_group and not r.operator:
        out.at[i, 'operator'] = e.operator_group

cols = ['center_id', 'coverage_status', 'facility_type', 'name', 'operator', 'operator_parent', 'operator_entity',
        'ultimate_owner', 'group_link_confidence', 'legal_entity_name', 'operator_group', 'operator_group_size', 'entity_type', 'entity_notes', 'sector', 'street', 'municipality', 'province', 'admin_region',
        'lat', 'lon', 'coord_source', 'phones', 'mobile_count', 'emails', 'corporate_email_domain',
        'philhealth_accredited', 'philhealth_list', 'philhealth_seq', 'philhealth_accreditation_expiry',
        'hospital_level', 'hospital_beds', 'hd_stations', 'services', 'legal_event_count', 'legal_regulatory_events',
        'hd_unit_evidence', 'web_source_urls', 'philhealth_region', 'tel_raw', 'email_raw', 'name_key']
out[cols].to_csv('data/dialysis_centers_philippines.csv', index=False)
print(len(out), 'rows'); print(out.coverage_status.str.split(':').str[0].value_counts().to_string())
print(out.facility_type.value_counts().to_string())
print('with coords:', (out.lat != '').sum(), '| with operator:', (out.operator != '').sum(),
      '| with legal events:', (out.legal_event_count.astype(int) > 0).sum(), '| with stations:', (out.hd_stations != '').sum())

# ---- 6. approximate coordinates: municipality centroid of OSM health facilities (HDX, adm3) ----
import json
g = json.load(open('raw/geo/hdx_health/health_facilities.geojson'))
pts = []
for f in g['features']:
    p, geom = f['properties'], f.get('geometry') or {}
    if geom.get('type') != 'Point' or not p.get('adm3_name'):
        continue
    lon, lat = geom['coordinates'][:2]
    pts.append((city_key(p['adm3_name']), city_key(p['adm2_name']), lat, lon, p['adm3_pcode'], p['adm1_name']))
P = pd.DataFrame(pts, columns=['ck', 'pk', 'lat', 'lon', 'adm3_pcode', 'adm1'])
cent = P.groupby(['ck', 'pk']).agg(lat=('lat', 'median'), lon=('lon', 'median'), adm3_pcode=('adm3_pcode', 'first'), n=('lat', 'size')).reset_index()
by_city = cent.sort_values('n', ascending=False).drop_duplicates('ck').set_index('ck')
by_cp = cent.set_index(['ck', 'pk'])
out = pd.read_csv('data/dialysis_centers_philippines.csv', dtype=str).fillna('')
out['psgc_adm3_pcode'] = ''
filled = 0
for i, r in out.iterrows():
    ck, pk = city_key(r.municipality), city_key(r.province.replace('PROVINCE OF ', '').replace(' PROVINCE', ''))
    row = by_cp.loc[(ck, pk)] if (ck, pk) in by_cp.index else (by_city.loc[ck] if ck in by_city.index else None)
    if row is None:
        continue
    out.at[i, 'psgc_adm3_pcode'] = row.adm3_pcode
    if not r.lat:
        out.at[i, 'lat'], out.at[i, 'lon'] = f'{row.lat:.5f}', f'{row.lon:.5f}'
        out.at[i, 'coord_source'] = 'APPROXIMATE: municipality centroid (median of OSM health facilities, HDX)'
        filled += 1
out.to_csv('data/dialysis_centers_philippines.csv', index=False)
print('approx coords filled:', filled, '| still no coords:', (out.lat == '').sum(), '| pcode matched:', (out.psgc_adm3_pcode != '').sum())
print(out[out.lat == ''][['municipality', 'province']].drop_duplicates().head(30).to_string())
