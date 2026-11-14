#!/usr/bin/env python3
"""Build operator / directory / geo outputs and the not-in-PhilHealth candidate list.

Inputs (all produced by other scripts in scripts/ or saved raw pages):
  data/philhealth_fdc_2026-09-30.csv
  data/geo/osm_dialysis.csv                        (osm_extract_dialysis.py + osm_filter.py)
  raw/geo/hdx_health/health_facilities.geojson     (HOT/HDX OSM health facilities: used as
                                                   municipality gazetteer + nearest-adm3 lookup)
  raw/operators/nephroplus/nephroplus_branches.json (scrape_nephroplus_ph.py)
  raw/operators/bbraun_ph_locationmap.json          (B. Braun centre-locator JSON, bbraun.ph)
  raw/operators/hemotek_branches.html               (hemotek.net branches page)
  raw/directories/clinicfinderph/clinicfinderph_dialysis.json (scrape_clinicfinderph.py)
  raw/directories/mykidneyjourney/ph-dialysis-centers.html    (Baxter "My Kidney Journey")
  raw/directories/psn/psn_dialysis-center_wpjson_p1.json      (PSN WP REST, names only)
  scripts/manual_sources.py                         (hand transcriptions w/ source URLs)
Outputs:
  data/operators/chain_branches.csv, data/operators/operators.csv,
  data/directories/directory_listings.csv, data/operators/not_in_philhealth_candidates.csv
"""
import csv, json, math, os, re, sys, unicodedata
from collections import defaultdict
import pandas as pd
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_sources as M

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
ACCESS = M.ACCESS
PH_URL = 'https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf'

# ----------------------------------------------------------------------------- helpers
def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s or '') if not unicodedata.combining(c))

def norm_muni(s, manila_rule=True):
    s = strip_acc(str(s or '')).upper()
    if not s or s == 'NAN': return ''
    if manila_rule and re.search(r'\bMANILA\b', s) and 'METRO' not in s: return 'MANILA'
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'\bCITY OF\b|\bCITY\b|\bMUNICIPALITY OF\b', ' ', s)
    s = s.replace('STO.', 'SANTO').replace('STA.', 'SANTA').replace('GEN.', 'GENERAL')
    s = re.sub(r'\bSTO\b', 'SANTO', s); s = re.sub(r'\bSTA\b', 'SANTA', s)
    s = re.sub(r'[^A-Z ]', ' ', s)
    s = s.replace('LAS PINAS', 'LAS PINAS').replace('PARANAQUE', 'PARANAQUE')
    return re.sub(r'\s+', ' ', s).strip()

def muni_eq(a, b):
    a, b = norm_muni(a), norm_muni(b)
    if not a or not b: return False
    if a == b: return True
    if len(a) >= 5 and len(b) >= 5 and (a in b or b in a): return True
    return fuzz.ratio(a, b) >= 90

LEGAL = r'\b(INC|INCORPORATED|CORP|CORPORATION|CO|OPC|LTD|PHILS|PHILIPPINES|PHIL|COMPANY)\b'
GENERIC = r'\b(THE|OF|AND|DIALYSIS|DIALYSES|CENTER|CENTRE|CENTERS|CLINIC|CLINICS|HEMODIALYSIS|HAEMODIALYSIS|KIDNEY|RENAL|CARE|MEDICAL|HEALTH|HEALTHCARE|UNIT|SERVICES|SERVICE|HOSPITAL|DIAGNOSTIC|DIAGNOSTICS|GROUP|BRANCH|NEPHROLOGY|FOUNDATION)\b'
def clean_name(s, heavy=False):
    s = strip_acc(str(s or '')).upper()
    s = s.replace('SAINT ', 'ST ').replace('ST. ', 'ST ').replace('&', ' AND ')
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    s = re.sub(LEGAL, ' ', s)
    if heavy: s = re.sub(GENERIC, ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def name_score(a, b):
    ha, hb = clean_name(a, True), clean_name(b, True)
    if ha and hb:
        ts = fuzz.token_set_ratio(ha, hb) if min(len(ha), len(hb)) >= 4 else fuzz.ratio(ha, hb)
        return max(0.7 * ts + 0.3 * fuzz.token_sort_ratio(ha, hb), 0.9 * fuzz.token_sort_ratio(clean_name(a), clean_name(b)))
    return 0.8 * fuzz.token_sort_ratio(clean_name(a), clean_name(b))

# ----------------------------------------------------------------------------- operators
# (canonical operator, regex on facility name, regex on e-mail domain or None)
OPERATOR_RULES = [
    ('B. Braun Avitum Philippines', r'B\.? ?BRAUN', r'bbraun'),
    ('NephroPlus (NephroCare Health Care Services Philippines Inc.)', r'NEPHROCARE HEALTH CARE SERVICES|NEPHRO ?PLUS|ROYAL CARE DIALYSIS|RENAL THERAPY SOLUTIONS', r'nephroplus|\.pho@'),
    ('Fresenius Kidney Care (FMC Renalcare Corp.)', r'FRESENIUS|FRISENIUS|FMC RENALCARE', r'fmc-asia|freseniusm'),
    ('Avitus Kidney Care and Dialysis Center', r'AVITUS|NVITUS', r'avitus'),
    ('Hemotek Renal Center Inc.', r'HEMOTEK', r'hemotek'),
    ('Nephro Synergies Inc. (The Nephro Group)', r'NEPHRO SYNERGIES|NSPI', None),
    ('The Nephro Group', r'NEPHROLOGY CENTER OF|NEPHROLOGY SERVICES PHIL|NEPHRO SYSTEMS|NEPHRO GROUP', r'nephrogroup'),
    ('TotalCare Dialysis Center', r'TOTAL ?CARE DIALYSIS', None),
    ('JL Dialmed Dialysis Center', r'JL DIALMED|DIALMED', r'dialmed'),
    ('Prime Dialysis Center Inc.', r'PRIME DIALYSIS CENTER', None),
    ('One Dialysis Center (TresMedica)', r'^ONE DIALYSIS CENTER|TRESMEDICA', r'tresmedica'),
    ('Vida / Avida Dialysis Center Phils.', r'^A?VIDA DIALYSIS CENTER', r'avidadialysis'),
    ("St. Theresa('s) Dialysis Center", r"^ST\.? THERESA'?S? DIALYSIS|^SAINT THERESA'?S? DIALYSIS", None),
    ('Premier 101 Healthcare Management Inc.', r'PREMIER 101', None),
    ('Pro Renal Specialist Dialysis Center Corp.', r'PRO RENAL SPECIALIST', None),
    ('KidneyCare Dialysis Center', r'^KIDNEYCARE DIALYSIS', None),
    ('Nephro Specialist (Cebu group)', r'NEPHRO SPECIALIST OF', None),
    ('Saint Marina Kidney / Dialysis Center', r'(ST\.?|SAINT) MARINA', None),
    ('Saint Mary Kidney Care Inc.', r'SAINT MARY KIDNEY CARE|ST\.? MARY KIDNEY CARE', None),
    ('NephroMed Asia Medical Group', r'NEPHROMED ?ASIA', None),
    ('New Hope (dialysis group)', r'^(QC )?NEW HOPE', None),
    ('Global Reliance Renalcare Inc.', r'GLOBAL RELIANCE', None),
    ('MSR Health Care Inc.', r'^MSR HEALTH', None),
    ('Best Option Medical Group Inc.', r'BEST OPTION MEDICAL', None),
    ('The Best Renal Care Inc.', r'BEST RENAL CARE', r'thebestrenalcare'),
    ('KidneyWell Medical Health Services Inc.', r'KIDNEYWELL', None),
    ('JOrtiz Dialysis Corporation', r'JORTIZ', r'jortiz|dialysiscenter\.ph'),
    ('First Renal Dialysis Center', r'FIRST RENAL DIALYSIS', None),
    ('GC Hemodynamix Inc.', r'HEMODYNAMIX', None),
    ('Hope Zarepath Dialysis Center', r'ZAREPATH', None),
    ('RAJ Medical Solutions Inc.', r'RAJ MEDICAL', None),
    ('Alia Via Medical Corporation', r'ALIA VIA', None),
    ('M3 Dialysis Center Inc.', r'^M-?3 DIALYSIS', None),
    ('North East Dialysis Center Corp.', r'NORTH EAST DIALYSIS', None),
    ('Saint Nicholas Dialysis Center Inc.', r'(ST\.?|SAINT) NICHOLAS DIALYSIS', None),
    ('Medical Mission Group (cooperative network)', r'MEDICAL MISSION GROUP', r'mmgphil'),
    ('St. John Biocare and Dialysis Center Foundation', r'ST\.? JOHN BIOCARE', None),
    ('Renal Med Dialysis Center Inc.', r'RENAL ?MED DIALYSIS', None),
    ('Renal One Dialysis Corp.', r'RENAL ONE DIALYSIS', None),
    ('Nursia Dialysis Inc.', r'NURSIA', None),
    ('Healthway Medical Network (AC Health)', r'HEALTHWAY', r'healthway\.com|qualimed'),
    ('Juan Dialysis Center', r'^JUAN (NEPHRO )?DIALYSIS', r'juandialysis'),
    ('Excelsior (excelsior.net.ph)', r'EXCELSIOR', r'excelsior\.net'),
    ('HealthFirst (healthfirst.com.ph)', r'HEALTH ?FIRST', r'healthfirst\.com'),
    ('ClearBridge Health Philippines', r'CLEARBRIDGE', r'clearbridge'),
    ('Reliance Dialysis Center', r'^RELIANCE DIALYSIS', r'reliancehealth'),
    ('Healthy Kidney Center', r'HEALTHY KIDNEY CENTER', r'healthykidneycenter'),
    ('Lifestream Dialysis', r'LIFESTREAM', r'lifestreamdialysis'),
    ('CuraKidney', r'CURA ?KIDNEY', r'curakidney'),
    ('Pampanga Provincial Dialysis Centers (Prov. Govt.)', r'PAMPANGA PROVINCIAL DIALYSIS', None),
    ('Kolff Dialysis Inc.', r'KOLFF|KOFF DIALYSIS', None),
    ('NephroLife', r'NEPHROLIFE', None),
    ('Nueva Ecija Renal Center', r'NUEVA ECIJA RENAL CENTER', None),
    ('Medline Dialysis Center', r'^MEDLINE DIALYSIS', None),
]
_RULES = [(o, re.compile(n), re.compile(e, re.I) if e else None) for o, n, e in OPERATOR_RULES]
def operator_of(name, email=''):
    n = strip_acc(str(name or '')).upper()
    for o, rn, re_ in _RULES:
        if rn.search(n): return o
    if email:
        for o, rn, re_ in _RULES:
            if re_ is not None and re_.search(str(email)): return o
    return ''

# ----------------------------------------------------------------------------- gazetteer
hdx = json.load(open('raw/geo/hdx_health/health_facilities.geojson'))['features']
GAZ = []   # (lat, lon, adm3, adm2)
MUNIS = {}  # norm muni -> (display, province)
for f in hdx:
    p = f['properties']; g = f['geometry']
    a3, a2 = p.get('adm3_name') or '', p.get('adm2_name') or ''
    if a2.startswith('Metropolitan Manila First District'): a3 = 'Manila'
    if g and g['type'] == 'Point' and a3:
        GAZ.append((g['coordinates'][1], g['coordinates'][0], a3, a2))
    if a3: MUNIS.setdefault(norm_muni(a3), (a3, a2))
ph = pd.read_csv('data/philhealth_fdc_2026-09-30.csv', dtype=str).fillna('')
for m, pv in zip(ph.municipality, ph.province):
    MUNIS.setdefault(norm_muni(m), (m.title(), pv.title()))
ALIASES = {'NOVALICHES': 'Quezon City', 'CUBAO': 'Quezon City', 'DILIMAN': 'Quezon City', 'FAIRVIEW': 'Quezon City',
           'ALABANG': 'Muntinlupa City', 'TONDO': 'Manila', 'SAMPALOC': 'Manila', 'MALATE': 'Manila', 'ERMITA': 'Manila',
           'BINONDO': 'Manila', 'SANTA MESA': 'Manila', 'PANANAQUE': 'Paranaque City', 'BGC': 'Taguig City', 'MACTAN': 'Lapu-Lapu City'}
for k, v in ALIASES.items(): MUNIS[k] = (v, '')
MUNI_KEYS = sorted([k for k in MUNIS if len(k) >= 3], key=len, reverse=True)

def nearest_adm3(lat, lon):
    try: lat, lon = float(lat), float(lon)
    except Exception: return '', '', ''
    best, bd = None, 1e9
    for la, lo, a3, a2 in GAZ:
        d = (la - lat) ** 2 + ((lo - lon) * math.cos(math.radians(lat))) ** 2
        if d < bd: bd, best = d, (a3, a2)
    km = math.sqrt(bd) * 111
    return (best[0], best[1], round(km, 2)) if best and km < 5 else ('', '', round(km, 2))

PROVS = {norm_muni(f['properties'].get('adm2_name') or '') for f in hdx} - {''}   # true provinces (HDX adm2)
def muni_from_text(txt):
    """pick the gazetteer municipality whose mention ends right-most in the text (addresses run
    street > barangay > city > province); province names are used only if nothing else matches."""
    txt2 = re.sub(r'(?i)metro manila|kalakhang maynila|philippines|\bNCR\b', ' ', strip_acc(str(txt or '')))
    t = ' ' + norm_muni(txt2, manila_rule=False) + ' '
    hits = []
    for k in MUNI_KEYS:
        for m in re.finditer(r'(?<= )' + re.escape(k) + r'(?= )', t):
            hits.append((m.end(), len(k), k))
    if not hits: return ''
    raw = strip_acc(str(txt)).upper()
    nonprov = [h for h in hits if h[2] not in PROVS or re.search(re.escape(h[2]) + r',? CITY', raw)]
    h = max(nonprov or hits)
    return MUNIS[h[2]][0]

# ----------------------------------------------------------------------------- PhilHealth index
ph['op'] = [operator_of(n, e) for n, e in zip(ph.name, ph.email)]
ph['nmuni'] = ph.municipality.map(norm_muni)
PH_ROWS = ph.to_dict('records')

def match_philhealth(name, muni, operator=''):
    """return (status, best_row, score). status: matched / possible / no_match / no_match_generic"""
    best, bs = None, -1
    for r in PH_ROWS:
        same_m = muni_eq(muni, r['municipality']) if muni else False
        s = name_score(name, r['name'])
        if operator and r['op'] == operator and same_m: s = max(s, 95)
        eff = s + (30 if same_m else 0)
        if eff > bs: bs, best, best_s, best_same = eff, r, s, same_m
    generic = not clean_name(name, True)
    strict = fuzz.token_sort_ratio(clean_name(name, True), clean_name(best['name'], True)) if not generic else 0
    if best_same and best_s >= 72: return 'matched', best, best_s
    if not muni and best_s >= 90 and strict >= 85: return 'matched_name_only', best, best_s
    if not muni and best_s >= 80 and not generic: return 'possible_name_only', best, best_s
    if best_same and best_s >= 55: return 'possible', best, best_s
    if best_s >= 88 and strict >= 80 and not (operator and best['op'] == operator):
        return 'possible_other_muni', best, best_s
    return ('no_match_generic_name' if generic else 'no_match'), best, best_s

# ============================================================================= 1. chain branches
CB_COLS = ['operator', 'branch_name', 'address', 'city', 'province', 'region', 'phone', 'email', 'lat', 'lon',
           'hd_stations', 'opening_year', 'nephrologist_in_charge', 'hours', 'services', 'status',
           'source_type', 'source_url', 'access_date', 'extraction_method', 'notes',
           'philhealth_match', 'philhealth_seq', 'philhealth_name', 'philhealth_municipality', 'match_score']
cb = []
def add_cb(**k):
    row = {c: '' for c in CB_COLS}; row.update({k2: ('' if v is None else v) for k2, v in k.items()}); row['access_date'] = ACCESS
    cb.append(row)

# 1a. PhilHealth list grouped by operator rule
for r in PH_ROWS:
    if not r['op']: continue
    add_cb(operator=r['op'], branch_name=r['name'], address=r['street'], city=r['municipality'], province=r['province'], region=r['region'],
           phone=r['tel'], email=r['email'], source_type='philhealth_fdc_list (operator assigned by name/e-mail rule)', source_url=PH_URL,
           extraction_method='derived', notes=f"accreditation_expiry {r['accreditation_expiry']}; sector {r['sector']}",
           philhealth_match='self', philhealth_seq=r['seq'], philhealth_name=r['name'], philhealth_municipality=r['municipality'])

web_rows = []  # operator-website rows (also feed candidate list)
def add_web(op, name, address, city, province, source_url, method, src_type, **extra):
    city = city or muni_from_text(address) or muni_from_text(name)
    st, best, sc = match_philhealth(name, city, op)
    add_cb(operator=op, branch_name=name, address=address, city=city, province=province, source_type=src_type,
           source_url=source_url, extraction_method=method, philhealth_match=st,
           philhealth_seq=best['seq'] if best is not None and st.startswith(('matched', 'possible')) else '',
           philhealth_name=best['name'] if best is not None and st.startswith(('matched', 'possible')) else '',
           philhealth_municipality=best['municipality'] if best is not None and st.startswith(('matched', 'possible')) else '',
           match_score=round(sc, 1), **extra)
    web_rows.append(cb[-1])

# 1b. NephroPlus
for o in json.load(open('raw/operators/nephroplus/nephroplus_branches.json')):
    add_web('NephroPlus (NephroCare Health Care Services Philippines Inc.)', o['name'], o['address'], '', '',
            o['href'], 'page_fetched', 'operator website (nephroplus.ph city listing ' + o['list_url'] + ')',
            phone='+639178750003 (central)', email='customercare@nephroplus.ph')
# 1c. B. Braun locator
for x in json.load(open('raw/operators/bbraun_ph_locationmap.json')):
    if x.get('country') != 'PH': continue
    tt = ';'.join(x.get('searchFields', {}).get('Treatmenttypes', []))
    addr = f"{x.get('streetAndNumber','')}, {x.get('city','')} {x.get('zipCode','')}".strip(', ')
    city = muni_from_text(addr)
    add_web('B. Braun Avitum Philippines', x.get('title', '').strip(), addr, city, '',
            'https://www.bbraun.ph/en/patient-care/services/care-and-dialysis-centers.html', 'page_fetched',
            'operator website (bbraun.ph centre locator JSON /bin/locationmap)',
            phone=x.get('phoneNumber', ''), email=x.get('mailAddress', ''), lat=x.get('latitude', ''), lon=x.get('longitude', ''),
            services=tt, notes='locator coordinates not validated; several look wrong (e.g. Mandaluyong lat 12.59, Olongapo pin in QC, Roxas lat 11.1)')
# 1d. Hemotek
txt = BeautifulSoup(open('raw/operators/hemotek_branches.html').read(), 'lxml').get_text('|', strip=True)
seg = txt[txt.find('NCR BRANCHES'):txt.find('Was incoporated')]
parts = [p.strip() for p in seg.split('|') if p.strip()]
i = 0; region = ''
while i < len(parts):
    p = parts[i]
    if p.endswith('BRANCHES') or 'BRANCHES' in p: region = p; i += 1; continue
    if i + 4 < len(parts) and '@hemotek.net' in parts[i + 4]:
        add_web('Hemotek Renal Center Inc.', 'Hemotek Renal Center - ' + p, parts[i + 1], '', '', 'https://hemotek.net/?page_id=110', 'page_fetched',
                'operator website', phone=f'{parts[i+2]} / {parts[i+3]}', email=parts[i + 4], notes=region.title(),
                services='High-flux/low-flux HD; online HDF; BCM; FIRAPY (company-wide services page)')
        i += 5; continue
    i += 1
# 1e. FKC
for name, addr, city, prov, url, method, ex in M.FKC:
    add_web('Fresenius Kidney Care (FMC Renalcare Corp.)', name, addr, city, prov, url, method,
            'operator website (robots.txt Disallow: / -> search-engine result only)', **ex)
# 1f. Nephro Group / Synergies
for op, name, addr, city, prov, phone, kind in M.NEPHRO_GROUP:
    url = M.NS_URL if kind != 'training-page location' else M.NS_URL.replace('id=6&Itemid=120', 'id=5&Itemid=119')
    add_web('Nephro Synergies Inc. (The Nephro Group)' if op == 'Nephro Synergies' else 'The Nephro Group', name, addr, city, prov, url,
            'page_fetched', 'operator website (nephrosynergies.com, footer (c)2013 - may be dated)', phone=phone, notes=kind)
# 1g. TresMedica
for name, addr, city, prov, phone, status, tags in M.TRESMEDICA:
    add_web('One Dialysis Center (TresMedica)', name, addr, city, prov, M.TM_URL, 'page_fetched', 'operator website',
            phone=phone, status=status, notes=tags)
# 1h. CuraKidney
for name, addr, city, prov, phone, hours in M.CURAKIDNEY:
    add_web('CuraKidney', name, addr, city, prov, M.CURAKIDNEY_URL, 'page_fetched', 'operator website', phone=phone, hours=hours,
            services='HD (single-use dialyzers, double-pass RO); nephrologist on duty')

os.makedirs('data/operators', exist_ok=True)
pd.DataFrame(cb, columns=CB_COLS).to_csv('data/operators/chain_branches.csv', index=False)

# ============================================================================= 2. operators.csv
OPS = [
 # operator, legal entity, parent, HQ, claimed, claim date, claim source, website, notes
 ('NephroPlus (NephroCare Health Care Services Philippines Inc.)', 'NephroCare Health Care Services Philippines Inc. (formerly Royal Care Dialysis; acquired Renal Therapy Solutions Inc. 2024)', 'Nephrocare Health Services Ltd (NephroPlus), Hyderabad, India', 'Metro Manila', '53', '2026-09', 'https://mindanaodailynews.com/nephroplus-expands-footprint-to-eight-centers-across-visayas-and-mindanao-opens-new-greenfield-center-in-quezon-city/', 'https://nephroplus.ph', 'Entered PH FY20 via majority stake in Royal Care Dialysis Clinics; 27 clinics after RTSI deal (manilatimes 2024-03-01); 36 after 7-clinic acquisition (nephroplus.com press 2025-02-18); 39 after 5 more (Aug 2025); 50th clinic Orion, Bataan (tribune 2026-07-14); 53 incl. 8 outside Luzon (Sept 2026)'),
 ('B. Braun Avitum Philippines', 'B. Braun Avitum Philippines, Inc.', 'B. Braun Melsungen AG (Germany)', '', '25 (2020); 33 PH entries in locator (2026)', '2020 / 2026-11', 'https://newsinfo.inquirer.net/?p=1321247 ; https://www.bbraun.ph/en/patient-care/services/care-and-dialysis-centers.html', 'https://www.bbraun.ph', 'Inquirer 2020: owns and manages 25 dialysis centres in Luzon; locator also lists partner hospital units (Mary Johnston, Paranaque Doctors, Eagle Rock, Best Nephro Specialist)'),
 ('Fresenius Kidney Care (FMC Renalcare Corp.)', 'FMC Renalcare Corp. / Fresenius Medical Care Philippines, Inc.', 'Fresenius Medical Care AG (Germany)', '2257 Chino Roces Ave. Ext., Makati City', '24', '2026-11', 'https://freseniusmedicalcare.com/en-ph/clinics/', 'https://freseniuskidneycare.ph', 'FMC PH site: "operates 24 Dialysis centers locally"; Oct 2025 Ormoc opening report said 20 branches; freseniuskidneycare.ph robots.txt disallows crawling'),
 ('Hemotek Renal Center Inc.', 'Hemotek Renal Center, Inc.', '', '', '19 listed on website', '2026-11', 'https://hemotek.net/?page_id=110', 'https://hemotek.net', 'SEC-registered 11 June 2008 (website)'),
 ('The Nephro Group', 'Nephro Group Dialysis Centers Inc. / Nephrology Center of * / Nephrology Services Phils. Inc. / Nephro Systems Phils. Inc.', '', '6/F Eastgate Center 169 EDSA, Mandaluyong (Nephro Systems)', '', '', 'http://www.nephrosynergies.com/index.php?option=com_content&view=article&id=1&Itemid=101', 'nephrogroup.com (unreachable)', 'Self-described "pioneer in professional outpatient dialysis operations" launched 1995; "biggest and fastest growing operator of free-standing dialysis clinics"'),
 ('Nephro Synergies Inc. (The Nephro Group)', 'Nephro Synergies, Inc.', 'The Nephro Group', '', '', '', 'http://www.nephrosynergies.com/', 'http://www.nephrosynergies.com', 'Established 2012; hospital JV partnerships (70-30 JV model); runs Global Nephro Training Center'),
 ('One Dialysis Center (TresMedica)', 'TresMedica', '', 'The Gate, Baltao Compound, Ortigas Ave. Ext., Taytay, Rizal', '12 (255 machines)', '2026-11', 'https://tresmedica.com/centers/', 'https://tresmedica.com', 'Own One Dialysis Center brand + LGU partnership centres; No Balance Billing pledge'),
 ('Avitus Kidney Care and Dialysis Center', 'Avitus Kidney Care and Dialysis Center Corporation; Avitus Davao Dialysis Center Corp.; Avitus Pangasinan Dialysis Center Corp.', '', '', '', '', 'https://ph.jobstreet.com/companies/avitus-kidney-care-and-dialysis-center-corporation-168553584420617', '', 'No reachable website (avitus.com.ph / avituskidneycare.com do not resolve); branches from PhilHealth list'),
 ('Prime Dialysis Center Inc.', 'Prime Dialysis Center Inc. (PDCI)', '', '', '', '', 'https://manilastandard.net/lgu/314577098/alicia-town-now-has-new-dialysis-center.html', '', 'President Dr. Gjay L. Ordinal (Manila Standard 2025); PPP partner for 100-machine Flora V. Valisno De Siojo Dialysis Center, Manila (MB 2026-08-28)'),
 ('Premier 101 Healthcare Management Inc.', 'Premier 101 Healthcare Management Inc.', '', '', '', '', 'https://pia.gov.ph/news/luzon/cl/first-ppp-dialysis-center-in-malolos-covered-by-philhealth/', '', 'PPP partner of Malolos City 40-machine centre (2025)'),
 ('Healthway Medical Network (AC Health)', 'Healthway Medical / Healthway Qualimed hospitals; PMVI', 'Ayala Healthcare Holdings Inc. (AC Health), Ayala Corp.', 'Makati City', '13 planned Iloilo PPP sites (8 stations each) + One Ayala (12 stations)', '2025-11 / 2026-07', 'https://iloilo.gov.ph/en/health-news/iloilo-province-partners-ac-health-bring-lifesaving-dialysis-care-closer-ilonggo', 'https://www.healthway.com.ph', 'Iloilo PPP signed 2025-11-25: AC Health/PMVI to fit out, equip, manage and operate dialysis centres in 12 district hospitals + provincial hospital; individual sites not named'),
 ('Metro Pacific Health', 'Metro Pacific Health (hospital group)', 'Metro Pacific Investments Corp.', '', '31 hospitals (dialysis units per hospital not enumerated)', '2026-07', 'https://www.philstar.com/business/real-estate/2026/07/02/2539132/metro-pacific-expands-hospital-network-31', 'https://www.metropacifichealth.com', 'Hospital-based dialysis units (e.g. Makati Medical Center, De Los Santos Medical Center hemodialysis center); not enumerated here - hospital lists handled by other workstream'),
 ('CuraKidney', 'CuraKidney', '', '', '2', '2026-11', 'https://www.curakidney.com/', 'https://www.curakidney.com', 'Single-use dialyzers; Nipro machines; Medical Director Dr. Jason Paul T. Medina'),
 ('Medical Mission Group (cooperative network)', 'Medical Mission Group Hospitals and Health Services Cooperative of the Phils. - Federation', '', '', '', '', PH_URL, '', 'Cooperative hospital network; PhilHealth-listed FDCs'),
]
op_rows = []
cbdf = pd.DataFrame(cb)
for op in sorted(set(cbdf.operator)):
    sub = cbdf[cbdf.operator == op]
    n_ph = int((sub.philhealth_match == 'self').sum())
    n_web = int((sub.philhealth_match != 'self').sum())
    meta = next((x for x in OPS if x[0] == op), None)
    if n_ph < 2 and not meta and n_web == 0: continue
    op_rows.append({'operator': op, 'legal_entities': meta[1] if meta else '; '.join(sorted(set(ph[ph.op == op].name)))[:300],
                    'parent': meta[2] if meta else '', 'hq': meta[3] if meta else '',
                    'branch_count_claimed': meta[4] if meta else '', 'claim_date': meta[5] if meta else '',
                    'branches_in_philhealth_fdc_2026-09-30': n_ph, 'branches_listed_on_operator_web_or_news': n_web,
                    'website': meta[7] if meta else '', 'notes': meta[8] if meta else 'grouped from PhilHealth FDC list by name/e-mail rule',
                    'source_url': meta[6] if meta else PH_URL, 'access_date': ACCESS})
for meta in OPS:
    if meta[0] not in set(cbdf.operator):
        op_rows.append({'operator': meta[0], 'legal_entities': meta[1], 'parent': meta[2], 'hq': meta[3], 'branch_count_claimed': meta[4],
                        'claim_date': meta[5], 'branches_in_philhealth_fdc_2026-09-30': 0, 'branches_listed_on_operator_web_or_news': 0,
                        'website': meta[7], 'notes': meta[8], 'source_url': meta[6], 'access_date': ACCESS})
opdf = pd.DataFrame(op_rows).sort_values('branches_in_philhealth_fdc_2026-09-30', ascending=False)
opdf.to_csv('data/operators/operators.csv', index=False)

# ============================================================================= 3. directory listings
DL_COLS = ['name', 'address', 'city', 'province', 'phone', 'email', 'lat', 'lon', 'facility_type', 'status', 'machines', 'event_date',
           'operator', 'source_name', 'source_url', 'access_date', 'extraction_method', 'notes']
dl = []
def add_dl(**k):
    row = {c: '' for c in DL_COLS}; row.update({a: ('' if b is None else b) for a, b in k.items()}); row['access_date'] = ACCESS; dl.append(row)
# ClinicFinderPH
for x in json.load(open('raw/directories/clinicfinderph/clinicfinderph_dialysis.json')):
    add_dl(name=x.get('name', ''), address=x.get('street', ''), city=x.get('city', ''), province=x.get('province', ''), phone=x.get('phone', ''),
           lat=x.get('lat', ''), lon=x.get('lon', ''), facility_type=x.get('category', ''), source_name='ClinicFinderPH',
           source_url=x['url'], extraction_method='page_fetched (schema.org JSON-LD)', notes='hours: ' + x.get('hours', '') if x.get('hours') else '')
# Baxter My Kidney Journey (updated Sept 2023)
html = open('raw/directories/mykidneyjourney/ph-dialysis-centers.html').read()
t = BeautifulSoup(html, 'lxml').get_text('|', strip=True)
t = t[t.find('Select your region'):t.find('Questions to ask your nephrologist')]
parts = [p.strip() for p in t.split('|') if p.strip()]
REG = {'Calabarzon', 'Metro Manila', 'Luzon', 'Visayas - Cebu', 'Mindanao - Davao'}
cur = None; region = ''
for i, p in enumerate(parts):
    if p in REG: region = p; continue
    if p == 'Address:' and i > 0:
        nm = parts[i - 1]; addr = parts[i + 1] if i + 1 < len(parts) else ''
        phones, emails = [], []
        j = i + 2
        while j < len(parts) and parts[j] not in REG and not (j + 1 < len(parts) and parts[j + 1] == 'Address:'):
            if re.search(r'\d{3}', parts[j]) and not parts[j].endswith(':'): phones.append(parts[j])
            j += 1
        add_dl(name=nm, address=addr, city=muni_from_text(addr), phone='; '.join(phones), facility_type='dialysis centre / hospital (HD or PD)',
               source_name='Baxter My Kidney Journey PH directory (updated Sept 2023)', source_url='https://apac.mykidneyjourney.com/en-PH/ph-dialysis-centers',
               extraction_method='page_fetched', notes='region tab: ' + region)
# PSN (names only)
for x in json.load(open('raw/directories/psn/psn_dialysis-center_wpjson_p1.json')):
    nm = BeautifulSoup(x['title']['rendered'], 'lxml').get_text()
    add_dl(name=nm, facility_type='dialysis centre (PSN directory; name only)', source_name='Philippine Society of Nephrology dialysis-center directory',
           source_url=x['link'], extraction_method='WP REST API /wp-json/wp/v2/dialysis-center (title only; detail pages empty)', notes='posted ' + x['date'][:10])
# News
for nm, addr, city, prov, status, date, mach, op, url, note in M.NEWS:
    add_dl(name=nm, address=addr, city=city, province=prov, status=status, event_date=date, machines=mach, operator=op,
           facility_type='news: opening/announcement', source_name='news', source_url=url, extraction_method='search_summary', notes=note)
os.makedirs('data/directories', exist_ok=True)
pd.DataFrame(dl, columns=DL_COLS).to_csv('data/directories/directory_listings.csv', index=False)

# ============================================================================= 4. candidates
cand = []
osm = pd.read_csv('data/geo/osm_dialysis.csv', dtype=str).fillna('')
for _, r in osm.iterrows():
    nm = r['name'] or r['operator']
    if not nm: nm = ''
    city = r['addr_city']; how = 'osm addr:city'
    a3, a2, km = nearest_adm3(r['lat'], r['lon'])
    if not city: city, how = a3, f'nearest HDX health facility adm3 ({km} km)'
    cand.append(dict(name=nm, address=' '.join(x for x in [r['addr_housenumber'], r['addr_street'], r['addr_barangay'], r['addr_full']] if x),
                     city=city, city_method=how, province=r['addr_province'] or a2, lat=r['lat'], lon=r['lon'], phone=r['phone'],
                     operator=operator_of(nm), source='OSM (' + r['category'] + ')', source_url=r['source_url']))
for r in web_rows:
    cand.append(dict(name=r['branch_name'], address=r['address'], city=r['city'], city_method='operator site', province=r['province'], lat=r['lat'],
                     lon=r['lon'], phone=r['phone'], operator=r['operator'], source='operator website: ' + r['operator'], source_url=r['source_url'],
                     status=r['status']))
for r in dl:
    if r['source_name'].startswith('Philippine Society'): pass
    city = r['city'] or muni_from_text(r['address'])
    cand.append(dict(name=r['name'], address=r['address'], city=city, city_method='directory', province=r['province'], lat=r['lat'], lon=r['lon'],
                     phone=r['phone'], operator=r['operator'] and operator_of(r['operator']) or operator_of(r['name']), source=r['source_name'],
                     source_url=r['source_url'], status=r['status'], event_date=r['event_date'], machines=r['machines']))
for c in cand:
    if not c['name']: c['ph_status'] = 'no_match_generic_name'; c['best'] = None; c['score'] = 0; continue
    st, best, sc = match_philhealth(c['name'], c['city'], c['operator'])
    c['ph_status'], c['best'], c['score'] = st, best, sc

# cluster unmatched candidates across sources (same muni & name score >= 85, or within 150 m)
un = [c for c in cand if c['ph_status'] not in ('matched', 'matched_name_only')]
cl = list(range(len(un)))
def find(i):
    while cl[i] != i: cl[i] = cl[cl[i]]; i = cl[i]
    return i
def dist_m(a, b):
    try: return math.hypot((float(a['lat']) - float(b['lat'])) * 111000, (float(a['lon']) - float(b['lon'])) * 111000 * math.cos(math.radians(float(a['lat']))))
    except Exception: return 1e9
for i in range(len(un)):
    for j in range(i + 1, len(un)):
        a, b = un[i], un[j]
        same = muni_eq(a['city'], b['city'])
        s = name_score(a['name'], b['name']) if a['name'] and b['name'] else 0
        if (same and s >= 85) or (dist_m(a, b) < 150 and s >= 60):
            cl[find(i)] = find(j)
groups = defaultdict(list)
for i, c in enumerate(un): groups[find(i)].append(c)
HOSP = re.compile(r'hospital|medical cent|med\.? ctr|memorial|institute|infirmary|\bmc\b|doctors', re.I)
out = []
for gid, (k, g) in enumerate(sorted(groups.items(), key=lambda kv: kv[1][0]['name'].lower())):
    g.sort(key=lambda c: (c['source'].startswith('OSM'), -len(c['address'] or '')))  # prefer web/directory as display
    head = g[0]
    def first(f): return next((c.get(f) for c in g if c.get(f)), '')
    statuses = sorted(set(c['ph_status'] for c in g))
    best = max(g, key=lambda c: c['score'])
    out.append({
        'candidate_id': f'NPH{gid+1:04d}', 'name': head['name'], 'alt_names': ' | '.join(sorted(set(c['name'] for c in g[1:] if c['name'] != head['name'])))[:300],
        'address': first('address'), 'city': first('city'), 'city_method': head['city_method'], 'province': first('province'),
        'lat': first('lat'), 'lon': first('lon'), 'phone': first('phone'), 'operator': first('operator'),
        'status_reported': first('status'), 'event_date': first('event_date'), 'machines': first('machines'),
        'likely_hospital_based': 'yes' if any(HOSP.search(c['name']) for c in g) else '',
        'match_detail': ';'.join(statuses),
        'match_status': 'possible_match' if any(s.startswith('possible') for s in statuses) else ('generic_name_unmatched' if statuses == ['no_match_generic_name'] else 'no_match'),
        'best_philhealth_name': best['best']['name'] if best['best'] is not None else '', 'best_philhealth_municipality': best['best']['municipality'] if best['best'] is not None else '',
        'best_philhealth_seq': best['best']['seq'] if best['best'] is not None else '', 'best_score': round(best['score'], 1),
        'n_sources': len(g), 'sources': ' | '.join(sorted(set(c['source'] for c in g))),
        'evidence_urls': ' '.join(sorted(set(c['source_url'] for c in g))), 'access_date': ACCESS})
cdf = pd.DataFrame(out)
cdf.to_csv('data/operators/not_in_philhealth_candidates.csv', index=False)

# ----------------------------------------------------------------------------- report
print('chain_branches', len(cb)); print('operators', len(opdf)); print('directory_listings', len(dl))
print('candidates (input rows)', len(cand), 'matched', sum(c['ph_status'].startswith('matched') for c in cand))
print('not_in_philhealth clusters', len(cdf)); print(cdf.match_status.value_counts().to_string())
print(cdf.likely_hospital_based.value_counts().to_string())
