"""Classify each PhilHealth-accredited freestanding dialysis clinic (FDC) by legal-entity type and
link it to an operator group / ultimate owner where public evidence exists.

Input : data/philhealth_fdc_2026-09-30.csv
Output: data/corporate/entities.csv
  legal_entity_name_guess = accredited juridical name as printed (cleaned), or for a business name the
  operator entity when known; operator_entity = entity that (per disclosures) operates/owns the site when
  it differs from the accredited name (e.g. NephroPlus asset purchases, group subsidiaries).

Rules (applied to the accredited name exactly as PhilHealth printed it):
  government            sector == Government (LGU / DOH / provincial facility)
  cooperative           name contains COOPERATIVE
  non_stock_non_profit  FOUNDATION, RED CROSS, ROTARY CLUB, CHURCH, DIOCESE
  one_person_corp       OPC suffix (Revised Corporation Code 2019, sec. 115-)
  stock_corporation     INC / INCORPORATED / CORP / CORPORATION / LTD / OPC-less corporate suffix
  corp_or_partnership   "CO." or "COMPANY" suffix (can be a corporation or a registered partnership)
  business_name         no juridical suffix: a DTI business name of a sole proprietor OR a trade
                        name of a corporation -> legal entity unknown unless group evidence exists
Group links come from (a) the operator's own disclosures (NephroPlus RHP / NSE filings, Euro-Med 17-A,
Clearbridge annual report, GLEIF), (b) brand names, (c) shared corporate e-mail domains / mailbox
patterns in the PhilHealth list. The basis and a confidence level are recorded for every link.
"""
import csv, re, os, collections

SRC = 'data/philhealth_fdc_2026-09-30.csv'
DST = 'data/corporate/entities.csv'
ACCESS = '2026-11-14'
PH_URL = 'https://www.philhealth.gov.ph/partners/providers/facilities/accredited/FDC_093026.pdf'
RHP = 'https://www.chittorgarh.net/reports/ipo_notes/nephrocare-health-ipo-rhp.pdf'
NP_ULT = 'Nephrocare Health Services Ltd (NephroPlus), Hyderabad, India (NSE: NEPHROPLUS)'

GROUPS = {
    'BBRAUN': dict(legal='B. Braun Avitum Philippines, Inc.',
                   ult='B. Braun SE / B. Braun Holding GmbH & Co. KG, Melsungen, Germany',
                   src='https://www.gmanetwork.com/news/news/nation/751153/b-braun-avitum-vows-cooperation-with-gov-t-after-being-linked-to-philhealth-s-irm-releases/story/'),
    'FRESENIUS': dict(legal='Fresenius Medical Care Philippines, Inc. / FMC Renalcare Corp. (site-level licensee not confirmed)',
                      ult='Fresenius Medical Care AG, Bad Homburg, Germany',
                      src='https://freseniusmedicalcare.com/en-ph/clinics/'),
    'NEPHROPLUS': dict(legal='Nephrocare Health Care Services, Philippines Inc.', ult=NP_ULT, src=RHP),
    'HEMOTEK': dict(legal='Hemotek Renal Center, Inc.',
                    ult='Euro-Med Laboratories Phil., Inc. (PSE: EURO; 100% owner) <- U.S. Automotive Co., Inc. (ultimate parent, ~58%)',
                    src='https://edge.pse.com.ph/openDiscViewer.do?edge_no=3f637e70c200074b64d70b69f0a3140b'),
    'CLEARBRIDGE': dict(legal='', ult='Clearbridge Health Ltd (SGX Catalist: 1H3), Singapore - 65% of Clearbridge Medical (Philippines) Inc. (fka Marzan Health Care Inc.)',
                        src='https://links.sgx.com/1.0.0/corporate-announcements/RJ4RRULTOEY26PV0/882292_CBH%20-%20Annual%20Report%202025.pdf'),
    'HEALTHWAY': dict(legal='Healthway Philippines, Inc. (site-level licensee not confirmed)',
                      ult='Ayala Healthcare Holdings, Inc. (AC Health) <- Ayala Corporation (PSE: AC)',
                      src='https://mb.com.ph/2023/12/10/ayala-boosts-stake-in-healthway-to-94'),
    'MMG': dict(legal='', ult='Medical Mission Group Hospitals and Health Services Cooperative of the Philippines (federation of member co-ops)', src=PH_URL),
}

# NephroPlus site-level links (seq -> (legal entity, basis, confidence, note))
NP = {}
def np(seqs, legal, basis, conf, note=''):
    for s in str(seqs).split():
        NP[s] = (legal, basis, conf, note)
np('318 482 709 761 762', 'Renal Therapy Solutions, Inc.', 'RHP subsidiary list (100% NHCS-PH; acquired 2024)', 'high')
np('214', 'Bioregen Hemo Center Inc.', 'RHP subsidiary list (Hemo Group, acquired 2025)', 'high')
np('63', 'Infini Care Health Systems Inc.', 'RHP subsidiary list (Hemo Group); same Doria Bldg Malasiqui address', 'high')
np('622 647', 'Kolff Dialysis Inc.', 'RHP subsidiary list (Hemo Group); Lucena address matches', 'high')
np('625', 'Mega Health Dialysis Center Inc.', 'RHP subsidiary list; LGC Bldg Parian Calamba address matches', 'high')
np('551', 'Carmona Dialysis System Inc.', 'RHP subsidiary list (Hemo Group); Bldg 88 Governor\'s Drive address matches', 'high')
np('661', 'AIZ Hemodialysis Centre Inc.', 'RHP subsidiary list (Hemo Group)', 'high')
np('541', 'Rizal Dialysis and Wellness Centre Inc.', 'RHP subsidiary list + NephroPlus mailbox pattern; PhilHealth prints OPC', 'high')
np('474', "People's Center for Hemodialysis Care Inc.", 'RHP subsidiary list + mailbox pattern', 'high')
np('791', 'Cadiz Dialysis Hub Inc.', 'RHP subsidiary list (Cadiz SPA 31 May 2022)', 'high')
np('700', 'Universe Dialysis and Kidney Care Centre Inc.', 'RHP subsidiary list (Nasugbu) + mailbox pattern', 'high')
np('90', 'Curis Hemodialysis Clinic Inc.', 'RHP subsidiary list + mailbox pattern (ph.isa.cyn.pho)', 'high')
np('553', 'Curis Cavite Renal Corporation', 'RHP subsidiary registered in Naic, Cavite (street differs)', 'medium')
np('377', 'Medical Experts Group and Associates Inc.', 'RHP registered office Unit 101 Nodison Centre, Marikina = PhilHealth address; mailbox pattern', 'high')
np('389', 'Nephrocare Health Care Services, Philippines Inc.', 'accredited under NHCS-PH; same address as RHP subsidiary St. Margareth Dialysis and Biocare Centre Inc.', 'high')
np('489', 'Nephrocare Health Care Services, Philippines Inc.', 'accredited under NHCS-PH; same address as RHP subsidiary Dialysis Asia and Patient Care Center Inc. (Gate 3 Plaza Mall)', 'high')
np('630', 'Nephrocare Health Care Services, Philippines Inc.', 'accredited under NHCS-PH; business of Cabuyao Kidney Care Dialysis Centre acquired 24 Jun 2025 (RHP note 42a)', 'high')
np('338', 'Passion Healthcare Phils Inc. (business acquired by NephroPlus 24 Jul 2025)', 'RHP note 42c + mailbox pattern', 'high', 'accreditation still in seller name')
np('114', 'Santiago City Kidney Centre Inc. (business acquired by NephroPlus 1 Jul 2025)', 'RHP note 42b', 'high', 'accreditation still in seller name')
np('305', 'Zambales Dialysis & Kidney Center Inc. (business acquired by NephroPlus 6 Oct 2025)', 'RHP note (xi)', 'high', 'same address as seq 302 (NHCS-PH) - likely same physical site, old accreditation')
np('467', 'Nephrocare Health Care Services, Philippines Inc. (brand NephroPlus)', 'brand name + mailbox pattern', 'high')
np('882', 'Nephro Alliance Ventures Inc.', 'RHP subsidiary registered office Governor Lim Avenue, Zone 4, Zamboanga City = PhilHealth address; mailbox pattern', 'high')
np('135', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'NSE filing/news: Orion, Bataan dialysis assets PHP 151.6M (24 Jun 2026); NephroPlus 50th clinic Orion (Jul 2026)', 'medium', 'accreditation still in seller name')
# 2026 asset-transfer agreements disclosed to NSE/BSE (buyer NHCS-PH); PhilHealth still lists seller name
np('677', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'BSE/NSE Reg.30 filing 12 Feb 2026: ATA with Laurel Kidney Care Dialysis Centre Inc., PHP 49.4M', 'high', 'accreditation still in seller name')
np('91', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'NSE Reg.30 filing 27 Jan 2026: ATA with Dialysis Center of Cauayan Inc., PHP 37.72M', 'high', 'accreditation still in seller name')
np('911', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'NSE Reg.30 filing 26 May 2026: ATA with Northern Mindanao Dialysis Clinic Inc., PHP 27.4M', 'high', 'accreditation still in seller name')
np('211', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'NSE Reg.30 filing 26 May 2026: ATA with Aliaga Hemodialysis Centre Inc., PHP 44.8M', 'high', 'accreditation still in seller name')
np('940', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'NSE Reg.30 filing 13 Aug 2026: ATA with Juan Nephro Dialysis Center (Davao City), PHP 71.8M', 'high', 'accreditation still in seller name')
np('144', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'news of NSE filing: Orani Hemodialysis Center Inc., PHP 89.6M (May 2026)', 'medium', 'accreditation still in seller name')
np('547', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'news of NSE filing: Amica Healthcare System Corp., PHP 32.64M (Jun 2026)', 'medium', 'accreditation still in seller name')
np('898', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'news of NSE filing: Pag-Asa Dialysis and Diagnostic Center, Ipil, PHP 80.64M (22 Jun 2026)', 'medium', 'accreditation still in seller name')
np('858', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'news of NSE filing: Assumption Dialysis Center, Abuyog, PHP 75M (Aug 2026)', 'medium', 'accreditation still in seller name')
np('198', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'news of NSE filing: Renal One Dialysis Corp. Plaridel site, PHP 67.2M (Sep 2026)', 'medium', 'only the Plaridel site; other Renal One sites not covered')
np('446', 'Nephrocare Health Care Services, Philippines Inc. (asset buyer)', 'news of NSE filing: Inocentes Dialysis Clinic, Quezon City, ~PHP 30M (Jun 2026)', 'medium', 'accreditation still in seller name')
np('7', 'Nephrocare Health Care Services, Philippines Inc.', 'accredited under NHCS-PH (Baguio); RHP: business of Cordillera Kidney Specialist Inc. acquired 2 Oct 2025 (site match not confirmed)', 'high')

CORP_RE = re.compile(r'\b(INC|INCORPORATED|CORP|CORPORATION|LTD|LIMITED)\b\.?', re.I)
CO_RE = re.compile(r'\b(CO\.|COMPANY)(?=$|[\s,.)])', re.I)
OPC_RE = re.compile(r'\bOPC\b', re.I)
NONSTOCK_RE = re.compile(r'FOUNDATION|RED CROSS|ROTARY CLUB|CHURCH|DIOCESE', re.I)

def norm(s):
    s = s.upper().replace('Ñ', 'N')
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    s = re.sub(r'\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|OPC|PHILS|PHILIPPINES|THE)\b', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def akey(r):
    st = norm(r['street'])
    st = re.sub(r'\b(BRGY|BARANGAY|BGY|POB|POBLACION|ST|STREET|ROAD|RD|AVE|AVENUE|UNIT|BLDG|BUILDING|FLOOR|GF|G F|NO)\b', ' ', st)
    st = re.sub(r'\s+', ' ', st).strip()
    return (st[:22], r['municipality'].upper())

def clean_legal(name):
    n = re.sub(r'[,\s]+$', '', name.strip())
    n = re.sub(r'\bINC$', 'INC.', n)
    n = re.sub(r'\bCORP$', 'CORP.', n)
    n = re.sub(r',\s*INC,$', ', INC.', n)
    return n

def main():
    rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
    core_count = collections.Counter(norm(r['name']) for r in rows)
    addr = collections.defaultdict(list)
    for r in rows:
        addr[akey(r)].append(r['seq'])
    out = []
    for r in rows:
        name, seq, email = r['name'], r['seq'], r['email'].lower()
        up = name.upper()
        # ---- legal form
        if r['sector'].lower().startswith('gov'):
            et, basis = 'government', 'PhilHealth sector = Government'
        elif 'COOPERATIVE' in up:
            et, basis = 'cooperative', 'name contains COOPERATIVE (CDA-registered)'
        elif NONSTOCK_RE.search(up):
            et, basis = 'non_stock_non_profit', 'foundation/charitable/religious name'
        elif OPC_RE.search(up):
            et, basis = 'one_person_corp', 'OPC suffix'
        elif CORP_RE.search(up):
            et, basis = 'stock_corporation', 'INC/CORP/CORPORATION suffix'
        elif CO_RE.search(up):
            et, basis = 'corp_or_partnership', 'CO./COMPANY suffix'
        else:
            et, basis = 'business_name', 'no juridical suffix (sole-prop business name or corporate trade name)'
        legal = clean_legal(name) if et in ('stock_corporation', 'one_person_corp', 'cooperative', 'corp_or_partnership', 'non_stock_non_profit') else ''
        acc_legal = legal  # entity as printed on the accreditation (juridical names only)
        # ---- group links
        grp, ult, gbasis, conf, notes, src = '', '', '', '', [], PH_URL
        if re.search(r'B\.? ?BRAUN', up) or 'bbraun.com' in email:
            g = GROUPS['BBRAUN']; grp = 'B. Braun Avitum'; gbasis = 'name' + (' + bbraun.com e-mail' if 'bbraun.com' in email else ''); conf = 'high'
            legal = g['legal']; ult = g['ult']; src = g['src']
        elif re.search(r'FRESENIUS|^FMC RENAL', up) or 'freseniusmedicalcare' in email or 'fmc-asia' in email:
            g = GROUPS['FRESENIUS']; grp = 'Fresenius Kidney Care'; conf = 'high'
            gbasis = 'brand name' if 'FRESENIUS' in up else 'Fresenius corporate e-mail domain'
            legal = 'FMC Renal Care Corp.' if up.startswith('FMC RENAL') else g['legal']; ult = g['ult']; src = g['src']
            if up == 'NEPHROCARE':
                notes.append('"NEPHROCARE" here is Fresenius\'s service brand (freseniusmedicalcare.com e-mail), NOT NephroPlus\'s NHCS-PH')
        elif seq in NP or 'NEPHROCARE HEALTH CARE SERVICES' in up or re.search(r'ph\.[a-z0-9]+\.[a-z0-9]+\.pho|philhealthhead', email):
            grp = 'NephroPlus'; ult = NP_ULT; src = RHP
            if seq in NP:
                legal, gbasis, conf, nt = NP[seq]
                if nt: notes.append(nt)
            else:
                legal = GROUPS['NEPHROPLUS']['legal']; gbasis = 'accredited under NHCS-PH name' if 'NEPHROCARE HEALTH' in up else 'NephroPlus mailbox pattern'; conf = 'high'
        elif 'HEMOTEK' in up:
            g = GROUPS['HEMOTEK']; grp = 'Hemotek'; ult = g['ult']; src = g['src']
            legal = g['legal']; gbasis = 'name' + (' + hemotek.net e-mail' if 'hemotek.net' in email else '')
            conf = 'high' if ('INC' in up or 'hemotek.net' in email) else 'medium'
            if 'INC' not in up: notes.append('"HEMOTEK DIALYSIS CENTER" (no INC.) assumed Hemotek Renal Center, Inc. trade name')
        elif 'CLEARBRIDGE' in up:
            g = GROUPS['CLEARBRIDGE']; grp = 'Clearbridge Health'; ult = g['ult']; src = g['src']; gbasis = 'name + SGX annual report'; conf = 'high'
        elif 'HEALTHWAY' in up or 'healthway.com.ph' in email:
            g = GROUPS['HEALTHWAY']; grp = 'Healthway (AC Health)'; ult = g['ult']; src = g['src']; gbasis = 'brand name + healthway.com.ph e-mail'; conf = 'medium'
            if 'QUALIMED' in up: legal = 'Healthway QualiMed hospital network (Mercado General Hospital Inc. group; site entity not confirmed)'
            elif not legal: legal = g['legal']
        elif 'MEDICAL MISSION GROUP' in up:
            g = GROUPS['MMG']; grp = 'Medical Mission Group (cooperative network)'; ult = g['ult']; gbasis = 'name'; conf = 'medium'
        elif 'AVITUS' in up:
            grp = 'Avitus'; gbasis = 'name'; conf = 'high'; ult = ''
            notes.append('owner/shareholders not found in public sources; SEC GIS needed')
        elif 'eghi-' in email:
            grp = 'EG Healthcare (KidneyCare)'; legal = 'EG Healthcare, Inc.'; gbasis = 'eghi-* mailboxes on excelsior.net.ph'; conf = 'medium'
        elif 'thebestrenalcare.com' in email or 'THE BEST RENAL CARE' in up:
            grp = 'The Best Renal Care group'; gbasis = 'shared thebestrenalcare.com e-mail domain' if 'thebestrenalcare.com' in email else 'name'; conf = 'medium'
        elif 'reliancehealth' in email or 'healthfirst.com.ph' in email or 'GLOBAL RELIANCE RENALCARE' in up:
            grp = 'Global Reliance Renalcare'; gbasis = 'name + reliancehealth/healthfirst e-mail'; conf = 'high'
        elif 'tanauanmedicalcenter.com' in email:
            grp = 'Tanauan Medical Center group'; gbasis = 'tanauanmedicalcenter.com e-mail'; conf = 'medium'
        elif 'jortiz' in email or 'JORTIZ' in up:
            grp = 'JOrtiz Dialysis'; gbasis = 'name / jortiz.com.ph e-mail'; conf = 'medium'
        elif 'lifestream' in email or 'LIFESTREAM' in up:
            grp = 'Lifestream Dialysis'; gbasis = 'name / lifestreamdialysis.com e-mail'; conf = 'low' if 'lifestream' not in email else 'medium'
        elif 'NEPHROMED ASIA' in up:
            grp = 'Nephromed Asia'; gbasis = 'name'; conf = 'medium'
            notes.append('founder Jylberd L. Nabor (Manila Bulletin 2019)')
        elif re.match(r'NEPHROLOGY CENTER OF ', up):
            grp = 'Nephrology Center of [city] (name family)'; gbasis = 'name pattern only - common ownership NOT verified'; conf = 'low'
        elif re.match(r'NEPHRO SPECIALIST(S)? OF ', up):
            grp = 'Nephro Specialist of [city] (name family)'; gbasis = 'name pattern only - common ownership NOT verified'; conf = 'low'
        elif up.startswith('NURSIA DIALYSIS'):
            grp = 'Nursia Dialysis (name family)'; gbasis = 'name pattern'; conf = 'low'
        elif core_count[norm(name)] >= 2:
            grp = norm(name).title() + ' (same name, multi-site)'; gbasis = 'identical accredited name at >=2 sites'; conf = 'medium'
        operator_entity = legal if legal != acc_legal else ''
        legal = acc_legal or legal
        if et == 'business_name' and not legal:
            notes.append('legal entity unknown; check DOH LTO / SEC / DTI BNRS certification')
        same = [s for s in addr[akey(r)] if s != seq]
        if same and norm(r['street']):
            notes.append('same street address as seq ' + '/'.join(same))
        out.append(dict(seq=seq, name=name, municipality=r['municipality'], province=r['province'], sector=r['sector'],
                        entity_type=et, entity_type_basis=basis, legal_entity_name_guess=legal, operator_entity=operator_entity,
                        operator_group=grp, ultimate_owner=ult, group_link_basis=gbasis, group_link_confidence=conf,
                        notes='; '.join(notes), source_url=src if grp else PH_URL, access_date=ACCESS))
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    print(len(out), 'rows')
    print(collections.Counter(o['entity_type'] for o in out))
    g = collections.Counter(o['operator_group'] for o in out if o['operator_group'])
    for k, v in g.most_common(40): print(v, k)

if __name__ == '__main__':
    main()
