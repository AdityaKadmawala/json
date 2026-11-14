# Legal cases and regulatory actions: dialysis centers, operators and owners (Philippines)

Workstream: legal and regulatory events. Compiled 2026-11-14.

## Outputs

| File | Contents |
|---|---|
| `data/legal/legal_regulatory_events.csv` | 47 events. Columns: `entity_name, matched_center_name, people_named, event_type, forum, case_number, date, status_outcome, finding_level, summary, source_url, source_type`. `finding_level` is an extra column that separates allegations from findings: `allegation`, `investigation`, `complaint_filed`, `probable_cause`, `appeal`, `case_pending`, `procedural_dismissal`, `agency_action`, `agency_decision`, `audit_finding`, `court_decision`, `court_decision_final`, `final_decision_executed`, `legislative_finding`, and others. |
| `data/legal/philhealth_irm_dialysis_recipients_2020.csv` | 58 dialysis-related rows from PhilHealth's 2020 Interim Reimbursement Mechanism (IRM) recipient and liquidation list as of 2023-07-12. 46 rows match a name in the PhilHealth FDC list. Senate and DOH found the IRM releases to freestanding dialysis clinics improper. This file is context and does not list sanctions: every row shows 100% liquidated. |
| `raw/legal/` | Primary documents: lawphil HTML for G.R. 271209 and G.R. 153413; PhilHealth statements (2019 WellMed statements, the 2019 fraud-count statement, and the 2018 fines statement); PhilHealth Board Assessment reports for 2020, 2022 and 2023, which list the WellMed, Almazan, St. Theresa and NKTI appeals; IRM update and recipient list (PDF and text); Nephrocare Health Services Ltd prospectus (SEBI, Dec 2025, 12 MB) with an excerpt of its litigation section. `raw/legal/news_snapshots/` holds text snapshots of the news articles cited. |

`matched_center_name` holds the exact name string from `data/philhealth_fdc_2026-09-30.csv`. For chain operators, one name covers many facilities. In the FDC list, B. BRAUN AVITUM PHILIPPINES, INC. appears at 34 facilities, ST. THERESA DIALYSIS CENTER (INC.) at 10, HEMOTEK RENAL CENTER, INC. at 19, Fresenius Kidney Care/FMC Renal Care at 19, and Nephrocare Health Care Services Philippines at 19. Events at chain level are not tied to a single branch unless the source names one. The GABMMC Tondo branch, FDC seq 322, is the B. Braun facility in the COA finding. WellMed, SouthMed, TriHDCare, Nephroprime and the unnamed centers are not in the current FDC list.

## Counts by event_type (47 rows)

court_case 11; philhealth_sanction 6; philhealth_appeal 4; coa_audit 4; senate_hearing 3; doj_complaint 2; philhealth_investigation 2; one each: nbi_complaint, doj_resolution, ombudsman_complaint, senate_resolution, senate_privilege_speech, senate_report, doh_statement, philhealth_prosecution, philhealth_audit, labor_case, labor_dispute, dole_action, nbi_raid, denr_action, lgu_action.

By source_type: 15 primary (lawphil, PhilHealth, SEBI), 29 news, 3 secondary (2 union reports, 1 party pleading).

## Most significant matters

1. **WellMed Dialysis and Laboratory Center Corp. ("ghost dialysis", 2016–2019 claims).** 21 rows.
   - Agency actions: PhilHealth administrative cases (28 counts announced; 5 formal charges or 83 counts later reported), a temporary suspension of payment (13–14 June 2019), and withdrawal of accreditation (18 June 2019).
   - Criminal case: the NBI arrested owner Bryan Sy and filed charges, and the DOJ found probable cause on 17 counts of estafa through falsification (14 June 2019). QC RTC Branch 219 dismissed the case for lack of jurisdiction (5 Aug 2019). Prosecutors refiled it in the QC MeTC, where it is pending. The CA (11th Div., 30 Oct, year inferred as 2025) blocked the discharge of co-accused whistleblower Liezel de Leon as state witness.
   - Accreditation appeal: WellMed's appeal (PHIC Case No. HCP-NCR-19-0248 to 0260) was affirmed by the PhilHealth Board and then by the CA. The CA decision date is not verified; it was reported by Inquirer around 2023.
   - Related physician case: in G.R. No. 271209 (SC, 19 Aug 2024), the SC affirmed CA-G.R. SP No. 169097, which set aside PhilHealth's withdrawal of a WellMed-linked nephrologist's accreditation. Only the PhilHealth Board can revoke an accreditation, and due process had been violated. The ruling does not clear WellMed.
   - Spin-offs: the NBI filed a graft complaint against 21 PhilHealth officials (Aug 2019; no outcome found). Senate SR No. 3, a Lacson privilege speech and a Health Committee hearing followed. COA's 2019 PhilHealth audit found PRO-NCR paid 114 claims (P1.872M) before suspending payment.
2. **B. Braun Avitum Philippines, Inc.**
   - Senate Committee of the Whole, Aug 2020: allegations of sessions above capacity (PhilHealth MIDAS data), P45M+ in IRM advances, and the P9.7M credited to the wrong rural bank. The company denied these. The Senate report found IRM releases to freestanding dialysis clinics illegal.
   - Ombudsman, 11 Jan 2021: NBI graft and administrative complaint against former PhilHealth president Morales, 13 other PhilHealth officials and 3 B. Braun officers over P33.8M in IRM funds. Subsidiary TMS received P15.97M. No resolution found.
   - COA, Aug 2021: the 2014 joint venture agreement for the GABMMC (Manila) dialysis center was found disadvantageous to the city.
   - All of these are allegations, complaints or audit findings. None is an adjudicated finding against the company.
3. **NephroPlus group (Nephrocare Health Care Services Philippines Inc.)**, from the SEBI prospectus (primary):
   - RTC Manila civil suit (filed 10 Feb 2025) against Royal Care Dialysis Center Inc., Asialife Health Care Corp. and Sunil Chellani, to recover PHP 13.67M in PhilHealth reimbursements.
   - NLRC RAB-NCR Branch 50 complaint by a former consultant accountant.
   - Qualified-theft complaint against a former accounting officer, filed with the QC prosecutor.
   - All three are pending.
4. **SouthMed Dialysis Center / Adventist Hospital Cebu.** PhilHealth found the tenant dialysis clinic filed claims through the hospital. The penalty was a 3-month suspension and a P10,000 fine, affirmed by the CA (2017) and the SC, and executed from 1 Aug to 29 Oct 2021.
5. **TriHDCare / TriCity Medical Center (Pasig).** The NBI filed a DOJ complaint (2021) over 318 claims for dead dialysis patients. Pasig MeTC Branch 153 convicted a claims clerk on 46 counts (1 July 2024), on the provider's own complaint.
6. **Other items:**
   - PhilHealth Board appeals involving Almazan Renal Care Center (HCP-NCR-16-2142) and St. Theresa Dialysis Center, Inc. (MR of PBR 2593 s. 2021). The nature of the charges and the outcomes are not published.
   - Fresenius Kidney Care: union-reported DOLE findings of labour-standards and OSH violations (Jan 2023).
   - NBI raid on an unnamed Dasmariñas, Cavite center over unregistered "Diacid" dialysis concentrate (Aug 2024).
   - DENR-EMB 7 notice of violation to an unnamed Bogo City center over medical waste (Jun 2025).
   - Nephroprime Corp. pulled out of the La Carlota (Negros Occ.) government HD center (Jul 2025).
   - COA findings of idle dialysis machines in provincial hospitals.
   - Intra-corporate SC case Raniel v. Jochico (Nephro Systems Dialysis Center, G.R. 153413, 2007). It may relate to NEPHRO SYSTEMS PHILS., INC. (FDC seq 372), but that is not verified, so it is not matched.

## Data-quality rules applied

- Allegations, complaints, probable-cause findings, audit observations and court decisions are kept apart in `status_outcome` and `finding_level`. No row presents an allegation as a finding.
- `people_named` lists only names that appear in the cited court, official or news source, and mainly owners, officers and directors. Respondents who are public officials are named where the news source names them. Low-level private individuals (clerks, a former accounting officer, a consultant complainant) are described by role, not by name. A Senate-hearing allegation that a PhilHealth official owned B. Braun was denied and is mentioned without the name. No names are taken from the Scribd-hosted Hemotek pleading.
- Some figures differ between sources and are kept as reported: B. Braun IRM of P33.8M (NBI) versus P45M+ (Senate); WellMed P4.24M (Lacson) versus PhilHealth's statement that payments stopped in Feb 2019; de Leon described as a former WellMed employee (GMA) or a "PhilHealth official" (Philstar).
- Gaps:
  - The status after 2019–2021 of the NBI/DOJ complaint against 21 PhilHealth officials, of the B. Braun IRM Ombudsman complaint, of the TriCity complaint against the other respondents, and of the WellMed MeTC trial could not be found.
  - The CA decision date in the WellMed accreditation appeal could not be confirmed. inquirer.net blocks both curl and WebFetch with 403, so only search snippets were available.

## Searches done

- **WebSearch:** about 60 queries, covering these themes:
  - WellMed and its owners, the RTC/MeTC/CA case, state-witness status, the NBI complaint against 21 PhilHealth officials, and Senate resolutions and hearings.
  - B. Braun: IRM, Senate, Ombudsman, and the COA/GABMMC finding.
  - "ghost dialysis" beyond WellMed and the "19 dialysis centers"; PhilHealth fraud cases from 2022 to 2026.
  - SC, CA and Sandiganbayan cases with "dialysis", "hemodialysis", "Dialysis Center, Inc." or "Kidney Center" (lawphil, chanrobles, jur.ph, lawyerly, elibrary).
  - NLRC and labor (dialysis nurses, Fresenius, B. Braun, Nephrology Center); CTA and tax; malpractice involving hemodialysis deaths.
  - PCC and NephroPlus acquisitions; the NephroPlus DRHP and prospectus; Royal Care and Sunil Chellani.
  - DOH licence suspension, closures and CDOs; FDA advisories on dialysis products; NBI raids; infection outbreaks.
  - COA observations on dialysis (PPPs, idle machines, the PhilHealth hemodialysis package); Ombudsman cases on dialysis contracts and procurement.
  - Business-permit and LGU closures; DENR; PhilHealth balance billing and the Dialysis Coalition; House and Senate hearings from 2023 to 2025.
  - Named entities: St. Theresa, Almazan, Hemotek, Kidney Foundation, Nephro Synergies, Nephrology Center, Fresenius.
- **PhilHealth site (curl, rate-limited at 1 request/s):**
  - Crawled the news archive indexes for 2011–2026 and the advisories indexes for 2006–2026 (1,552 advisories) and filtered titles by keyword.
  - The advisories contain no named list of sanctioned dialysis HCIs. Only collecting agents and banks are named in suspension or non-renewal advisories.
  - Downloaded the IRM recipient and liquidation lists.
  - Downloaded and text-searched the Board and CAAC transparency reports for 2019–2025, which is where the WellMed, Almazan, St. Theresa and NKTI appeals were found.
- **PCC (phcc.gov.ph, curl):** scanned 22 pages of Commission Decisions plus the letters-of-non-coverage page. No dialysis-related merger decision was found; NephroPlus' PH acquisitions are likely below the notification thresholds.
- **SEBI (curl):** Nephrocare Health Services Ltd final prospectus (Dec 2025), section "Outstanding Litigation and Material Developments".

## Sources: reachable or blocked (from this sandbox)

| Source | Status |
|---|---|
| lawphil.net | Reachable with curl (used) |
| www.philhealth.gov.ph | Reachable with curl (used: news, advisories, IRM, board transparency) |
| philstar.com, gmanetwork.com, bworldonline.com, sunstar.com.ph, currentph.com, digicastnegros.com, visayandailystar.com, corpwatch.org | Reachable with curl |
| sebi.gov.in, phcc.gov.ph, cta.judiciary.gov.ph, ca.judiciary.gov.ph, lawyerly.ph | Reachable with curl (homepages) |
| newsinfo.inquirer.net, mb.com.ph, abs-cbn.com, rappler.com | 403 for curl and WebFetch; search snippets only |
| pna.gov.ph, officialgazette.gov.ph, legacy.senate.gov.ph, web.senate.gov.ph, coa.gov.ph, fda.gov.ph, privacy.gov.ph (NPC), nlrc.dole.gov.ph | 403 |
| elibrary.judiciary.gov.ph, sec.gov.ph, doh.gov.ph, foi.gov.ph | 403 (per brief; not retried) |
| ombudsman.gov.ph, sb.judiciary.gov.ph | Connection reset or timeout |
| jur.ph | 429 (rate-limited) |
| web.archive.org | Connection reset for curl; WebFetch refused |
| scribd.com | Client challenge; not readable |
| uniglobalunion.org | Redirect loop |

No attempt was made to bypass bot protection.

## Not found or no public record located

- No public DOH, FDA or CHD order suspending, revoking or closing a named dialysis clinic's licence. Only the regulatory framework turned up: DOH AO 2012-0001 and earlier AOs.
- No PCC review of a dialysis transaction.
- No NPC (data privacy) case.
- No BIR or CTA case against a PH dialysis operator. The NephroPlus prospectus reports only aggregate subsidiary tax claims, not by country.
- No reported medical-malpractice decision against a PH dialysis center.
- No Sandiganbayan case specific to dialysis.

## Recommended paid or offline routes

1. **Courts:**
   - Supreme Court e-Library and the SC Judicial Records Office for unsigned resolutions, e.g. Adventist Hospital Cebu v. PhilHealth, and for any petitions by WellMed.
   - CA Docket Inquiry (ca.judiciary.gov.ph) by party name for WellMed, B. Braun Avitum, Hemotek, St. Theresa and Almazan. This is where the CA-G.R. SP number of the WellMed accreditation appeal would be found.
   - The eCourt/PhilJA case-status kiosks, or a Certificate of Pending/No Pending Case from the Office of the Clerk of Court, for the QC MeTC (WellMed estafa), RTC Manila (Nephrocare v. Royal Care), and Pasig MeTC Branch 153 (TriCity).
2. **Prosecution:** DOJ National Prosecution Service records request on the NBI complaint against the 21 PhilHealth officials (2019) and on the TriCity respondents (2021). Office of the Ombudsman "Case Status" request on the B. Braun IRM complaint (NBI, 11 Jan 2021).
3. **PhilHealth:**
   - eFOI request (foi.gov.ph; it returns 403 to automated access, so file manually) for the list of HCIs with withdrawn, suspended or denied accreditation and fines since 2015 filtered to dialysis facilities.
   - Copies of PBR 2593 s. 2021 (St. Theresa) and the Board decisions in HCP-NCR-16-2142 (Almazan) and HCP-NCR-19-0248 to 0260 (WellMed).
   - The internal "Audit on Hemodialysis Package" (2022).
   - The PROSEC docket for Hemotek.
4. **DOH-HFSRB and CHDs:** FOI request for licence suspensions, revocations and cease-and-desist orders issued to hemodialysis clinics under AO 2012-0001.
5. **SEC:** SEC i-View/eSPARC purchase of GIS and AFS for WellMed Dialysis and Laboratory Center Corp., B. Braun Avitum Philippines, TMS Philippines, Royal Care Dialysis Center Inc. and Asialife Health Care Corp. AFS notes disclose contingent liabilities and litigation. Intra-corporate cases before 2000 sit at the SEC; later ones are at the RTC Special Commercial Courts.
6. **NLRC and DOLE:** NLRC case-status inquiry by respondent name (B. Braun Avitum, FMC Renal Care Corp., Asia Renal Care Corp., Mindanao Renal Care, Nephrocare PH). DOLE-NCR FOI request for the 2022–2023 Fresenius inspection results and compliance orders.
7. **COA:** download Annual Audit Reports (coa.gov.ph is blocked here, so fetch manually) for PhilHealth (CY2019–2025, dialysis and IRM observations), City of Manila/GABMMC (CY2020–2021), and DOH-retained hospitals running dialysis PPPs (BGHMC dialysis PPP).
8. **Senate:** Committee of the Whole report on the PhilHealth inquiry (Sept 2020) and the 18th-Congress SR No. 3 hearing transcripts, from the Senate Legislative Bills and Index Service.
9. **News archives:** an Inquirer/PressReader subscription for the full texts blocked here, in particular articles 1764986, 2139125, 1324626 and 1479339.
