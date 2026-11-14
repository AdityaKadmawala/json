#!/usr/bin/env python3
"""Post-filter data/geo/osm_dialysis_all.csv -> data/geo/osm_dialysis.csv.
Drops regex false positives (e.g. 'Arenal', 'Renalyn' shops/streets) and classifies rows."""
import pandas as pd, re
d = pd.read_csv('data/geo/osm_dialysis_all.csv', dtype=str).fillna('')
word = re.compile(r'\b(renal|kidneys?|nephro\w*|dialy\w*|dilaysis|hemodialysis|haemodialysis|hemodynamix|kidneyspace|kidneycare|nephrocare|hemo ?lab)\b', re.I)
def cls(r):
    txt = ' '.join([r['name'], r['operator'], r['brand']])
    tag = r['healthcare']=='dialysis' or 'dialysis' in r['healthcare_speciality']
    if r['amenity']=='parking' or re.search(r'\b(street|lane|ukay|sari-sari|cellshop|kumon)\b', txt, re.I): return 'exclude'
    if tag or word.search(txt):
        if re.search(r'transplant institute|kidney foundation', txt, re.I) and not re.search('dialys', txt, re.I): return 'hospital/institution with dialysis'
        return 'dialysis facility'
    if 'nephrolog' in r['healthcare_speciality']: return 'nephrology specialty tag only'
    return 'exclude'
d['category'] = d.apply(cls, axis=1)
print(d.category.value_counts())
print(d[d.category=='exclude'][['osm_type','osm_id','name','amenity']].to_string())
d[d.category!='exclude'].to_csv('data/geo/osm_dialysis.csv', index=False)
