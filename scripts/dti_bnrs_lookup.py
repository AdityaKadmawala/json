"""Exact-match lookups of business names on the public DTI Business Name Registration System (BNRS)
search page (https://bnrs.dti.gov.ph/search/search_this). The page only allows exact-name search.
Rate-limited (default 2.5 s between requests); stops on any non-200 / challenge response.

Usage: python3 -I scripts/dti_bnrs_lookup.py names.txt out.csv
names.txt: one business name per line. Raw HTML saved under raw/corporate/dti_bnrs/.
"""
import csv, html, os, re, sys, time, urllib.parse, urllib.request, hashlib, datetime

BASE = 'https://bnrs.dti.gov.ph/search/search_this'
RAW = 'raw/corporate/dti_bnrs'

def fetch(name):
    q = urllib.parse.urlencode(dict(keyword=name, criteria='exact', sort_by='business_name', sort_order='asc'))
    req = urllib.request.Request(BASE + '?' + q, headers={'User-Agent': 'Mozilla/5.0 (research; rate-limited)'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.status, r.read().decode('utf-8', 'ignore'), BASE + '?' + q

def parse(t):
    rows = []
    tb = re.search(r'<tbody.*?</tbody>', t, re.S)
    if not tb:
        return rows
    for tr in re.findall(r'<tr.*?</tr>', tb.group(0), re.S):
        cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', c))).strip() for c in re.findall(r'<td.*?</td>', tr, re.S)]
        if cells:
            rows.append(cells)
    return rows

def main(src, dst, delay=2.5):
    os.makedirs(RAW, exist_ok=True)
    names = [l.strip() for l in open(src, encoding='utf-8') if l.strip()]
    today = datetime.date.today().isoformat()
    with open(dst, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['query', 'n_results', 'business_name', 'territory', 'owner_name', 'certificate_no_bnn', 'registration_date', 'status', 'scope', 'source_url', 'access_date'])
        for n in names:
            try:
                st, t, url = fetch(n)
            except Exception as e:
                print('STOP on error', n, e); break
            if st != 200 or 'search results found' not in t:
                print('STOP: unexpected response', st, n); break
            open(os.path.join(RAW, hashlib.md5(n.encode()).hexdigest()[:10] + '.html'), 'w', encoding='utf-8').write(t)
            m = re.search(r'(?:<b>)?(\d+)(?:</b>)? search results found', t)
            rows = parse(t)
            if not rows:
                w.writerow([n, m.group(1) if m else '', '', '', '', '', '', '', '', url, today])
            for c in rows:
                c = (c + [''] * 7)[:7]
                w.writerow([n, m.group(1) if m else ''] + c + [url, today])
            f.flush()
            print(n, '->', m.group(1) if m else '?', [c[:3] for c in rows][:3])
            time.sleep(delay)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
