"""Extract Philippine subsidiary details (incorporation date, office, capital, shareholders,
revenue/PAT/net worth in INR million) from the NephroPlus (Nephrocare Health Services Ltd) RHP text.

Usage: python3 -I scripts/parse_nephroplus_rhp_subsidiaries.py raw/corporate/nephroplus/rhp.txt out.json
(rhp.txt produced by: pdftotext -layout nephrocare_rhp.pdf rhp.txt)
"""
import re, sys, json

def main(src, dst):
    t = open(src, encoding='utf-8').read()
    start = t.find('AIZ Hemodialysis Centre Inc. (“AIZ Hemodialysis”) was incorporated')
    end = t.find('Universe Dialysis and Kidney Care Centre Inc. (“Universe Dialysis”)')
    end = t.find('Amount of accumulated profits', end)
    sec = t[start-200:end+400]
    # split on "Corporate Information"
    parts = re.split(r'\n\s*\d+\.\s+([^\n]+)\n\s*\nCorporate Information', '\n' + sec)
    out = []
    blocks = re.split(r'Corporate Information', sec)
    for b in blocks[1:]:
        flat = re.sub(r'\s+', ' ', b)
        m = re.match(r'\s*(.+?) \(“[^”]+”\) was incorporated', flat)
        name = m.group(1).strip() if m else ''
        d = re.search(r'(?:on|as on) ((?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})', flat)
        office = re.search(r'registered office is (?:located )?at (.+?)\. (?:Nature|\d{3} )', flat)
        nature = re.search(r'Nature of Business (.+?) Capital structure', flat)
        auth = re.search(r'authori[sz]ed share capital of .+? is (?:Peso|PHP|₱) ?([\d,]+)', flat)
        paid = re.search(r'paid-up share capital (?:of .+? )?is (?:Peso|PHP|₱) ?([\d,]+)', flat)
        nhcs = re.search(r'Nephrocare Health Care Services, Philippines Inc\.? ([\d,]+) ([\d.]+)', flat)
        def row(label):
            r = re.search(label + r' ([\-\(\)\d.,N/A]+) ([\-\(\)\d.,N/A]+) ([\-\(\)\d.,N/A]+)', flat)
            return list(r.groups()) if r else ['', '', '']
        sh = re.search(r'Shareholding pattern(.+?)(?:Total|Financial Information)', flat)
        holders = re.findall(r'\d\. ([A-Z][A-Za-z.,’\' \-]+?) ([\d,]+) (?:[\d.]+|Negligible)', sh.group(1)) if sh else []
        out.append(dict(name=name, incorporated=d.group(1) if d else '',
                        registered_office=office.group(1) if office else '',
                        nature=nature.group(1).strip() if nature else '',
                        authorized_capital_php=auth.group(1) if auth else '',
                        paidup_capital_php=paid.group(1) if paid else '',
                        nhcs_pct=nhcs.group(2) if nhcs else '',
                        shareholders='; '.join(f'{a.strip()} ({b})' for a, b in holders),
                        revenue_inr_m_fy25_fy24_fy23=row('Revenue from operations'),
                        pat_inr_m_fy25_fy24_fy23=row(r'Profit/\(loss\) after tax'),
                        networth_inr_m_fy25_fy24_fy23=row('Net Worth')))
    json.dump(out, open(dst, 'w'), indent=1, ensure_ascii=False)
    for o in out: print(o['name'], '|', o['incorporated'], '|', o['nhcs_pct'], '|', o['revenue_inr_m_fy25_fy24_fy23'])

if __name__ == '__main__':
    main(*sys.argv[1:3])
