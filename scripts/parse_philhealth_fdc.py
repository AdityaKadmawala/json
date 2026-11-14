"""Parse a PhilHealth 'List of Accredited Freestanding Dialysis Clinics' PDF into CSV.

Usage: python3 scripts/parse_philhealth_fdc.py raw/philhealth/FDC_093026.pdf data/philhealth_fdc_2026-09-30.csv
"""
import csv, re, sys
import pdfplumber

REGION_RE = re.compile(r'(REGION|NATIONAL CAPITAL|CORDILLERA|BANGSAMORO|BARMM|\bNCR\b|\bCAR\b|NIR\b|NEGROS ISLAND)', re.I)

def clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('\n', ' ')).strip()

def main(src, dst):
    rows, region, province = [], '', ''
    with pdfplumber.open(src) as pdf:
        title = clean(pdf.pages[0].extract_text().split('\n')[0])
        for pno, page in enumerate(pdf.pages, 1):
            for table in page.extract_tables():
                for r in table:
                    r = [clean(c) for c in r] + [''] * (8 - len(r))
                    if r[1] == 'NAME OF HEALTH FACILITY':
                        continue
                    if r[0] and not any(r[1:]):
                        if REGION_RE.search(r[0]) and not re.match(r'^\d', r[0]):
                            region, province = r[0], ''
                        else:
                            province = r[0]
                        continue
                    if not re.fullmatch(r'\d+', r[0] or ''):
                        # continuation row (rare): append to previous record
                        if rows and any(r[1:]):
                            for k, v in zip(['name', 'tel', 'email', 'street', 'municipality'], r[1:6]):
                                if v: rows[-1][k] = (rows[-1][k] + ' ' + v).strip()
                        continue
                    rows.append(dict(seq=int(r[0]), name=r[1], tel=r[2], email=r[3].replace(' ', ''),
                                     street=r[4], municipality=r[5], accreditation_expiry=r[6],
                                     sector={'P': 'Private', 'G': 'Government'}.get(r[7], r[7]),
                                     region=region, province=province, source_page=pno))
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) + ['source_list'])
        w.writeheader()
        for row in rows:
            row['source_list'] = title
            w.writerow(row)
    print(f'{len(rows)} rows; seq max {max(r["seq"] for r in rows)}; title: {title}')

if __name__ == '__main__':
    main(*sys.argv[1:3])
