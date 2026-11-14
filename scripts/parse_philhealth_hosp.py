"""Parse PhilHealth 'List of Accredited Hospitals and Infirmaries' PDF into CSV.

Usage: python3 scripts/parse_philhealth_hosp.py raw/philhealth/HOSP_093026.pdf data/philhealth_hospitals_2026-09-30.csv
"""
import csv, re, sys
import pdfplumber
from parse_philhealth_fdc import REGION_RE, clean

COLS = ['seq', 'name', 'beds', 'category', 'tel', 'email', 'street', 'municipality', 'accreditation_expiry', 'sector']

def main(src, dst):
    rows, region, province = [], '', ''
    with pdfplumber.open(src) as pdf:
        title = clean(pdf.pages[0].extract_text().split('\n')[1] if 'Philippine Health' in pdf.pages[0].extract_text().split('\n')[0] else pdf.pages[0].extract_text().split('\n')[0])
        for pno, page in enumerate(pdf.pages, 1):
            for table in page.extract_tables():
                for r in table:
                    r = [clean(c) for c in r] + [''] * (10 - len(r))
                    if r[1] == 'NAME OF HEALTH FACILITY':
                        continue
                    if r[0] and not any(r[1:]):
                        if REGION_RE.search(r[0]):
                            region, province = r[0], ''
                        else:
                            province = r[0]
                        continue
                    if not re.fullmatch(r'\d+', r[0] or ''):
                        continue
                    d = dict(zip(COLS, r[:10]))
                    d['seq'] = int(d['seq']); d['email'] = d['email'].replace(' ', '')
                    d['sector'] = {'P': 'Private', 'G': 'Government'}.get(d['sector'], d['sector'])
                    d.update(region=region, province=province, source_page=pno, source_list=title)
                    rows.append(d)
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f'{len(rows)} rows; seq max {max(r["seq"] for r in rows)}; {title}')

if __name__ == '__main__':
    main(*sys.argv[1:3])
