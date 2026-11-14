# Operators / chains, directories and geolocation workstream

Access date for everything below: **2026-11-14**. Every CSV row carries its own `source_url`
and `access_date`. Raw copies of fetched pages are under `raw/operators/`, `raw/geo/`,
`raw/directories/`. Rate limit: about 1.2 to 1.5 s between requests, and 3 s for psn.org.ph,
which sets `Crawl-delay: 3`. robots.txt was checked before crawling each site.

## Outputs

| file | rows | what |
|---|---|---|
| `data/operators/chain_branches.csv` | 569 | 402 PhilHealth-FDC rows assigned to a multi-site operator by name/e-mail rule (`philhealth_match=self`) + 167 branches from operator websites/search snippets (NephroPlus 50, B. Braun 33, Nephro Group/Synergies 33, Hemotek 19, FKC 18, TresMedica 12, CuraKidney 2), each fuzzy-matched back to the PhilHealth list (`philhealth_match`, `philhealth_seq`, `match_score`) |
| `data/operators/operators.csv` | 52 | operator, legal entities, parent, HQ, claimed branch count + date + source, count in the PhilHealth FDC list, count on the website |
| `data/geo/osm_dialysis.csv` | 177 | OSM features (176 with lat/lon), filtered from 189 raw hits (unfiltered set: `raw/geo/osm_dialysis_all_unfiltered.csv`). `category` = dialysis facility (163) / nephrology specialty tag only (9) / hospital-institution (5). 12 rows dropped as false positives (streets "Arenal", shops "Renalyn", Kumon, a parking lot) |
| `data/directories/directory_listings.csv` | 221 | ClinicFinderPH 59, Baxter My Kidney Journey 43, PSN directory 91 (names only), news 2024-2026 28 |
| `data/operators/not_in_philhealth_candidates.csv` | 186 | centres from OSM + operator sites + directories + news that do not match a PhilHealth FDC row on name + municipality, merged across sources. 93 `no_match`, 86 `possible_match` (weak or other-municipality match, check by hand), 7 `generic_name_unmatched`. 70 flagged `likely_hospital_based`: these are expected to be missing from the FDC list, so cross-check them with the PhilHealth hospital list |

### Matching method (`scripts/build_operators_geo.py`)
- rapidfuzz 3.14. Names are cleaned of legal suffixes and generic words (dialysis, center, renal, kidney, inc, ...). The score is 0.7·token_set + 0.3·token_sort.
- Municipalities are normalized: accents removed, "City of"/"City" dropped, Manila districts mapped to Manila, Sto/Sta expanded.
- **matched**: same municipality and score ≥72, or same operator (by rule) and same municipality.
- **matched_name_only**: no municipality and score ≥90 with a strict token_sort ≥85.
- **possible**: same municipality and score 55-72; no municipality and score ≥80; or other municipality and score ≥88 with a different operator.
- Where an OSM row has no `addr:city`, the municipality comes from the nearest point in the HOT/HDX OSM health-facility export, which carries PSGC adm3 names, if it is within 5 km (`city_method` records this). Points near a municipal border can get the neighbouring town: Eastern Marikina Dialysis → Cainta, Renalink → Valenzuela vs Malabon. That is why some exact-name hits show up as `possible_match`.
- Where a website or directory row gives no city, the municipality is inferred from the address text by gazetteer lookup, taking the right-most municipality mention. Known miss: Hemotek Dasmariñas ("Dasmariñas Cavite City") was read as Cavite City, so it shows as a false `no_match`.
- Candidates are merged when they share a municipality and score ≥85, or lie within 150 m of each other and score ≥60.

## Chains found (PhilHealth FDC count / operator-site count / claimed)
- The Nephro Group (Nephrology Center of *, Nephrology Services Phils., Nephro Systems, Nephro Group Dialysis Centers): 39 / 20 (2013-era page) / -. This is a name-pattern grouping, so some "Nephrology Center of X" may be independent.
- B. Braun Avitum Philippines: 34 / 33 locator entries (some are partner hospital units) / 25 (Inquirer 2020).
- NephroPlus (NephroCare Health Care Services Philippines Inc.; formerly Royal Care; acquired Renal Therapy Solutions Inc. 2024, 7 clinics Feb 2025, 5 Aug 2025): 33 / 50 on nephroplus.ph / 53 (Sept 2026).
- Avitus Kidney Care and Dialysis Center (incl. Avitus Davao, Avitus Pangasinan): 23 / no website.
- Fresenius Kidney Care (FMC Renalcare Corp.): 20 / 18 from search snippets / 24 (FMC PH site).
- Hemotek Renal Center Inc.: 19 / 19 on site / -.
- JL Dialmed 16, TotalCare 16, Prime Dialysis Center Inc. 15, St. Theresa('s) 10, Nephro Synergies 8 (+13 hospital-partner units on site), Vida/Avida 8, Nephro Specialist (Cebu) 7, JOrtiz 7, KidneyCare 7, Premier 101 7, Medical Mission Group 7, Pro Renal Specialist 7, The Best Renal Care 7, New Hope 7, One Dialysis Center/TresMedica 6 (12 on tresmedica.com, 255 machines), and about 30 smaller 2-6 site groups (see operators.csv).
- Hospital groups: Healthway/AC Health (3 FDC rows; Iloilo PPP for 13 hospital sites at 8 stations each, signed 2025-11-25; One Ayala 12 stations). Metro Pacific Health has 31 hospitals; their dialysis units are not enumerated here.

## Sources tried

| source | URL | status | used for / rows |
|---|---|---|---|
| Overpass API (main) | overpass-api.de | connection reset | - |
| Overpass kumi.systems / private.coffee / maps.mail.ru | */api/interpreter | 504 / timeout (even trivial query) | - |
| OSM PBF extract (openstreetmap.fr) | download.openstreetmap.fr/extracts/asia/philippines-latest.osm.pbf | OK, 706 MB, replication ts 2026-11-13T00:14Z. **Not kept** (>50 MB) | `scripts/osm_extract_dialysis.py` (pyosmium) → 189 raw → 177 kept |
| Geofabrik | download.geofabrik.de | connection reset | - |
| HDX HOT OSM health facilities | data.humdata.org/dataset/hotosm_phl_health_facilities (S3 geojson zip, updated 2026-10-13) | OK | 19,129 facilities, used as adm3 gazetteer; it is a subset of OSM, so not listed separately |
| healthsites.io | healthsites.io | 200, but the API needs a key; data is OSM-derived | not used |
| B. Braun bbraun.ph centre locator | www.bbraun.ph/en/patient-care/services/care-and-dialysis-centers.html → POST /bin/locationmap (same call the page makes) | OK | 33 PH entries with lat/lon, phone, email, treatment types |
| B. Braun dev mirror | cloud-bbraun-com.dispatcher.dev.cw.bbraun.com | not fetched (dev environment; access refused by policy) | - |
| bbraun.com renal-care-center pages | www.bbraun.com/.../Philippines/*.html | 404 | - |
| NephroPlus | nephroplus.com/ph/sitemap.xml, nephroplus.ph/sitemap.xml, /our-clinics/<city> | OK (the `/clinics/...` detail URLs in the sitemap return a 404 page; city listings work) | 50 branches |
| NephroPlus press | nephroplus.com/press/... ; manilatimes 2024-03-01; mindanaodailynews Sept 2026 | OK (WebFetch) | operator counts |
| Fresenius | freseniusmedicalcare.com/en-ph/clinics/ (robots crawl-delay 10) | OK | "24 Dialysis centers" claim |
| Fresenius Kidney Care centre pages | freseniuskidneycare.ph / .asia / .au /center-detail/phlNNNN | **robots.txt Disallow: /** → not crawled (one page, phl1001, fetched before robots was checked) | 18 rows from search-engine snippets only (`extraction_method`) |
| Hemotek | hemotek.net/?page_id=110 | OK | 19 branches (address, phones, e-mail) |
| Nephro Synergies / Nephro Group | nephrosynergies.com (Joomla, footer (c)2013); nephrogroup.com | nephrosynergies OK; nephrogroup.com does not resolve | 33 rows (13 hospital partnerships, 20 affiliated clinics); may be dated |
| TresMedica (One Dialysis Center) | tresmedica.com/centers/ | OK | 12 centres |
| CuraKidney | curakidney.com | OK | 2 branches; nephrologist roster |
| Avitus | avitus.com.ph, avituskidneycare.com | do not resolve | PhilHealth grouping only |
| Other operator domains taken from e-mails | excelsior.net.ph (Cloudflare 429 challenge, not bypassed), healthfirst.com.ph (403), dckidneycare.com (403), lifestreamdialysis.com ("Coming soon"), juandialysiscenter.com (parked), jortiz.com.ph (no branch info), healthykidneycenter.com / totalcaredialysis.com (empty 114-byte pages), clearbridgemedical.com.ph, reliancehealth.com.ph, dialysiscareplus.com, primedialysis.com.ph, msrhealthcare.com (no DNS), isabelakidneycare.com (single site) | mostly dead | - |
| thebestrenalcare.com | | robots Disallow: / | not crawled |
| ClinicFinderPH | clinicfinderph.com sitemaps (27,267 URLs) → 59 clinic URLs with dialysis/renal/kidney/nephro/hemo in the slug | OK (robots Allow /) | 59 rows with lat/lon, phone, hours (JSON-LD). Note: the site's own category labels are often wrong ("Eye Clinic", "Orthopedic") |
| Baxter My Kidney Journey | apac.mykidneyjourney.com/en-PH/ph-dialysis-centers ("updated as of September 2023") | OK | 43 rows incl. hospitals and PD centres |
| Philippine Society of Nephrology | psn.org.ph/dialysis-center/ (Toolset view renders empty); /wp-json/wp/v2/dialysis-center | REST OK, 91 entries; detail pages have no address | 91 names (no address) |
| KidneyTalksPH | kidneytalks.ph/centres | OK, but derived from the PhilHealth list (May 2026) | not used (duplicate of official list) |
| Yellow Pages PH | www.yellow-pages.ph | connection fails | - |
| Kidney Foundation of the Philippines | kidneyfoundation.org.ph | connection fails | - |
| findhealthclinics.org | | robots blocks town pages | not used |
| Metro Pacific Health / AC Health | news via search (philstar 2026-07-02, iloilo.gov.ph PPP article) | OK | operator rows only |
| News 2024-2026 | PIA, Manila Times, Inquirer, Philstar, MB, SunStar, Politiko, provincial/LGU sites | search summaries (not every page fetched) | 28 rows (`extraction_method=search_summary`) |

## Caveats
- Assigning PhilHealth rows to operators is rule-based (regex on name, plus e-mail domain such as `bbraun`, `fmc-asia`, `hemotek`, `nephrogroup`, `*.pho@gmail.com` for NephroPlus). Generic families such as "Nephrology Center of ..." or "New Hope" may combine unrelated owners.
- No HD-station counts, nephrologist-in-charge or opening years were published per branch on the operator sites I could reach. Those columns stay blank except where a news item gives a machine count (`machines` in directory_listings).
- B. Braun locator coordinates are partly wrong: Mandaluyong at lat 12.59, the Olongapo pin in Quezon City, Roxas (Isabela) at lat 11.1.
- FKC rows marked `search_summary` / `search_snippet` were not crawled; check them before relying on them.
- News-derived rows give status (opened / groundbreaking / announced). Planned centres are included on purpose and labelled.
