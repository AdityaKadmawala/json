"""Build the master dialysis-center table from parsed sources.

Inputs (data/): philhealth_fdc_2026-09-30.csv, philhealth_hospitals_2026-09-30.csv
Output: data/master_dialysis_centers.csv
Enrichment files from other workstreams are merged by scripts/merge_enrichment.py.
"""
import re, csv
import pandas as pd

FREE_MAIL = {'gmail.com', 'yahoo.com', 'yahoo.com.ph', 'ymail.com', 'hotmail.com', 'outlook.com', 'live.com',
             'icloud.com', 'rocketmail.com', 'outlook.ph', 'aol.com', 'protonmail.com', 'mail.com', 'zoho.com', 'gmai.com'}

# Province / independent city -> administrative region (PSGC, incl. Negros Island Region re-created by RA 12000, 2024)
ADMIN_REGION = {
 'NCR': ['QUEZON CITY','CITY OF MANILA','CALOOCAN CITY','PASIG CITY','PARAÑAQUE CITY','MAKATI CITY','MANDALUYONG CITY',
         'LAS PIÑAS CITY','MARIKINA CITY','MALABON CITY','MUNTINLUPA CITY','TAGUIG CITY','PASAY CITY','VALENZUELA CITY',
         'NAVOTAS CITY','SAN JUAN CITY','PATEROS'],
 'CAR': ['BENGUET','BAGUIO CITY','MOUNTAIN PROVINCE','ABRA','IFUGAO','KALINGA','APAYAO'],
 'Region I (Ilocos)': ['PANGASINAN','LA UNION','ILOCOS SUR','ILOCOS NORTE','DAGUPAN CITY'],
 'Region II (Cagayan Valley)': ['ISABELA','CAGAYAN','NUEVA VIZCAYA','SANTIAGO CITY','QUIRINO','BATANES'],
 'Region III (Central Luzon)': ['BULACAN','PAMPANGA','NUEVA ECIJA','BATAAN','TARLAC','ANGELES CITY','ZAMBALES','OLONGAPO CITY','AURORA'],
 'Region IV-A (CALABARZON)': ['CAVITE','LAGUNA','QUEZON','LUCENA CITY','BATANGAS','PROVINCE OF RIZAL','RIZAL'],
 'MIMAROPA': ['OCCIDENTAL MINDORO','ORIENTAL MINDORO','PUERTO PRINCESA CITY','PALAWAN','MARINDUQUE','ROMBLON'],
 'Region V (Bicol)': ['ALBAY','CAMARINES SUR','NAGA CITY','SORSOGON','CAMARINES NORTE','MASBATE','CATANDUANES'],
 'Region VI (Western Visayas)': ['ILOILO CITY','CAPIZ','ILOILO PROVINCE','ILOILO','ANTIQUE','AKLAN','GUIMARAS'],
 'NIR (Negros Island)': ['BACOLOD CITY','NEGROS OCCIDENTAL','NEGROS ORIENTAL','SIQUIJOR'],
 'Region VII (Central Visayas)': ['CEBU PROVINCE','CEBU','CEBU CITY','BOHOL','LAPU-LAPU CITY','MANDAUE CITY'],
 'Region VIII (Eastern Visayas)': ['TACLOBAN CITY','WESTERN SAMAR','SAMAR','LEYTE','NORTHERN SAMAR','SOUTHERN LEYTE','EASTERN SAMAR','ORMOC CITY','BILIRAN'],
 'Region IX (Zamboanga Peninsula)': ['ZAMBOANGA CITY','ZAMBOANGA DEL NORTE','ZAMBOANGA SIBUGAY','ZAMBOANGA DEL SUR','ISABELA CITY'],
 'Region X (Northern Mindanao)': ['CAGAYAN DE ORO CITY','BUKIDNON','MISAMIS OCCIDENTAL','MISAMIS ORIENTAL','ILIGAN CITY','LANAO DEL NORTE','CAMIGUIN'],
 'Region XI (Davao)': ['DAVAO CITY','DAVAO DEL NORTE','DAVAO DE ORO','DAVAO DEL SUR','DAVAO ORIENTAL','DAVAO OCCIDENTAL','COMPOSTELA VALLEY'],
 'Region XII (SOCCSKSARGEN)': ['SOUTH COTABATO','NORTH COTABATO','COTABATO','SULTAN KUDARAT','SARANGANI','GENERAL SANTOS CITY'],
 'Caraga': ['AGUSAN DEL NORTE','SURIGAO DEL NORTE','AGUSAN DEL SUR','SURIGAO DEL SUR','DINAGAT ISLANDS','BUTUAN CITY'],
 'BARMM': ['COTABATO CITY','LANAO DEL SUR','BASILAN','MAGUINDANAO','MAGUINDANAO DEL NORTE','MAGUINDANAO DEL SUR','SULU','TAWI-TAWI'],
}
PROV2REG = {p: r for r, ps in ADMIN_REGION.items() for p in ps}

SUFFIX_RE = re.compile(r'[,.]?\s*\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|OPC|LTD|LLC|PHILS?|PHILIPPINES)\b\.?', re.I)
BRANCH_RE = re.compile(r'\s*[-–(]?\s*\b([A-Z .]+ )?BRANCH\b.*$', re.I)

def entity_type(name, sector):
    n = name.upper()
    if sector == 'Government': return 'government'
    if re.search(r'\bCOOPERATIVE\b|\bCOOP\b', n): return 'cooperative'
    if re.search(r'\b(FOUNDATION|ASSOCIATION|SOCIETY|MINISTR)', n): return 'non-stock / foundation'
    if re.search(r'\bOPC\b|ONE PERSON CORP', n): return 'one-person corporation'
    if re.search(r'\b(INC|INCORPORATED|CORP|CORPORATION|COMPANY|CO)\b\.?', n): return 'corporation (SEC)'
    return 'unspecified (business name: sole prop/partnership/corp trade name)'

def norm_name(name):
    n = BRANCH_RE.sub('', name.upper())
    n = SUFFIX_RE.sub('', n)
    n = re.sub(r'[^A-Z0-9Ñ ]', ' ', n)
    return re.sub(r'\s+', ' ', n).strip()

def phones(tel):
    out = []
    for part in re.split(r'[/;,]| or |\bloc\b|\blocal\b', str(tel or ''), flags=re.I):
        digits = re.sub(r'\D', '', part)
        if len(digits) < 7: continue
        if digits.startswith('63'): digits = '0' + digits[2:]
        if len(digits) == 10 and digits.startswith('9'): digits = '0' + digits
        kind = 'mobile' if re.fullmatch(r'09\d{9}', digits) else 'landline'
        out.append((('+63' + digits[1:]) if digits.startswith('0') else digits, kind))
    return out

def emails(e):
    return [x.lower().strip(' .') for x in re.split(r'[/;, ]+', str(e or '')) if '@' in x]

class DSU:
    def __init__(s): s.p = {}
    def f(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b): s.p[s.f(a)] = s.f(b)

def main():
    fdc = pd.read_csv('data/philhealth_fdc_2026-09-30.csv', dtype=str).fillna('')
    hosp = pd.read_csv('data/philhealth_hospitals_2026-09-30.csv', dtype=str).fillna('')
    recs = []
    for _, r in fdc.iterrows():
        recs.append(dict(center_id=f'FDC-{int(r.seq):04d}', facility_type='Freestanding dialysis clinic',
            hd_unit_evidence='PhilHealth FDC accreditation', name=r['name'], street=r.street, municipality=r.municipality,
            province=r.province, philhealth_region=r.region, sector=r.sector, tel_raw=r.tel, email_raw=r.email,
            philhealth_accredited='Yes', philhealth_list='FDC 2026-09-30', philhealth_seq=r.seq,
            philhealth_accreditation_expiry=r.accreditation_expiry, hospital_level='', hospital_beds=''))
    for _, r in hosp[hosp.category == 'LEVEL 3'].iterrows():
        recs.append(dict(center_id=f'HOSP-{int(r.seq):04d}', facility_type='Hospital-based dialysis unit',
            hd_unit_evidence='Level 3 hospital: DOH AO 2012-0012-A requires a dialysis facility (HD and/or PD)',
            name=r['name'], street=r.street, municipality=r.municipality, province=r.province, philhealth_region=r.region,
            sector=r.sector, tel_raw=r.tel, email_raw=r.email, philhealth_accredited='Yes (as hospital)',
            philhealth_list='HOSP 2026-09-30', philhealth_seq=r.seq, philhealth_accreditation_expiry=r.accreditation_expiry,
            hospital_level=r.category, hospital_beds=r.beds))
    df = pd.DataFrame(recs)
    df['admin_region'] = df.province.map(PROV2REG).fillna('')
    df['entity_type'] = [entity_type(n, s) if t.startswith('Free') else ('government hospital' if s == 'Government' else 'private hospital')
                         for n, s, t in zip(df.name, df.sector, df.facility_type)]
    df['name_key'] = df.name.map(norm_name)
    ph = df.tel_raw.map(phones)
    df['phones'] = ph.map(lambda l: '; '.join(p for p, _ in l))
    df['mobile_count'] = ph.map(lambda l: sum(k == 'mobile' for _, k in l))
    em = df.email_raw.map(emails)
    df['emails'] = em.map('; '.join)
    df['email_domains'] = em.map(lambda l: '; '.join(sorted({x.split('@')[1] for x in l})))
    df['corporate_email_domain'] = em.map(lambda l: '; '.join(sorted({x.split('@')[1] for x in l} - FREE_MAIL)))

    # Operator grouping (freestanding only): same normalised name, same corporate email domain, or same exact email
    dsu, f = DSU(), df[df.facility_type.str.startswith('Free')]
    for i, r in f.iterrows():
        dsu.f(i); dsu.u(i, 'N:' + r.name_key)
        for d in filter(None, r.corporate_email_domain.split('; ')): dsu.u(i, 'D:' + d)
        for e in filter(None, r.emails.split('; ')): dsu.u(i, 'E:' + e)
    groups = {}
    for i in f.index: groups.setdefault(dsu.f(i), []).append(i)
    df['operator_group'] = ''; df['operator_group_size'] = 1
    for members in groups.values():
        if len(members) < 2: continue
        names = df.loc[members, 'name_key'].value_counts()
        label = names.index[0]
        df.loc[members, 'operator_group'] = label
        df.loc[members, 'operator_group_size'] = len(members)
    cols = ['center_id','facility_type','name','operator_group','operator_group_size','entity_type','sector','street',
            'municipality','province','admin_region','philhealth_region','phones','mobile_count','emails','email_domains',
            'corporate_email_domain','philhealth_accredited','philhealth_list','philhealth_seq','philhealth_accreditation_expiry',
            'hospital_level','hospital_beds','hd_unit_evidence','tel_raw','email_raw','name_key']
    df[cols].to_csv('data/master_dialysis_centers.csv', index=False, quoting=csv.QUOTE_MINIMAL)
    print(len(df), 'rows'); print(df.facility_type.value_counts().to_string())
    print('unmapped provinces:', sorted(set(df.province[df.admin_region == ''])))
    g = df[df.operator_group != ''].groupby('operator_group').size().sort_values(ascending=False)
    print(len(g), 'multi-site groups; top:'); print(g.head(25).to_string())
    print(df.entity_type.value_counts().to_string())

if __name__ == '__main__':
    main()
