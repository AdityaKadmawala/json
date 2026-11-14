# Corporate entities, ownership, revenue, volume and capacity: workstream notes

Access date for everything: **2026-11-14**. The base list is `data/philhealth_fdc_2026-09-30.csv` (1,012 PhilHealth-accredited free-standing dialysis clinics).

## Outputs

| File | Rows | What it is |
|---|---|---|
| `data/corporate/entities.csv` | 1,012 | One row per PhilHealth FDC row. Gives the legal-form type, a guessed legal-entity name, the operator group, the ultimate owner, the basis and confidence of each group link, and notes (same-address duplicates, accreditations still in a seller's name). Built by `scripts/classify_entities.py`. |
| `data/corporate/ownership.csv` | 74 | Entity-level ownership rows: operators, PH subsidiaries, parents and ultimate owners, registry IDs, incorporation dates, registered offices, shareholders and officers, former owners, and asset sellers. Built by `scripts/build_corporate_tables.py`. |
| `data/corporate/financials_volume.csv` | 181 | Entity- and site-level revenue, PhilHealth payments, deal values, clinic, station and machine counts, patients, and derived site counts per group. The `value_type` column is `reported` or `derived`. |
| `data/market/market_context.csv` | 122 | National aggregates: PhilHealth HD claims 2017 to H1 2026, claims paid to FDCs, accredited-FDC counts, PD and kidney-transplant Z-benefits, package-rate history 2015 to 2024, Frost & Sullivan market estimates, and derived session and patient-year estimates. `value_type` is one of `reported`, `derived`, `estimate`, `third_party_estimate`. |
| `data/corporate/fda_lto_lookups.csv` | 79 | FDA establishment-licence hits for 38 operator-name queries. Built by `scripts/fda_verification_lookup.py` from `scripts/fda_queries.txt`. |
| `notes/registrations_map.md` | | The permits a dialysis center needs, and whether each has a public lookup (tested). |

### Entity typing result (`entities.csv`)
`stock_corporation` 605 · `business_name` (no juridical suffix) 304 · `government` 41 · `one_person_corp` 22 · `corp_or_partnership` ("CO."/"COMPANY") 19 · `cooperative` 11 · `non_stock_non_profit` 10.
475 rows are linked to an operator group: 148 at high confidence, 281 medium, 46 low. 140 rows have a named ultimate owner.

## Largest operators in the PhilHealth list (30 Sep 2026)

| Group | Accredited rows | Legal entity | Ultimate owner | Key evidence |
|---|---|---|---|---|
| **NephroPlus** | 55 (some are sites acquired in 2026 whose accreditation is still in the seller's name; seqs 302/305 are the same Iba site) | Nephrocare Health Care Services, Philippines Inc. (incorporated 27 Feb 2020 as Tech Care Center, Inc.; paid-up PHP 153.8m) plus 18 to 20 PH subsidiaries | Nephrocare Health Services Ltd, India (NSE: NEPHROPLUS), via Nephrocare Health Services International Pte Ltd (Singapore). Promoters: Vikram Vuppala, Bessemer, Edoras, Healthcare Parent Ltd, Investcorp. | RHP of 2 Dec 2025 (subsidiary-by-subsidiary corporate data and financials); NSE/BSE Reg. 30 filings for 2026 asset deals |
| **B. Braun Avitum** | 34 | B. Braun Avitum Philippines, Inc. (incorporated 24 Jan 2002 as Philippine Renal Care, Inc.) | B. Braun SE, then B. Braun Holding GmbH & Co. KG (Germany) | GMA 2020 company statement; GLEIF records for sister company B. Braun Medical Supplies Inc. (SEC 0000130178) |
| **Avitus** | 23 | Avitus Kidney Care and Dialysis Center Corp. (+ Avitus Pangasinan, Avitus Davao corps.) | **unknown** | FDA LTO head office: 1759 Rizal Ave, West Bajac-Bajac, Olongapo |
| **Fresenius Kidney Care** | 20 (company says 24 centers) | Fresenius Medical Care Philippines, Inc. (SEC A200108421) / FMC Renalcare Corp. | Fresenius Medical Care AG (Germany) | GLEIF; Fresenius PH site |
| **Hemotek** | 19 | Hemotek Renal Center, Inc. (incorporated June 2008) | Euro-Med Laboratories Phil., Inc. (PSE: EURO, 100%), which is ~58% owned by U.S. Automotive Co., Inc. (Yap family) | Euro-Med 17-A FY2025, 17-Q Q2 2026 (PSE Edge) |
| "Nephrology Center of [city]" | 34 | separate "Nephrology Center of X Dialysis, Inc." corporations | **not verified**: name pattern only | |
| JL Dialmed / TotalCare / Prime Dialysis Center / St. Theresa / Vida / Nephro Synergies / Premier 101 / Pro Renal | 16 / 16 / 15 / 10 / 8 / 8 / 7 / 7 | mostly business names; owners unknown. FDA lists "JL DIALMED TRADING CO." (QC) and "Premier 101 Healthcare Management Inc." (Valenzuela) as LTO holders. | | |
| Others with a confirmed owner | | Clearbridge Medical (Philippines) Inc.: 65% Clearbridge Health Ltd (SGX: 1H3). Healthway: AC Health / Ayala Corp. Six cooperatives matched to CDA registration numbers. | | |

## Key revenue / volume figures
* **PhilHealth HD (RVS 90935) claims paid** (Stats & Charts): PHP 8.38bn (2017), 10.80bn (2018), 10.64bn (2019), 12.58bn (2020), 14.01bn (2021), 17.34bn (2022), 17.44bn (2023), **28.16bn (2024; 5.19m claims)**, **71.68bn (2025; 7.22m claims)**, **48.73bn in H1 2026 (5.41m claims)**. HD has been PhilHealth's top procedure every year.
* **Paid to freestanding dialysis clinics as a facility type**: PHP 14.39bn (2024), 36.83bn (2025; 13% of all PhilHealth claims), 26.09bn (H1 2026). The FDC share of HD spending has risen from 44% (2017) to 51% (2024/25) and 54% (H1 2026). These shares are derived.
* **Accredited FDCs** (SNC): 394 (2019), 433, 492, 559, 624, 705 (2024), 817 (2025), 931 (H1 2026). The 30 Sep 2026 PhilHealth list has 1,012.
* **Package-rate history (checked against the circulars)**:

  | Effective | Rate per session | Split (facility + professional fee) | Sessions per year | Circular |
  |---|---|---|---|---|
  | 28 Jul 2015 | PHP 2,600 | 2,250 + 350 | 90 (45 + 45) | PC 022/024-2015 |
  | CY2020 to CY2022 | PHP 2,600 | | temporary 144 | PC 2021-0002, 2021-0009, 2022-0017 |
  | CY2023 | PHP 2,600 | | 156 institutionalized | PC 2023-0009 |
  | **1 Jul 2024** | **PHP 4,000** | 3,650 + 350; no co-pay | 156 | PC 2024-0014 |
  | **Oct 2024** (signed 7 Oct; effective on publication) | **PHP 6,350** | 6,000 + 350 | 156 (PHP 990,600/yr) | PC 2024-0023 |

  The brief's "2,600 → 4,000 → 6,350, 90 → 156" is correct. One correction: the 90 → 156 change came in 2023 (after temporary 144-session years in 2020 to 2022), and the PHP 4,000 rate dates from July 2024. The NephroPlus RHP's "4,000 in 2023" is wrong.
* **Average paid per HD claim** (derived) is about PHP 4,800 against a PHP 2,600 rate (2017 to 2023), and PHP 9,932 against PHP 6,350 (2025). So one claim covers more than one session, and claim counts must not be read as sessions.
* **Estimates** (marked `estimate`): about 6.7m PhilHealth-paid HD sessions in 2023 and about 11.3m in 2025. That implies about 43k and 72k patient-years at 156 sessions. H1 2026 annualizes to about 98k.
* **NephroPlus PH**: NHCS-PH standalone revenue was INR 238m (FY23), 334m (FY24) and 556m (FY25), with PAT INR 49.7m in FY25. Renal Therapy Solutions made INR 432m in FY25. The group's revenue outside India (PH + Uzbekistan) was INR 2,403m in FY25 (31.8%). It had 41 clinics and 2,276 patients at 30 Sep 2025, and 50 clinics with **686 stations** and about 2,866 patients per month in Jul 2026. 2026 asset deals ran PHP 27m to 152m per site.
* **B. Braun Avitum**: PhilHealth paid it PHP 811m over 2015 to 2018 and PHP 45.2m in IRM advances in 2020 (Senate figures). It had 25 centers in 2020. Its QC branch had 15 machines.
* **Euro-Med (Hemotek parent)**: consolidated "sale of services" PHP 443.4m in H1 2026 against 295.4m in H1 2025. This line includes Hemotek dialysis, and may also include CafeFrance food services, because no segment split is disclosed.
* **Clearbridge PH**: SGD 3.34m (FY2025) against 2.17m (FY2024), driven by dialysis and the PhilHealth rate increases.
* **Frost & Sullivan (via the RHP; third-party estimates)**: market USD 492m (2024) rising to USD 1.36bn (2029F). 54k patients on dialysis in 2024 (82k by 2029F). Average USD 71 per treatment. A deficit of 8,000 stations. The top 5 chains are B. Braun, Hemotek, NephroPlus, Fresenius and Avitus.

## Sources tried

**Reachable and used**
* philhealth.gov.ph: circulars (2015 to 2024), Stats & Charts 2016 to H1 2026, the FDC list. Two circulars (2024-0014 and 2024-0023) are scanned. With no OCR available (I was not allowed to install tesseract), I read the rate tables visually from page images.
* PSE Edge (edge.pse.com.ph): Euro-Med disclosure index, 17-A FY2025 (amended) and 17-Q Q2 2026. Both are scanned and were read visually.
* NephroPlus: RHP (chittorgarh mirror) and DRHP (BSE); NSE/BSE Reg. 30 filing PDFs (nsearchives.nseindia.com, bsmedia.business-standard.com).
* GLEIF API (api.gleif.org): LEI, SEC registration number and parent chains.
* SGX (links.sgx.com): Clearbridge Health AR 2025.
* CDA cooperative masterlist PDF (Dec 2024).
* FDA verification JSON search (verification.fda.gov.ph/api/search).
* News: GMA, Philstar, Tribune, NephroPlus press, The Ken, multibagg/sahi/angelone (secondary summaries of NSE filings; marked medium confidence).

**Blocked or not usable** (no bypass attempted)
* sec.gov.ph and checkwithsec: 403 (Cloudflare). iview: no connection.
* doh.gov.ph, hfsrb, nhfr: 403 (Cloudflare).
* coa.gov.ph: 403, so the COA annual audit reports of PhilHealth were not retrieved.
* emb.gov.ph, hwms, iis: 403. llda.gov.ph: 403. bfp.gov.ph: 403. orus.bir.gov.ph: 403.
* PRC verification: connection reset.
* web.archive.org from the shell: connection reset.
* NSE announcements API: redirect. I did not pursue it, because it needs a browser session.
* malaya.com.ph, inquirer.net, mb.com.ph articles: 403 to WebFetch. Some facts from these are taken from search-result snippets and flagged in the notes.
* alpha.pna.gov.ph: DNS blocked in this session. pna.gov.ph article: 404.
* DTI BNRS: reachable, but every exact-name query (11 tested) returned 0 results, so it gave no owner data.
* Fresenius, B. Braun and freseniuskidneycare.au center pages list no machine or station counts.

## Paid / offline routes for what is missing
1. **SEC**: buy certified copies of the GIS (directors, officers, top-20 shareholders) and the AFS (revenue, assets) for the about 640 corporate operators, through SEC eFAST / CRMD or an accredited retrieval agent. This is the only route to revenue by operator for the private chains: Avitus, the "Nephrology Center of" family, JL Dialmed, TotalCare, Prime and others.
2. **DOH HFSRB**: an eFOI request (foi.gov.ph) for the list of licensed hemodialysis facilities with LTO number, validity and number of HD machines/stations. This is the main source for capacity per center.
3. **PhilHealth**: an eFOI request for claims paid per accredited FDC (amount and count per year, 2019 to 2026). PhilHealth publishes only national and facility-type totals. Per-facility numbers have surfaced only in Senate hearings (e.g. the B. Braun figures from 2020).
4. **COA**: the PhilHealth annual audit reports (2019 to 2025) for dialysis-related audit observations. The site is blocked here, so retry from another network or ask COA.
5. **DTI BNRS** "Request Certification" (paid) for owners of the 304 business-name FDCs. Alternatively, LGU BPLO records via local FOI (these also hold declared gross receipts).
6. **NSE**: download the full NephroPlus announcement list from a browser to capture every Reg. 30 PH acquisition filing. Thirteen are captured here (5 direct PDFs, the rest via secondary summaries).

## Caveats
* Group links based only on a shared name ("same name, multi-site", "name family") are **not** evidence of common ownership. Use `group_link_confidence`.
* Sites bought by NephroPlus in 2026 under asset-transfer agreements still appear under the seller's name in PhilHealth's list until the LTO and accreditation move. `entities.csv` flags these.
* "NEPHROCARE" (seq 373, freseniusmedicalcare.com email) is Fresenius's service brand. "NEPHROCARE HEALTH CARE SERVICES PHILIPPINES" is NephroPlus.
* INR figures from the RHP are not converted. No FX assumptions are embedded in the data.
