"""Build data/corporate/ownership.csv, data/corporate/financials_volume.csv and
data/market/market_context.csv from curated, source-cited records.

Every record below was transcribed from the cited document (raw copies under raw/corporate/ where
downloadable). NephroPlus Philippine subsidiaries are read from
raw/corporate/nephroplus/ph_subsidiaries.json (output of scripts/parse_nephroplus_rhp_subsidiaries.py).
value_type: reported = figure as published; derived = arithmetic on reported figures (formula in notes);
third_party_estimate = market-research estimate quoted in a filing.

Usage: python3 -I scripts/build_corporate_tables.py
"""
import csv, json, os, collections, datetime

A = '2026-11-14'
ENT = 'data/corporate/entities.csv'
RHP = 'https://www.chittorgarh.net/reports/ipo_notes/nephrocare-health-ipo-rhp.pdf'
GLEIF = 'https://api.gleif.org/api/v1/lei-records/'
SNC = 'https://www.philhealth.gov.ph/about_us/statsncharts/'
EURO17A = 'https://edge.pse.com.ph/openDiscViewer.do?edge_no=3f637e70c200074b64d70b69f0a3140b'
EURO17Q = 'https://edge.pse.com.ph/openDiscViewer.do?edge_no=1f54bb1294150b2764d70b69f0a3140b'
CBH = 'https://links.sgx.com/1.0.0/corporate-announcements/RJ4RRULTOEY26PV0/882292_CBH%20-%20Annual%20Report%202025.pdf'
GMA_BB1 = 'https://www.gmanetwork.com/news/news/nation/751153/b-braun-avitum-vows-cooperation-with-gov-t-after-being-linked-to-philhealth-s-irm-releases/story/'
GMA_BB2 = 'https://www.gmanetwork.com/news/news/nation/751850/lacson-points-out-alleged-excessive-philhealth-claims-of-b-braun-avitum/story/'
NSE = 'https://nsearchives.nseindia.com/corporate/'
MULTIBAGG = 'https://www.multibagg.ai/market-pulse/articles/nephrocare-philippines-dialysis-assets-2026-cmvqsg5xw001h2lpuo1yp4w5q'
CIRC = 'https://www.philhealth.gov.ph/circulars/'

ents = list(csv.DictReader(open(ENT, encoding='utf-8')))
def seqs_group(g):
    return ' '.join(e['seq'] for e in ents if e['operator_group'] == g)
def seqs_legal(sub):
    return ' '.join(e['seq'] for e in ents if sub.lower() in e['legal_entity_name_guess'].lower())
def seqs_name(sub):
    return ' '.join(e['seq'] for e in ents if sub.lower() in e['name'].lower())

# ------------------------------------------------------------------ ownership
O = []
def own(group, legal, role, country='PH', reg='', inc='', office='', people='', parent='', ult='', pct='',
        seqs='', notes='', conf='high', src='', access=A):
    O.append(dict(operator_group=group, legal_entity=legal, role=role, country=country, registry_id=reg,
                  incorporation_date=inc, registered_office=office, shareholders_directors_officers=people,
                  parent_company=parent, ultimate_owner=ult, ownership_pct=pct, linked_center_seqs=seqs,
                  notes=notes, confidence=conf, source_url=src, access_date=access))

# B. Braun
own('B. Braun Avitum', 'B. Braun Avitum Philippines, Inc.', 'operator (dialysis centers)',
    inc='2002-01-24 (incorporated as Philippine Renal Care, Inc.; later renamed)',
    parent='B. Braun group (company statement: wholly-owned subsidiary; parent not named in article)',
    ult='B. Braun Holding GmbH & Co. KG (Germany)', pct='100 (per company statement)',
    seqs=seqs_group('B. Braun Avitum'),
    notes='Company statement Aug 2020: owns and manages 25 dialysis centers in Luzon; B. Braun Medical Supplies, Inc. registered with SEC 11 Dec 1985. SEC reg. no. of the Avitum entity not found publicly.',
    src=GMA_BB1)
own('B. Braun Avitum', 'B. Braun Medical Supplies Inc.', 'sister company / PH distributor of B. Braun products',
    reg='SEC 0000130178; LEI 529900UZ0B2A7SEU1J14', inc='1985-12-10 (GLEIF; GMA: 11 Dec 1985)', office='Taguig City (GLEIF legal address)',
    parent='B. Braun SE (LEI 529900W8MHYEV82GT965)', ult='B. Braun Holding GmbH & Co. KG (LEI 5299004E1B0DK73UIY59)',
    notes='Parent relationships from GLEIF level-2 data; raw JSON raw/corporate/gleif_bbraun_medical_supplies.json',
    src=GLEIF + '529900UZ0B2A7SEU1J14')
# Fresenius
own('Fresenius Kidney Care', 'Fresenius Medical Care Philippines, Inc.', 'PH holding/operating company',
    reg='SEC A200108421; LEI 529900YTY5Q7H4K14X02', inc='2001-06-17/18 (GLEIF entity creation date)',
    office='18/F Aeon Center, Alabang-Zapote Road cor. North Bridgeway, Alabang, Muntinlupa 1781',
    parent='Fresenius Medical Care AG (LEI 549300CP8NY40UP89Q40)', ult='Fresenius Medical Care AG (Germany; NYSE/FWB listed)',
    seqs=seqs_group('Fresenius Kidney Care'),
    notes='Fresenius PH site (accessed 2026-11-14): "operates 24 dialysis centers locally"; footer names Fresenius Medical Care Philippines, Inc. and FMC Renalcare Corp.; raw JSON raw/corporate/gleif_fmc_philippines.json',
    src=GLEIF + '529900YTY5Q7H4K14X02')
own('Fresenius Kidney Care', 'FMC Renalcare Corp. (PhilHealth: "FMC RENAL CARE CORP.")', 'clinic operating subsidiary',
    parent='Fresenius Medical Care group', ult='Fresenius Medical Care AG', seqs=seqs_name('FMC RENAL'),
    notes='Named in footer of freseniusmedicalcare.com/en-ph; accredited as an FDC in Ormoc (seq 866). SEC no./incorporation date not public.',
    src='https://freseniusmedicalcare.com/en-ph/clinics/')
own('Fresenius Kidney Care', 'Asia Renal Care Corp.; Mindanao Renal Care, Inc.', 'reported clinic operating subsidiaries',
    parent='Fresenius Medical Care Philippines, Inc.', ult='Fresenius Medical Care AG', conf='low',
    notes='Named only in a UNI Global Union page seen in search results (page itself not retrievable - redirect loop). FMC acquired Singapore-based Asia Renal Care in 2006-07 (Aerztezeitung).',
    src='https://uniglobalunion.org/?p=11408')
# NephroPlus
own('NephroPlus', 'Nephrocare Health Services Ltd (brand NephroPlus)', 'ultimate parent', country='IN',
    reg='CIN U85100TG2009PLC066359', inc='2009-12-18', office='5th Floor, D Block, iLabs Centre, Madhapur, Hyderabad 500081, India',
    people='Promoters: Vikram Vuppala (Chairman & MD), Bessemer Venture Partners Trust, Edoras Investment Holdings Pte. Ltd., Healthcare Parent Limited, Investcorp Private Equity Fund II, Investcorp Growth Opportunity Fund; other selling shareholders incl. International Finance Corporation, 360 One funds',
    ult='listed on NSE/BSE (symbol NEPHROPLUS) after Dec-2025 IPO; promoter group above', seqs=seqs_group('NephroPlus'),
    notes='RHP dated 2 Dec 2025: 41 PH clinics in 30 cities through 18 subsidiaries, 2,276 PH patients (30 Sep 2025); entered PH Oct 2020 via Royal Care Dialysis Centre Inc. + Asialife Healthcare Corp.',
    src=RHP)
own('NephroPlus', 'Nephrocare Health Services International Pte. Ltd', 'intermediate holding company', country='SG',
    parent='Nephrocare Health Services Ltd', ult='Nephrocare Health Services Ltd', pct='100',
    notes='Holds 1,537,768 of 1,537,770 shares of NHCS Philippines', src=RHP)
subs = json.load(open('raw/corporate/nephroplus/ph_subsidiaries.json', encoding='utf-8'))
for s in subs:
    nm = s['name'].replace('371 ', '').strip()
    if not nm:
        continue  # Saudi entities parsed from the same section
    is_parent = nm.startswith('Nephrocare Health Care Services')
    key = nm.split(' Inc')[0].split(' Corporation')[0].split(' Incorporation')[0]
    linked = seqs_legal(key)
    if nm.startswith('Nephro Alliance'):
        linked = seqs_legal('Nephro Alliance')
    extra = {'People': ('474', ''), 'St. Margareth': ('389', 'site accredited under NHCS-PH at this subsidiary\'s registered address. '),
             'Dialysis Asia': ('489', 'site accredited under NHCS-PH at this subsidiary\'s registered address (Gate 3 Plaza Mall, Taguig). '),
             'Anram': ('457', 'probable: NHCS-PH site at 132 Timog Ave QC; Anram registered at GMPC Bldg, Timog Ave. ')}
    xnote = ''
    for k, (sq, xn) in extra.items():
        if nm.startswith(k):
            linked, xnote = sq, xn
    try:
        iso = datetime.datetime.strptime(s['incorporated'].replace(' 0', ' '), '%B %d, %Y').date().isoformat()
    except ValueError:
        iso = s['incorporated']
    people = s['shareholders'].replace('Nephrocare Health Care Services, (', 'Nephrocare Health Care Services, Philippines Inc. (').replace('Nephrocare Health care services, (', 'Nephrocare Health Care Services, Philippines Inc. (')
    rev = s['revenue_inr_m_fy25_fy24_fy23']
    own('NephroPlus', nm, 'PH holding & operating company' if is_parent else 'PH subsidiary (dialysis center operator)',
        reg='SEC (number not disclosed in RHP)', inc=iso + (' (as Tech Care Center, Inc.; renamed 28 Oct 2022)' if is_parent else ''),
        office=s['registered_office'], people='Shareholders (no. of shares): ' + people,
        parent='Nephrocare Health Services International Pte. Ltd' if is_parent else 'Nephrocare Health Care Services, Philippines Inc.',
        ult='Nephrocare Health Services Ltd (India)', pct='100 (nominee single shares held by officers)',
        seqs=linked,
        notes=xnote + f"Paid-up capital PHP {s['paidup_capital_php'] or 'n/a'}; authorized PHP {s['authorized_capital_php'] or 'n/a'}. Revenue FY25/FY24/FY23 (INR m): {'/'.join(rev)}",
        src=RHP)
own('NephroPlus', 'Royal Care Dialysis Centre Inc. (RCDC) and Asialife Healthcare Corp.', 'acquired chain (entry vehicle)',
    people='Founder of RCDC: Sunil Chellani (The Ken, 2020)', parent='Nephrocare Health Care Services, Philippines Inc. (51% Oct 2020; 100% by 2022)',
    ult='Nephrocare Health Services Ltd', pct='100 (from 2022)', conf='medium',
    notes='6 clinics / 292 patients at entry (RHP). RCDC no longer in the RHP subsidiary list (likely merged into NHCS-PH - not confirmed).',
    src=RHP)
own('NephroPlus', 'Anram Medical Group Inc. - former owners', 'former shareholders (sellers)',
    people='Anna Teresa G. Valdes; Ramon V. Valdes; Theresa Khristine M. Garcia; Florentine R. Lirag; Victoria V. Valdes',
    notes='Share purchase agreement dated 1 Mar 2022 with NHCS-PH', src=RHP)
own('NephroPlus', 'Cadiz Dialysis Hub Inc. - former owners', 'former shareholders (sellers)',
    people='Mary Ann L. Olayvar; Jonathan A. Olayvar; Rafael A. Ilagan; Mario Jacinto A. Rapadas; Ronaldo B. Ordoney; Johnnel Sucaldito; Jose M. (surname truncated in RHP)',
    notes='Share purchase agreement dated 31 May 2022 with NHCS-PH', seqs=seqs_name('CADIZ DIALYSIS HUB'), src=RHP)
# NephroPlus asset / business acquisitions (seller entity -> buyer NHCS-PH)
deals = [
    ('Cabuyao Kidney Care Dialysis Centre', '2025-06-24', 'INR 40.11m purchase consideration', '630', RHP),
    ('Santiago City Kidney Centre Inc.', '2025-07-01', 'INR 60.50m', '114', RHP),
    ('Passion Healthcare Phils Inc.', '2025-07-24', 'INR 174.29m', '338', RHP),
    ('Cordillera Kidney Specialist Inc.', '2025-10-02', 'INR 75.28m', '', RHP),
    ('Zambales Dialysis & Kidney Center Inc.', '2025-10-06', 'INR 58.15m', '305 302', RHP),
    ('Dialysis Center of Cauayan Inc. (DCCI)', '2026-01-26', 'PHP 37,721,600', '91', NSE + 'NEPHROCARE1_27012026221639_Intimation_under_Reg_30_dt_270102026_signed.pdf'),
    ('Laurel Kidney Care Dialysis Centre Inc.', '2026-02-12', 'PHP 49,400,000', '677', 'https://bsmedia.business-standard.com/_media/bs/data/announcements/bse/12022026/57d2cea1-4a37-41bc-8acb-abb930d6ab55.pdf'),
    ('Northern Mindanao Dialysis Clinic Inc.', '2026-05 (ATA disclosed 26 May 2026)', 'PHP 27,400,000', '911', NSE + 'NEPHROCARE1_26052026201218_Intimation_under_Reg_30_f.pdf'),
    ('Aliaga Hemodialysis Centre Inc.', '2026-05 (ATA disclosed 26 May 2026)', 'PHP 44,800,000', '211', NSE + 'NEPHROCARE1_26052026201218_Intimation_under_Reg_30_f.pdf'),
    ('Orani Hemodialysis Center Inc.', '2026-05-12', 'PHP 89.6m', '144', MULTIBAGG),
    ('Inocentes Dialysis Clinic', '2026-06 (reported 4 Jun 2026)', 'PHP ~30m', '446', 'https://www.sahi.com/news/nephroplus-acquires-inocentes-dialysis-assets-for-php-30m-boosting-international-revenue-to-42-5673385-PE1_'),
    ('Amica Healthcare System Corp.', '2026-06-09', 'PHP 32.64m', '547', MULTIBAGG),
    ('Pag-Asa Dialysis and Diagnostic Center (Ipil)', '2026-06-22', 'PHP 80.64m', '898', 'https://www.angelone.in/news/stocks/nephroplus-share-price-in-focus-philippines-subsidiary-acquires-dialysis-centre-assets'),
    ('(seller not named) Orion, Bataan dialysis assets', '2026-06-24', 'PHP 151.6m', '135', MULTIBAGG),
    ('Juan Nephro Dialysis Center (Davao City)', '2026-08-12', 'PHP 71,800,000', '940', NSE + 'NEPHROCARE1_13082026111757_intimation.pdf'),
    ('Assumption Dialysis Center (Abuyog, Leyte)', '2026-08-17', 'PHP 75m', '858', MULTIBAGG),
    ('Renal One Dialysis Corp (Plaridel, Bulacan site)', '2026-09-14', 'PHP 67.2m', '198', MULTIBAGG),
]
for seller, d, val, sq, src in deals:
    own('NephroPlus', seller, 'seller of dialysis-center business/assets to NHCS-PH',
        parent='(site now operated by) Nephrocare Health Care Services, Philippines Inc.', ult='Nephrocare Health Services Ltd',
        seqs=sq, notes=f'Business/asset transfer dated {d}; consideration {val}. Asset deal - seller entity itself not acquired.',
        conf='high' if ('nseindia' in src or 'bseindia' in src or 'business-standard' in src or src == RHP) else 'medium', src=src)
# Hemotek / Euro-Med
own('Hemotek', 'Hemotek Renal Center, Inc.', 'operator (dialysis centers)', inc='2008-06 (17-A: incorporated June 2008)',
    people='Chairman: Enrique Raymond Yap (MarketScreener); COO: Dr. Sonny L. Antonio (PR Newswire 2024)',
    parent='Euro-Med Laboratories Phil., Inc.', ult='U.S. Automotive Co., Inc. (via Euro-Med)', pct='100',
    seqs=seqs_group('Hemotek'), notes='First branch Malate, Manila opened 4 Feb 2008 (JobStreet profile). Branch/machine counts not disclosed in 17-A pages reviewed.',
    src=EURO17A)
own('Hemotek', 'Euro-Med Laboratories Phil., Inc.', 'listed parent (PSE: EURO)', reg='SEC-registered 1988-01-29',
    inc='1988-01-29', people='Top holders (31 Mar 2026): U.S. Automotive Co., Inc. 2,401,747,112 sh; USAUTOCO, Inc. 855,505,147 sh (20.80%); Philippine Trust Co.; Yap family members (Johnny C., Emilio C. III, Nichol C., Enrique Raymond I., Michael Vincent Y.)',
    parent='U.S. Automotive Co., Inc.', ult='U.S. Automotive Co., Inc. (PH; Yap family-linked per stockholder list)', pct='58.41 (17-A text); 58.06 in top-20 table',
    notes='17-A FY2025 (amended 27 Apr 2026), scanned PDF read visually; also owns CafeFrance Corp. (100%).', src=EURO17A)
# Clearbridge
own('Clearbridge Health', 'Clearbridge Medical (Philippines) Inc. (formerly Marzan Health Care Inc.)', 'operator (multi-specialty centre with renal dialysis, Manila; Clearbridge Dialysis Center, Quezon City)',
    parent='Clearbridge Health (Philippines) Inc.', ult='Clearbridge Health Limited (SGX Catalist: 1H3), Singapore', pct='65',
    seqs=seqs_group('Clearbridge Health'), notes='65% acquired Jan 2018 for PHP 69.6m (The Edge Singapore).', src=CBH)
# Healthway / AC Health
own('Healthway (AC Health)', 'Healthway Philippines, Inc.', 'clinic & hospital network (Healthway Medical clinics; Healthway QualiMed hospitals)',
    parent='Ayala Healthcare Holdings, Inc. (AC Health)', ult='Ayala Corporation (PSE: AC)', pct='~94 (Ayala stake in Healthway, Dec 2023 report)',
    seqs=seqs_group('Healthway (AC Health)'), conf='medium',
    notes='AC Health via HPI acquired majority of Mercado General Hospital Inc. (QualiMed) Feb 2021. Healthway committed PHP 200m to Iloilo dialysis PPP (12 hospitals, Nov 2025). Site-level licensee of accredited FDCs not confirmed.',
    src='https://mb.com.ph/2023/12/10/ayala-boosts-stake-in-healthway-to-94')
# MedLine / Nephromed / Avitus / MMG
own('MedLine dialysis', 'MedLine (dialysis chain & franchisor)', 'operator/franchisor', people='Established 2015 by the family of Alexander and Sonny Lim',
    parent='', ult='Lim family; growth capital from ARQCapital (2019)', seqs=seqs_name('MEDLINE') + ' ' + seqs_name('MED LINE'), conf='low',
    notes='Franchise programme designed with Francorp; legal entity of PhilHealth-listed "MEDLINE/MED LINE DIALYSIS CENTER" sites not confirmed as MedLine.',
    src='https://philstar.com/business/2019/11/17/1969362/arqcapital-boosts-medline-bid-expand-dialysis-centers')
own('Nephromed Asia', 'Nephromed Asia Medical Group Incorporated', 'operator', people='Founder/Chairman-CEO: Jylberd L. Nabor (ex-Roche sales manager)',
    seqs=seqs_group('Nephromed Asia'), conf='medium', notes='2019: 6 company-owned centers + 2 under construction (Manila Bulletin, via search snippet; page 403 to fetch).',
    src='https://mb.com.ph/2019/06/11/the-game-changer')
own('Avitus', 'Avitus Kidney Care and Dialysis Center Corporation (+ Avitus Pangasinan Dialysis Center Corp.; Avitus Davao Dialysis Center Corp.)', 'operator',
    seqs=seqs_group('Avitus'), conf='low', notes='Owners/officers not found publicly. JobStreet: independent dialysis provider, also supplier/distributor of medical equipment. Listed by F&S (NephroPlus RHP) among top-5 standalone chains.',
    src='https://ph.jobstreet.com/companies/avitus-kidney-care-and-dialysis-center-corporation-168553584420617')
own('Medical Mission Group (cooperative network)', 'Medical Mission Group hospital & health services cooperatives (Metro Manila East, Sorsogon, Bohol/Cebu, Occidental Mindoro, Palawan, federation)',
    'cooperative operators', parent='', ult='member-owned cooperatives (CDA-registered)', seqs=' '.join(sorted(set((seqs_group('Medical Mission Group (cooperative network)') + ' ' + seqs_name('PREMIER MEDICAL GROUP MULTIPURPOSE') + ' ' + seqs_name('MEDICAL MISSION GROUP MULTIPURPOSE')).split()), key=int)),
    conf='medium', notes='CDA registration numbers not retrieved.', src='https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf')

# Cooperatives: CDA registration numbers from the CDA "List of Cooperatives as of December 2024" PDF
CDA = 'https://cda.gov.ph/wp-content/uploads/2025/08/For-posting_2024-data.pdf'
for nm, reg, addr, status, sq, conf, nt in [
    ('Vizcaya Kidney Care Center Cooperative', '9520-02005397', '97 Burgos Street, Quirino, Solano, Nueva Vizcaya', 'Compliant (primary, health service)', '107 108', 'high', ''),
    ('Medical Mission Group Metro Manila East Hospital & Health Services Cooperative', '9520-16004290', 'Mission Hospital, Km. 17 Ortigas Ave. Ext., Rosario, Pasig', 'Compliant (primary, health service)', '413', 'high', ''),
    ('Medical Mission Group Hospitals and Health Services Cooperative of the Philippines Federation (MMGHHSCPF)', '9520-16015121', 'Mission Medical Plaza, Km.17 Ortigas Ave. Ext., Rosario, Pasig', 'Compliant (secondary, federation)', '301 803', 'high', 'PhilHealth lists the federation as accredited operator of sites in San Narciso, Zambales and Ubay, Bohol'),
    ('Palawan Medical Mission Group Multipurpose Cooperative (PMMGMPC)', '9520-04006983', 'cor. Burgos and Mabini Sts, Puerto Princesa', 'Compliant (primary, multipurpose)', '713', 'high', ''),
    ('Sorsogon Medical Mission Group Hospital and Health Services Cooperative', '9520-05010541', 'Maharlika Highway, Pangpang, Sorsogon City', 'Compliant (primary, health service)', '748 749 750', 'high', ''),
    ('Cebu CFI Community Cooperative', '9520-07000198', 'Cebu Capitol, Cebu City', 'Compliant (primary, multipurpose)', '830', 'high', 'Cebu provincial-employee (CFI) cooperative'),
    ('Mindoro Occidental Premier Medical Group Multipurpose Cooperative', '', '', 'not found by that name in CDA 2024 list', '706', 'low', 'closest CDA entry: Mindoro Occidental Medical Mission Group Health Service Cooperative (MOMMGHSC) 9520-1040000000025147, Diego Silang St, San Jose - same street as PhilHealth address; identity not confirmed'),
]:
    own('Cooperative', nm, 'cooperative operator', reg='CDA ' + reg if reg else '', office=addr, ult='member-owned cooperative',
        seqs=sq, conf=conf, notes=('CDA status 2024: ' + status + '. ' + nt).strip(), src=CDA)

os.makedirs('data/corporate', exist_ok=True)
with open('data/corporate/ownership.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(O[0].keys())); w.writeheader(); w.writerows(O)

# ------------------------------------------------------------------ financials / volume (entity level)
F = []
def fin(ent, metric, value, unit, period, vtype='reported', notes='', src='', seqs=''):
    F.append(dict(entity_or_center=ent, linked_center_seqs=seqs, metric=metric, value=value, unit=unit, period=period,
                  value_type=vtype, notes=notes, source_url=src, access_date=A))
np_seqs = seqs_group('NephroPlus')
own_seqs = {o['legal_entity']: o['linked_center_seqs'] for o in O}
for s in subs:
    nm = s['name'].replace('371 ', '').strip()
    if not nm or nm.startswith('Nephro Alliance'):
        continue
    for val, per in zip(s['revenue_inr_m_fy25_fy24_fy23'], ['FY2025 (Apr24-Mar25)', 'FY2024 (Apr23-Mar24)', 'FY2023 (Apr22-Mar23)']):
        if val and val not in ('N.A.', 'NA', '-'):
            fin(nm, 'revenue_from_operations', val, 'INR million', per, notes='standalone subsidiary figure as restated in RHP; not PHP', src=RHP, seqs=own_seqs.get(nm, ''))
    pat = s['pat_inr_m_fy25_fy24_fy23'][0]
    if pat and pat not in ('N.A.', 'NA'):
        fin(nm, 'profit_after_tax', pat.replace('(', '-').replace(')', ''), 'INR million', 'FY2025 (Apr24-Mar25)', src=RHP, seqs=own_seqs.get(nm, ''))
fin('NephroPlus group', 'revenue_from_operations_outside_india (Philippines + Uzbekistan)', '2403.10', 'INR million', 'FY2025', notes='31.79% of group revenue; not split PH vs Uzbekistan', src=RHP)
fin('NephroPlus group', 'revenue_from_operations_outside_india (Philippines + Uzbekistan)', '1346.16', 'INR million', 'FY2024', notes='23.78% of group revenue', src=RHP)
fin('NephroPlus group', 'revenue_from_operations_outside_india (Philippines + Uzbekistan)', '511.84', 'INR million', 'FY2023', notes='11.70% of group revenue', src=RHP)
fin('NephroPlus group', 'revenue_from_operations_outside_india (Philippines + Uzbekistan)', '1892.18', 'INR million', 'H1 FY2026 (Apr-Sep 2025)', notes='39.96% of group revenue', src=RHP)
fin('NephroPlus Philippines', 'clinics', '41', 'clinics', '2025-09-30', notes='41 clinics in 30 cities via 18 subsidiaries; all standalone, leased premises', src=RHP, seqs=np_seqs)
fin('NephroPlus Philippines', 'patients', '2276', 'patients', '2025-09-30', src=RHP)
fin('NephroPlus Philippines', 'clinics', '6', 'clinics', '2020-10 (entry)', notes='RCDC + Asialife; 292 patients', src=RHP)
fin('NephroPlus Philippines', 'annual_treatments', '>100000', 'treatments/year', '2023', notes='"surpassing 100,000 annual treatments and reaching a 21 clinics network"', src=RHP)
fin('NephroPlus Philippines', 'clinics', '36', 'clinics', '2025-02-18', notes='after acquiring 7 clinics; ~2,000 patients', src='https://nephroplus.com/press/nephroplus-expands-its-footprint-in-the-philippines-with-acquisition-of-7-dialysis-centers')
fin('NephroPlus Philippines', 'clinics', '39', 'clinics', '2025-08', notes='~2,500 patients monthly; >600 employees; ~USD 30m invested since 2020; target 150 clinics by 2028', src='https://tribune.net.ph/2025/08/11/nephroplus-to-open-150-dialysis-clinics-in-phl-by-2028')
fin('NephroPlus Philippines', 'dialysis_stations', '686', 'stations', '2026-07-14', notes='50 clinics; ~2,866 patients per month; 50th clinic in Orion, Bataan', src='https://tribune.net.ph/2026/07/14/dialysis-provider-opens-50th-clinic')
fin('NephroPlus Philippines', 'clinics', '53', 'facilities', '2026-09', notes='incl. 8 outside Luzon (Daily Tribune 4 Sep 2026, via search snippet; page returned HTTP 500)', src='https://tribune.net.ph/2026/09/04/nephroplus-expands-dialysis-network')
fin('NephroPlus Philippines (Noveleta, Cavite greenfield)', 'dialysis_machines', '12', 'machines', '2025-08 (planned)', notes='up to 75 patients monthly; pending BOI approval', src='https://tribune.net.ph/2025/08/11/nephroplus-to-open-150-dialysis-clinics-in-phl-by-2028', seqs='583')
for seller, d, val, sq, src in deals:
    fin('Nephrocare Health Care Services, Philippines Inc. <- ' + seller, 'acquisition_consideration', val.split(' ', 1)[1] if ' ' in val else val,
        val.split(' ')[0] if val.split(' ')[0] in ('PHP', 'INR') else '', d, notes='business/asset transfer price (site-level transaction value)', src=src, seqs=sq)
# B. Braun
bb = seqs_group('B. Braun Avitum')
fin('B. Braun Avitum Philippines, Inc.', 'philhealth_payments', '811', 'PHP million', '2015-2018', notes='figure cited by Sen. Lacson at Senate hearing (18 Aug 2020)', src=GMA_BB2, seqs=bb)
fin('B. Braun Avitum Philippines, Inc.', 'philhealth_IRM_cash_advance', '45.176', 'PHP million', '2020-04-23 to 2020-05-05', notes='Interim Reimbursement Mechanism releases; Benguet branch PHP 11.38m, Tondo ~PHP 15m (Inquirer)', src=GMA_BB1, seqs=bb)
fin('B. Braun Avitum Philippines, Inc.', 'dialysis_centers', '25', 'centers', '2020-08', notes='"owns and manages 25 dialysis centers across Luzon"', src=GMA_BB1, seqs=bb)
fin('B. Braun Avitum - Quezon City branch', 'dialysis_machines', '15', 'machines', '2018', notes='sessions-to-capacity ratio 133.78% vs PhilHealth 90% threshold (per Sen. Lacson)', src=GMA_BB2)
fin('B. Braun Avitum Philippines, Inc.', 'philhealth_accredited_sites', str(len(bb.split())), 'sites', '2026-09-30', vtype='derived', notes='count of PhilHealth FDC list rows linked to B. Braun', src='https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf', seqs=bb)
# Fresenius
fs = seqs_group('Fresenius Kidney Care')
fin('Fresenius Kidney Care (Philippines)', 'dialysis_centers', '24', 'centers', 'as published (undated) - accessed 2026-11-14', src='https://freseniusmedicalcare.com/en-ph/clinics/', seqs=fs)
fin('Fresenius Kidney Care (Philippines)', 'philhealth_accredited_sites', str(len(fs.split())), 'sites', '2026-09-30', vtype='derived', src='https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf', seqs=fs)
# Hemotek / Euro-Med
fin('Euro-Med Laboratories Phil., Inc. (consolidated)', 'sale_of_services', '443393751', 'PHP', 'H1 2026 (Jan-Jun)', notes='"Sale of services" line; services = Hemotek dialysis and possibly CafeFrance food services - segment split not disclosed in 17-Q', src=EURO17Q, seqs=seqs_group('Hemotek'))
fin('Euro-Med Laboratories Phil., Inc. (consolidated)', 'sale_of_services', '295432785', 'PHP', 'H1 2025 (Jan-Jun)', notes='as above (comparative)', src=EURO17Q, seqs=seqs_group('Hemotek'))
fin('Hemotek Renal Center, Inc.', 'philhealth_accredited_sites', str(len(seqs_group('Hemotek').split())), 'sites', '2026-09-30', vtype='derived', src='https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf', seqs=seqs_group('Hemotek'))
# Clearbridge
fin('Clearbridge Health Ltd - Philippines medical clinics/centres', 'revenue', '3.34', 'SGD million', 'FY2025', notes='+53.8% y/y, driven by renal care services (new dialysis centre) and PhilHealth rate increases', src=CBH, seqs=seqs_group('Clearbridge Health'))
fin('Clearbridge Health Ltd - Philippines medical clinics/centres', 'revenue', '2.17', 'SGD million', 'FY2024', src=CBH, seqs=seqs_group('Clearbridge Health'))
# Other capacity / volume facts
fin('National Kidney and Transplant Institute (NKTI)', 'philhealth_hd_claims_paid', '161', 'PHP million', '2025-01-01 to 2025-05-21', notes='total PhilHealth claims to NKTI same period PHP 592m (hospital-based, not an FDC)', src='https://tribune.net.ph/2025/05/28/philhealth-expands-dialysis-coverage-as-demand-for-treatment-surges')
fin('NKTI Legacy Building (hemodialysis hub, under construction)', 'dialysis_machines', '200', 'machines (planned)', 'target completion Dec 2027', notes='PHP 2.8bn, 13 storeys, NKTI compound Quezon City (DOH/DPWH)', src='https://www.philstar.com/other-sections/daily-bread/2026/06/26/2537993/marcos-eyes-early-completion-largest-dialysis-center-southeast-asia')
fin('MedLine dialysis', 'franchise_pipeline', '20', 'franchises planned in 12 months', '2019-11', notes='adding 1-2 franchises per month since 2018', src='https://philstar.com/business/2019/11/17/1969362/arqcapital-boosts-medline-bid-expand-dialysis-centers')
# Derived site counts for every multi-site group in the PhilHealth list
cnt = collections.Counter(e['operator_group'] for e in ents if e['operator_group'])
for g, c in cnt.most_common():
    if g in ('B. Braun Avitum', 'Fresenius Kidney Care', 'Hemotek'):
        continue
    fin(g, 'philhealth_accredited_sites', str(c), 'sites', '2026-09-30', vtype='derived', notes='rows in PhilHealth FDC list linked to this group (see entities.csv for basis/confidence)', src='https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf', seqs=seqs_group(g))
with open('data/corporate/financials_volume.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(F[0].keys())); w.writeheader(); w.writerows(F)

# ------------------------------------------------------------------ market context (national)
M = []
def mk(metric, value, unit, period, vtype='reported', notes='', src='', geo='Philippines'):
    M.append(dict(metric=metric, value=value, unit=unit, period=period, geography=geo, value_type=vtype, notes=notes, source_url=src, access_date=A))
hd = {  # RVS 90935 hemodialysis procedure: (amount PHP, claims count, file)
    '2017': ('8375307755', '1653491', 'snc2017.pdf'), '2018': ('10802713853.22', '2221430', 'snc2018.pdf'),
    '2019': ('10637239600', '2187846', 'snc2019_r1.pdf'), '2020': ('12576077490', '2685161', 'snc2020_v1.pdf'),
    '2021': ('14014183017', '2907447', 'snc2021_v1.pdf'), '2022': ('17339014971', '3625328', 'snc2022_v2.pdf'),
    '2023': ('17435331944', '3627350', 'SNC_2023_20240306.pdf'), '2024': ('28162018203', '5190286', 'SNC_2024_20250523_v1.3.pdf'),
    '2025': ('71676672571', '7216745', 'SNC_2025_20260623.pdf'), 'H1 2026 (Jan-Jun)': ('48728288954', '5409112', 'SNC2026_1stSem.pdf')}
for per, (amt, n, f) in hd.items():
    mk('philhealth_hemodialysis_claims_paid_amount', amt, 'PHP', per, notes='RVS 90935 Hemodialysis Procedure, all facility types; Stats & Charts top procedures table', src=SNC + f)
    mk('philhealth_hemodialysis_claims_paid_count', n, 'claims', per, notes='claims count, not sessions or patients', src=SNC + f)
    mk('philhealth_hemodialysis_avg_paid_per_claim', str(round(float(amt) / int(n))), 'PHP per claim', per, vtype='derived', notes='amount / count; exceeds per-session rate in some years, so a claim can cover >1 session', src=SNC + f)
fdc = {'2017': ('3639084838', '538401', 'snc2017.pdf'), '2018': ('4972951415', '608651', 'snc2018.pdf'),
       '2019': ('4798226552', '586942', 'snc2019_r1.pdf'), '2020': ('5889695293', '816267', 'snc2020_v1.pdf'),
       '2021': ('7018368189', '887698', 'snc2021_v1.pdf'), '2022': ('8484695357', '1066127', 'snc2022_v2.pdf'),
       '2023': ('8806694853', '1117882', 'SNC_2023_20240306.pdf'), '2024': ('14390655431', '1729646', 'SNC_2024_20250523_v1.3.pdf'),
       '2025': ('36830623179', '2602570', 'SNC_2025_20260623.pdf'), 'H1 2026 (Jan-Jun)': ('26086224204', '2264356', 'SNC2026_1stSem.pdf')}
for per, (amt, n, f) in fdc.items():
    mk('philhealth_claims_paid_to_freestanding_dialysis_clinics_amount', amt, 'PHP', per, notes='all benefits paid to facility type "Free-Standing Dialysis Clinic"', src=SNC + f)
    mk('philhealth_claims_paid_to_freestanding_dialysis_clinics_count', n, 'claims', per, src=SNC + f)
    if per in hd:
        mk('fdc_share_of_hemodialysis_claims_amount', str(round(100 * float(amt) / float(hd[per][0]), 1)), 'percent', per, vtype='derived',
           notes='FDC claims amount / RVS 90935 HD claims amount (FDC claims may include minor non-HD items)', src=SNC + f)
acc = {'2019': ('5', '389', 'snc2019_r1.pdf'), '2020': ('6', '427', 'snc2020_v1.pdf'), '2021': ('8', '484', 'snc2021_v1.pdf'),
       '2022': ('16', '543', 'snc2022_v2.pdf'), '2023': ('27', '597', 'SNC_2023_20240306.pdf'), '2024': ('31', '674', 'SNC_2024_20250523_v1.3.pdf'),
       '2025': ('37', '780', 'SNC_2025_20260623.pdf'), 'H1 2026 (as of 30 Jun)': ('40', '891', 'SNC2026_1stSem.pdf')}
for per, (g, p, f) in acc.items():
    mk('philhealth_accredited_freestanding_dialysis_clinics_government', g, 'facilities', per, src=SNC + f)
    mk('philhealth_accredited_freestanding_dialysis_clinics_private', p, 'facilities', per, src=SNC + f)
mk('philhealth_accredited_freestanding_dialysis_clinics_total', '1012', 'facilities', '2026-09-30', notes='41 government / 971 private (rows in PhilHealth list as of 30 Sep 2026)', src='https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf')
mk('philhealth_z_benefit_peritoneal_dialysis_claims_amount', '742441699', 'PHP', '2025', notes='38,317 claims', src=SNC + 'SNC_2025_20260623.pdf')
mk('philhealth_z_benefit_peritoneal_dialysis_claims_amount', '528918034', 'PHP', 'H1 2026 (Jan-Jun)', notes='22,422 claims', src=SNC + 'SNC2026_1stSem.pdf')
mk('philhealth_z_benefit_kidney_transplantation_claims_amount', '303682000', 'PHP', '2025', notes='539 claims', src=SNC + 'SNC_2025_20260623.pdf')
mk('philhealth_z_benefit_kidney_transplantation_claims_amount', '138905000', 'PHP', 'H1 2026 (Jan-Jun)', notes='142 claims', src=SNC + 'SNC2026_1stSem.pdf')
mk('philhealth_hemodialysis_claims_paid_amount (press)', '48.76', 'PHP billion', 'H1 2026 (Jan-Jun)', notes='press figure; total claims PHP 210.09bn; matches SNC within rounding', src='https://www.philstar.com/nation/2026/09/05/2554071/philhealth-pays-p210-billion-medical-claims')
mk('philhealth_hemodialysis_claims_paid_amount (press)', '~27', 'PHP billion', 'H1 2025 (Jan-Jun)', notes='>2 million claims; "almost equal to the P28 billion for all of 2024" (PNA/GMA via search results)', src='https://www.gmanetwork.com/news/topstories/nation/950268/philhealth-kidney-disease-heart-conditions-outpatient-care/story/')
for per, rate, f in [('2023', 2600, 'SNC_2023_20240306.pdf'), ('2025', 6350, 'SNC_2025_20260623.pdf'), ('H1 2026 (Jan-Jun)', 6350, 'SNC2026_1stSem.pdf')]:
    sess = float(hd[per][0]) / rate
    yr = sess * (2 if per.startswith('H1') else 1)
    mk('estimated_philhealth_paid_hd_sessions', str(round(sess)), 'sessions', per, vtype='estimate',
       notes=f'HD claims amount / PHP {rate} package rate (assumes every claim paid at full package; ignores partial/denied claims)', src=SNC + f)
    mk('estimated_patient_years_on_hd_at_156_sessions', str(round(yr / 156)), 'patient-years', per, vtype='estimate',
       notes='estimated sessions (annualised) / 156; a lower bound on patients if many dialyse <3x/week', src=SNC + f)
# package rate history
rates = [
    ('2015-07-28', '2600', '2250 facility + 350 professional fee', '90 (45 regular + 45 additional) per calendar year', 'PhilHealth Circular 022-2015 / 024-2015 (Rev.1) New PhilHealth Dialysis Package', CIRC + '2015/circ022-2015.pdf'),
    ('CY2020', '2600', '', 'max 144 (temporary, COVID-era)', 'PhilHealth Circular 2021-0002', CIRC + '2021/circ2021-0002.pdf'),
    ('CY2021', '2600', '', 'max 144 (temporary)', 'PhilHealth Circular 2021-0009', CIRC + '2021/circ2021-0009.pdf'),
    ('CY2022', '2600', '', 'max 144 (temporary; 91st-144th outpatient only)', 'PhilHealth Circular 2022-0017', CIRC + '2022/circ2022-0017.pdf'),
    ('CY2023 onwards (published 22 Jun 2023)', '2600', '2250 facility + 350 professional fee', '156 (institutionalized; 45-day limit not applicable)', 'PhilHealth Circular 2023-0009', CIRC + '2023/PC2023-0009.pdf'),
    ('2024-07-01', '4000', '3650 facility + 350 professional fee', '156', 'PhilHealth Circular 2024-0014 (Board Res. 2918 s.2024; no co-payment policy)', CIRC + '2024/PC2024-0014.pdf'),
    ('2024-10 (signed 7 Oct 2024; effective on publication, ~9 Oct 2024)', '6350', '6000 facility + 350 professional fee', '156 (PHP 990,600/yr max)', 'PhilHealth Circular 2024-0023 (Board Res. 2939 s.2024)', CIRC + '2024/PC2024-0023.pdf'),
]
for eff, rate, split, sess, circ, src in rates:
    mk('philhealth_hd_package_rate_per_session', rate, 'PHP per session', eff, notes=f'{circ}; split: {split or "not stated in text layer"}; sessions/yr: {sess}', src=src)
mk('philhealth_hd_annual_max_benefit', '990600', 'PHP per patient-year', 'from Oct 2024', vtype='derived', notes='6,350 x 156 (also stated in TS for PC 2024-0023)', src=CIRC + '2024/TS_PC2024-0023.pdf')
mk('philhealth_hd_annual_max_benefit', '624000', 'PHP per patient-year', 'Jul-Oct 2024', vtype='derived', notes='4,000 x 156', src=CIRC + '2024/PC2024-0014.pdf')
mk('philhealth_hd_annual_max_benefit', '405600', 'PHP per patient-year', '2023 - Jun 2024', vtype='derived', notes='2,600 x 156', src=CIRC + '2023/PC2023-0009.pdf')
mk('philhealth_hd_annual_max_benefit', '234000', 'PHP per patient-year', 'Jul 2015 - 2019', vtype='derived', notes='2,600 x 90', src=CIRC + '2015/circ022-2015.pdf')
# third-party / filing estimates
fs_src = RHP + ' (Frost & Sullivan report quoted in RHP, pp. 282-283)'
for k, v, u, p, n in [
    ('dialysis_services_market_value', '492.2', 'USD million', '2024', ''),
    ('dialysis_services_market_value_forecast', '1361.4', 'USD million', '2029F', 'CAGR 22.6%'),
    ('patients_undergoing_dialysis', '36.0', 'thousand', '2019', ''), ('patients_undergoing_dialysis', '54.0', 'thousand', '2024', ''),
    ('patients_undergoing_dialysis_forecast', '82.3', 'thousand', '2029F', ''),
    ('patients_requiring_dialysis', '238.6', 'thousand', '2019', ''), ('patients_requiring_dialysis', '329.3', 'thousand', '2024', ''),
    ('patients_requiring_dialysis_forecast', '465.0', 'thousand', '2029F', ''),
    ('ckd_population', '13189', 'thousand', '2024', '12,188k in 2019; 14,600k 2029F'),
    ('average_price_per_dialysis_treatment', '71.0', 'USD', '2024', 'vs ~USD 22 in India'),
    ('new_dialysis_patients_per_year', '>4000', 'patients/year', '2024-2029', ''),
    ('dialysis_station_deficit', '8000', 'stations', 'n.d.', 'attributed to the Philippine Renal Disease Registry; >100,000 patients needing treatment'),
    ('government_dialysis_subsidies', '300', 'USD million', '2022', ''), ('government_dialysis_subsidies', '1300', 'USD million', '2025', ''),
    ('accredited_standalone_dialysis_clinics', '~700', 'clinics', 'n.d. (PhilHealth cited)', ''),
    ('private_chain_share_of_market', '>90', 'percent', '2024', 'dialysis chains run by private providers'),
    ('top5_standalone_chains', 'B. Braun Avitum; Hemotek Renal Center; NephroPlus (Nephrocare); Fresenius Kidney Care; Avitus Kidney Care', 'list', '2024', 'NephroPlus 3rd by number of clinics'),
    ('co_payment_before_2024', '500-600', 'PHP per session', 'until 2023', 'patient co-pay on top of PHP 2,600'),
    ('nephrologist_additional_professional_fee_cap', '500', 'PHP per session', '2024-', 'as described in RHP'),
]:
    mk(k, v, u, p, vtype='third_party_estimate', notes=n, src=fs_src)
mk('hemodialysis_market_size', '300', 'USD million', '2019', vtype='third_party_estimate', notes='"fast-growing but highly fragmented" (MedLine/ARQCapital article)', src='https://philstar.com/business/2019/11/17/1969362/arqcapital-boosts-medline-bid-expand-dialysis-centers')
mk('dialysis_market_size', '200', 'USD million', '2025-02', vtype='third_party_estimate', notes='cited by NephroPlus CEO', src='https://nephroplus.com/press/nephroplus-expands-its-footprint-in-the-philippines-with-acquisition-of-7-dialysis-centers')
mk('western_visayas_dialysis_claims_paid', '4.12', 'PHP billion', 'Jun 2023 - Jun 2025', notes='814,973 claims; 46.92% Negros Occidental, 34.81% Capiz (via search results)', geo='Region VI', src='https://watchmendailyjournal.com/2025/08/29/dialysis-tops-philhealth-claims-in-western-visayas/')
os.makedirs('data/market', exist_ok=True)
with open('data/market/market_context.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(M[0].keys())); w.writeheader(); w.writerows(M)
print('ownership', len(O), 'financials_volume', len(F), 'market_context', len(M))
