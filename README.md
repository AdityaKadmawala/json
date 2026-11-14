# Philippine dialysis centers: a census of every centre we could find

Goal: every dialysis centre in the Philippines, freestanding and hospital-based, with location, contacts, entity and owner details, regulatory status, legal and regulatory history, and capacity, volume and revenue where public.

Research date: **2026-11-14**. Every row in every CSV carries a `source_url` (and usually an access date).

## Start here
| File | What it is |
|---|---|
| `data/PH_dialysis_centers.xlsx` | Everything below in one workbook: 14 sheets, frozen headers, filters |
| `data/dialysis_centers_philippines.csv` | **Master table, 1,302 rows**, one per centre or candidate (columns below) |
| `data/legal/legal_regulatory_events.csv` | 47 court, PhilHealth, DOH, Ombudsman, Senate and COA events |
| `data/corporate/ownership.csv` | 74 operator, subsidiary and parent records: SEC/registry IDs, officers, ultimate owners |
| `data/corporate/entities.csv` | Legal-form classification and owner links for all 1,012 accredited clinics |
| `data/corporate/financials_volume.csv` | 181 revenue, PhilHealth-payment, station, machine and patient figures |
| `data/market/market_context.csv` | National PhilHealth HD claims 2017–H1 2026, package-rate history, market size |
| `data/operators/*.csv` | 52 operators, 569 chain branches, 186 centres not in the PhilHealth lists |
| `notes/registrations_map.md` | **Every registration a dialysis centre needs, and whether it can be looked up publicly** |
| `notes/{legal,corporate,operators_geo}.md` | Source logs: what was tried, reachable or blocked, row counts |

## Coverage
| Status | Rows | Meaning |
|---|---|---|
| Confirmed freestanding clinic | 1,012 | On PhilHealth's *Accredited Freestanding Dialysis Clinics*, as of 30 Sep 2026 (complete: numbered 1–1,012, no gaps) |
| Confirmed hospital-based unit | 125 | Level 3 hospitals on PhilHealth's hospital list. DOH AO 2012-0012-A requires a dialysis facility at Level 3 |
| Confirmed hospital + web evidence | 12 | Level 1/2 hospitals on PhilHealth's list, with independent web evidence of an HD unit |
| Candidate, not in PhilHealth lists | 72 | Found in OSM, directories, operator sites or news; no match. Unaccredited, new, closed, or hospital units |
| Candidate, possible duplicate | 74 | Weak match to a PhilHealth row (score shown). Needs a human check |
| Candidate, generic name | 7 | e.g. "Dialysis Center"; can't be matched |

Confirmed centres by region (freestanding + hospital): NCR 252 · CALABARZON 214 · Central Luzon 201 · Central Visayas 63 · Ilocos 56 · Cagayan Valley 47 · Bicol 40 · Davao 39 · N. Mindanao 36 · W. Visayas 34 · Negros Island 30 · E. Visayas 28 · SOCCSKSARGEN 26 · CAR 25 · Caraga 19 · Zamboanga 18 · MIMAROPA 13 · BARMM 8.

**How complete is "every"?**
- **Freestanding clinics.** PhilHealth accreditation is effectively universal because almost all revenue is PhilHealth (₱36.8bn paid to freestanding clinics in 2025). The 1,012 accredited clinics should therefore be close to the whole operating market. The candidate list catches the rest: unaccredited, new and closed clinics.
- **Hospital units.** This is the weakest part. 432 Level 2 and 781 Level 1 hospitals are in `philhealth_hospitals_2026-09-30.csv`, and many run HD units with no published list. Only 12 have evidence so far.
- **The DOH licensing list closes both gaps.** It lists every licensed HD facility, hospital-based units included, with machine counts, but it is behind Cloudflare (see below).

## Master table columns (`dialysis_centers_philippines.csv`)
- **Identity:** `center_id` (FDC-#### = PhilHealth freestanding seq, HOSP-#### = PhilHealth hospital seq, CAND-… = candidate) · `coverage_status` · `facility_type` · `name` · `sector` (Private/Government) · `entity_type` (stock corp, business name, OPC, cooperative, non-stock, government)
- **Ownership:** `operator` · `operator_parent` · `operator_entity` · `ultimate_owner` · `group_link_confidence` · `legal_entity_name` · `operator_group` / `operator_group_size` (grouping by shared name, corporate email domain or exact email) · `entity_notes`
- **Location:** `street` · `municipality` · `province` · `admin_region` (PSGC regions incl. Negros Island Region) · `psgc_adm3_pcode` · `lat`/`lon` + `coord_source`. 120 are exact (OSM or operator locator); 1,089 are **APPROXIMATE municipality centroids**, labelled as such.
- **Contact:** `phones` (normalised +63) · `mobile_count` · `emails` · `corporate_email_domain`
- **Regulatory:** `philhealth_accredited` · `philhealth_list` · `philhealth_seq` · `philhealth_accreditation_expiry` · `hospital_level` · `hospital_beds`
- **Capacity:** `hd_stations` (sparse: published for very few sites) · `services`
- **Legal:** `legal_event_count` and `legal_regulatory_events`, matched by entity name. Chain-level events attach to every branch of that legal entity; check `data/legal/` for the facts.
- **Provenance:** `hd_unit_evidence` · `web_source_urls` · raw PhilHealth fields (`tel_raw`, `email_raw`, `philhealth_region`)

## Key findings
- **Ownership**
  - NephroPlus (India, NSE-listed) is now the largest chain: 55 accredited sites after its 2024–26 acquisitions, about 50 clinics and 686 stations in July 2026.
  - B. Braun Avitum (Germany) has 34 sites; Avitus 23 (owner not found); Fresenius Medical Care (Germany) 20.
  - Hemotek has 19, 100% owned by PSE-listed Euro-Med Laboratories (Yap family).
  - Name-only groups whose common owner isn't verified: "Nephrology Center of …" 34, JL Dialmed 16, TotalCare 16, Prime 15.
  - About 300 clinics trade under a business name with no corporate suffix, so their owner needs DTI/SEC records.
- **Money and volume.**
  - PhilHealth HD claims rose from ₱17.4bn (2023) to ₱71.7bn (2025) after the HD package went from ₱2,600 to ₱6,350 per session in October 2024 (156 sessions a year).
  - H1 2026 was ₱48.7bn.
  - Accredited freestanding clinics grew from 394 (2019) to 1,012 (Sep 2026).
- **Legal**
  - WellMed "ghost dialysis" (2019): accreditation withdrawn; estafa case pending.
  - B. Braun: Senate allegations and an NBI complaint to the Ombudsman over 2020 PhilHealth cash advances; no ruling found.
  - SouthMed: PhilHealth suspension upheld by the Supreme Court.
  - TriHDCare: claims for dead patients; a clerk was convicted in 2024.
  - NephroPlus subsidiaries: litigation disclosed in its prospectus.
  - No public DOH order closing a named clinic was found.

## Sources used (and status from this environment)
| Source | Status | Gave us |
|---|---|---|
| PhilHealth accredited FDC and hospital lists, circulars, advisories, Stats & Charts, IRM disclosures | ✅ | Backbone list, contacts, accreditation, hospital levels, claims totals, rate history |
| Operator websites (B. Braun locator, NephroPlus, Hemotek, TresMedica, Nephro Synergies…) | ✅ (Fresenius robots-blocked → search snippets) | Branches, coordinates, some station counts |
| OpenStreetMap (full PH extract), HDX health facilities | ✅ | 177 dialysis features with coordinates, municipality codes |
| ClinicFinderPH, Baxter My Kidney Journey, PSN, news | ✅ | Candidates not in PhilHealth lists |
| NSE/SEBI prospectus (NephroPlus), PSE Edge (Euro-Med), SGX (Clearbridge), GLEIF LEI | ✅ | Subsidiaries, incorporation data, shareholders, revenue, litigation |
| FDA verification portal | ✅ | Operator legal owner, LTO numbers, head offices |
| CDA cooperative masterlist | ✅ | Registration and compliance of cooperative operators |
| lawphil.net, PhilHealth Board decisions, GMA/Philstar/BusinessWorld/SunStar | ✅ | Court decisions, sanctions, news |
| **DOH HFSRB licensed-facility lists, NHFR, FOI portal, SEC, COA, DENR-EMB, BFP, Senate** | ❌ Cloudflare 403 | Not obtained. We did **not** attempt to bypass bot protection |
| Wayback Machine, Overpass API | ❌ unreachable | Historical PhilHealth lists not recovered |
| DTI BNRS name search | ⚠️ returns 0 results | No sole-proprietor owners |
| PRC license verification | ❌ connection reset | No nephrologist verification |

## How to push coverage toward 100% (recommended next steps)
1. **DOH HFSRB list of licensed dialysis facilities.** It is public on `hfsrb.doh.gov.ph`, but blocked only for this cloud environment. Download it from a normal browser, or file an eFOI request for "licensed hemodialysis facilities incl. hospital-based units, LTO no., validity, number of HD machines, owner". Drop it in `raw/registry/` and merge. This one source fills hospital units, machine counts and owner names.
2. **PhilHealth eFOI:** ask for claims paid per facility (₱ and sessions) for 2023–2026. That gives revenue and volume per centre. Also ask for past FDC lists, to find closed or de-accredited centres.
3. **SEC:** buy GIS and AFS copies via eFAST for the ~650 corporations: directors, shareholders and revenue. Start with the unverified groups (Avitus, Nephrology Center of…, JL Dialmed, TotalCare, Prime).
4. **DTI BNRS certifications** for the ~300 business-name clinics, to get the owner of each trade name.
5. **LGU BPLO** business-permit records for declared gross sales, a revenue proxy. Many cities answer local FOI requests.
6. **Courts:** eCourt/CA docket and NLRC searches by entity name. Ombudsman/DOJ status of the WellMed and B. Braun complaints.
7. **Verify the 74 possible duplicates and 72 unmatched candidates.** Call or check their Facebook pages, or use Google Places with your own API key.
8. **DENR-EMB hazardous-waste generator IDs, BFP FSIC and PRC checks:** request regionally (see `notes/registrations_map.md`).

## Rebuild
```bash
python3 scripts/parse_philhealth_fdc.py raw/philhealth/FDC_093026.pdf data/philhealth_fdc_2026-09-30.csv
PYTHONPATH=scripts python3 scripts/parse_philhealth_hosp.py raw/philhealth/HOSP_093026.pdf data/philhealth_hospitals_2026-09-30.csv
python3 scripts/build_master.py
PYTHONPATH=scripts python3 scripts/merge_enrichment.py
python3 scripts/build_workbook.py
```
Workstream builders: `build_operators_geo.py`, `build_corporate_tables.py`, `classify_entities.py`, and others; see the notes files.

## Caveats
- **Allegations vs findings.** Allegations and findings are kept separate (`finding_level`). People are named only as they appear in court, official or news sources.
- **Approximate coordinates.** Municipality-centroid coordinates are approximate. Don't use them for distance analysis.
- **PhilHealth region.** PhilHealth groups Batangas and Rizal under different regional offices; `admin_region` gives the official PSGC region.
- **Group sizes.** Operator groups built from shared names and emails are heuristics; `group_link_confidence` rates them. Chain counts differ from what the companies claim, because many acquired sites are still accredited under the seller's name.
