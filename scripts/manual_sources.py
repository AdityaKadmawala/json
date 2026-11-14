"""Hand-transcribed records from web pages / news articles that are not machine-parseable
(or whose site robots.txt forbids crawling, in which case only search-engine result
titles/snippets were used, never the page itself).

Each record carries its own source_url. `method` says how the values were obtained:
  page_fetched      - the page was downloaded (raw copy under raw/) and transcribed
  search_snippet    - values taken from a web-search result title/snippet of that URL
                      (page itself not crawled, e.g. robots.txt Disallow: /)
  search_summary    - values taken from a web-search tool summary of the article
All accessed 2026-11-14.
"""

ACCESS = "2026-11-14"

# ---------------------------------------------------------------------------
# Fresenius Kidney Care (FMC Renalcare Corp.) - freseniuskidneycare.ph/.asia/.au
# robots.txt on all three domains is "Disallow: /", so only search snippets used.
# ---------------------------------------------------------------------------
FKC = [
    # name, address, city, province, source_url, method, extra
    ("Fresenius Kidney Care Makati", "2257 Chino Roces Ave. Extension, Makati City, Metro Manila 1231", "Makati City", "Metro Manila",
     "https://freseniuskidneycare.au/center-detail/phl1001", "page_fetched",
     {"phone": "63288175791 / 639178209763", "email": "fkc.ph@fmc-asia.com",
      "hours": "Mon-Wed 05:00-18:00; Thu 07:00-15:00; Fri-Sat 05:00-18:00; Sun closed",
      "services": "HD; online HDF; BCM; holiday dialysis", "lat": "14.5404579", "lon": "121.0195363",
      "note": "page fetched once (raw/operators/fkc_au_phl1001.html) before robots.txt Disallow was noticed; no further crawling"}),
    ("Fresenius Kidney Care LRT-2 Cubao", "Diamond Arcade, 873 Aurora Blvd. Cubao, Quezon City, Metro Manila", "Quezon City", "Metro Manila",
     "https://freseniuskidneycare.au/center-detail/phl1002", "search_snippet", {}),
    ("Fresenius Kidney Care Sto. Tomas", "SMP Building, Maharlika Highway, San Rafael, Sto. Tomas, Batangas", "Santo Tomas", "Batangas",
     "https://freseniuskidneycare.asia/center-detail/phl1003/", "search_summary", {}),
    ("Fresenius Kidney Care (SM City Fairview)", "Annex 2 Bldg. SM City Fairview, Lower G/F, Quezon City", "Quezon City", "Metro Manila",
     "https://freseniuskidneycare.au/center-detail/phl1007", "search_snippet", {}),
    ("Fresenius Kidney Care Digos", "Digos City, Davao del Sur", "Digos City", "Davao del Sur",
     "https://freseniuskidneycare.ph/center-detail/phl1008/", "search_summary", {"hours": "Mon-Sat 05:00-23:00"}),
    ("Fresenius Kidney Care Bethany", "New Bethany Building, Ground Floor, Widdoes St., Barangay II, San Fernando City, La Union", "San Fernando City", "La Union",
     "https://freseniuskidneycare.au/center-detail/phl1010", "search_snippet", {}),
    ("Fresenius Kidney Care Capas", "Unit 3-8 Queen's Central Building, G/F, Sto. Domingo I, Capas, Tarlac", "Capas", "Tarlac",
     "https://freseniuskidneycare.au/center-detail/phl1014", "search_snippet", {}),
    ("Fresenius Kidney Care MDMRC", "4th Floor, Metro Davao Medical & Research Center, Davao City", "Davao City", "Davao del Sur",
     "https://freseniuskidneycare.ph/center-detail/phl1016/", "search_summary", {}),
    ("Fresenius Kidney Care LUMC", "La Union Medical Center, Agoo, La Union", "Agoo", "La Union",
     "https://freseniuskidneycare.asia/center-detail/phl1017/", "search_summary", {}),
    ("Fresenius Kidney Care Midsayap", "G/F CLAR Building, Caballero Street, Midsayap, Cotabato", "Midsayap", "Cotabato",
     "https://freseniuskidneycare.ph/center-detail/phl1022/", "search_summary", {"hours": "Mon-Sat; Sun closed"}),
    ("Fresenius Kidney Care Cebu", "CKU Bldg., Ground Floor, J. Llorente St., Capitol Site, Cebu City, Cebu", "Cebu City", "Cebu",
     "https://freseniuskidneycare.au/center-detail/phl2002", "search_snippet", {}),
    ("Fresenius Kidney Care Alabang", "Alabang Town Center, Muntinlupa City", "Muntinlupa City", "Metro Manila",
     "https://freseniuskidneycare.asia/center-detail/phl2005/", "search_summary", {"hours": "Mon-Sat"}),
    ("Fresenius Kidney Care DLSU", "De La Salle University Medical Center, Dasmarinas, Cavite", "Dasmarinas", "Cavite",
     "https://freseniuskidneycare.ph/center-detail/phl2006/", "search_summary", {}),
    ("Fresenius Kidney Care E. Rodriguez", "1054 E. Rodriguez Sr. Ave., Quezon City, Metro Manila", "Quezon City", "Metro Manila",
     "https://freseniuskidneycare.au/center-detail/phl2007", "search_snippet", {"services": "HD; online HDF"}),
    ("Fresenius Kidney Care North EDSA", "Ground Floor, 1026 HPI Bldg., North Edsa, Barangay Ramon Magsaysay, Quezon City", "Quezon City", "Metro Manila",
     "https://freseniuskidneycare.au/center-detail/phl2009", "search_snippet", {}),
    ("Fresenius Kidney Care Shaw", "G/F Littman Building, Jaime Cardinal Sin, Pleasant Hills, Mandaluyong", "Mandaluyong City", "Metro Manila",
     "https://freseniuskidneycare.ph/", "search_summary", {"note": "center-detail URL not given in search result"}),
    ("Fresenius Kidney Care Bankerohan", "Juliana Arcade, Davao City", "Davao City", "Davao del Sur",
     "https://freseniuskidneycare.ph/", "search_summary", {"note": "center-detail URL not given in search result"}),
    ("Fresenius Kidney Care Tagum", "CT North Commercial Building, Apokon Road, Tagum City, Davao del Norte", "Tagum City", "Davao del Norte",
     "https://freseniuskidneycare.ph/", "search_summary", {"note": "center-detail URL not given in search result"}),
]

# ---------------------------------------------------------------------------
# Nephro Synergies (subsidiary of The Nephro Group) - "Affiliated Clinics" page.
# NOTE: site footer "Copyright 2013" - list may be dated.
# ---------------------------------------------------------------------------
NS_URL = "http://www.nephrosynergies.com/index.php?option=com_content&view=article&id=6&Itemid=120"
NEPHRO_GROUP = [
    # (operator, name, address, city, province, phone, kind)
    ("Nephro Synergies", "Victor R. Potenciano Medical Center (Nephro Synergies partner unit)", "EDSA, Mandaluyong City", "Mandaluyong City", "Metro Manila", "(02) 531-4911 loc. 386", "hospital partnership"),
    ("Nephro Synergies", "Universidad de Sta. Isabel - Mother Seton Hospital (Nephro Synergies partner unit)", "Roxas Avenue, Naga City", "Naga City", "Camarines Sur", "(054) 811-8060", "hospital partnership"),
    ("Nephro Synergies", "United Candelaria Doctor's Hospital (Nephro Synergies partner unit)", "Mangilag Sur, Candelaria, Quezon Province", "Candelaria", "Quezon", "(042) 585-2124", "hospital partnership"),
    ("Nephro Synergies", "Medical Center Western Batangas (Nephro Synergies partner unit)", "Brgy. Lanatan, Balayan, Batangas", "Balayan", "Batangas", "(043) 921-3411", "hospital partnership"),
    ("Nephro Synergies", "The Medical City - Iloilo (Nephro Synergies partner unit)", "Locsin Street, Molo, Iloilo City", "Iloilo City", "Iloilo", "(033) 338-1505 to 1513", "hospital partnership"),
    ("Nephro Synergies", "J.P. Rizal Memorial & District Hospital (Nephro Synergies partner unit)", "National Road, Brgy. Bucal, Calamba City, Laguna", "Calamba City", "Laguna", "(049) 521-7759; 0922-4744257", "hospital partnership"),
    ("Nephro Synergies", "NSPI - V.L. Makabali Memorial Hospital", "B. Mendoza St., Sto. Rosario, San Fernando City, Pampanga", "San Fernando City", "Pampanga", "(045) 961-2234 or 2284 loc. 422", "hospital partnership"),
    ("Nephro Synergies", "Gullas Medical Center (Nephro Synergies partner unit)", "Banilad, Mandaue City, Cebu", "Mandaue City", "Cebu", "(032) 268-8886", "hospital partnership"),
    ("Nephro Synergies", "Nephrology Center of St. Alexius", "3/F Beghard Bldg., Alexian Health & Wellness Center, Mac Arthur Highway, Matina, Davao City", "Davao City", "Davao del Sur", "(082) 297-4355", "hospital partnership"),
    ("Nephro Synergies", "Nephrology Center of St. Alexian 2", "G/F Beghard Bldg., Alexian Health & Wellness Center, Mac Arthur Highway, Matina, Davao City", "Davao City", "Davao del Sur", "(082) 233-0811", "hospital partnership"),
    ("Nephro Synergies", "Butuan Medical Center (Nephro Synergies partner unit)", "Baan, Butuan City", "Butuan City", "Agusan del Norte", "", "hospital partnership"),
    ("Nephro Synergies", "Tagum Doctor's Hospital (Nephro Synergies partner unit)", "Tagum Doctors College Highway 54 Rabe Subd., Tagum City", "Tagum City", "Davao del Norte", "", "hospital partnership"),
    ("Nephro Synergies", "Rivera Medical Center (Nephro Synergies partner unit)", "7302 San Francisco, Panabo City", "Panabo City", "Davao del Norte", "(0925) 5527-670", "hospital partnership"),
    ("The Nephro Group", "Nephro Systems Phils. Inc.", "6/F Eastgate Center 169 EDSA, Mandaluyong City", "Mandaluyong City", "Metro Manila", "(02) 534-3226; (02) 531-5344; (02) 534-5952", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Manila", "G/F Ruby Ann Bldg., 911 San Andres cor. Leon Guinto St., Malate, Manila", "Manila", "Metro Manila", "(02) 536-5108 to 10", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Sta. Mesa", "3343 Ramon Magsaysay Blvd., Sta. Mesa, Manila", "Manila", "Metro Manila", "(02) 713-1166; (02) 713-0365", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Caloocan", "522 EDSA, Bgy. Biglang Awa, Caloocan City", "Caloocan City", "Metro Manila", "(02) 361-8484; (02) 361-8283", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of North Caloocan", "G/F Leticia Bldg, 555 Gov. Recto St. Bankers Village, Gate 3, Quirino Highway", "Caloocan City", "Metro Manila", "(02) 961-8974; (02) 961-8980", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Las Pinas", "440 Talon Uno, Alabang-Zapote, Las Pinas City", "Las Pinas City", "Metro Manila", "(02) 800-3775; (02) 800-4579", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Services Phil., Inc. Bicutan", "1st Flr, Asiavest Bldg., 145 Dona Soledad Ave. Better Living, Paranaque City", "Paranaque City", "Metro Manila", "(02) 846-8817", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Services Phil., Inc.", "G/F Bancom Bldg., 146 West Ave., Quezon City", "Quezon City", "Metro Manila", "(02) 926-2821; (02) 926-7280", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Fairview", "G/F Commonwealth Ave., Quezon City", "Quezon City", "Metro Manila", "(02) 442-4101 to 02", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Pasig City", "53 Dr. Sixto Antonio Ave Kapasigan, Pasig City", "Pasig City", "Metro Manila", "(02) 650-2129", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Malolos, Bulacan", "Unit I-8 New Santos Clinic Mac Arthur Hi-Way, Malolos, Bulacan", "Malolos", "Bulacan", "(044) 790-6553", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Imus", "Unit 105 Sun City Plaza Bldg., Anabu 1-B Aguinaldo Highway, Imus, Cavite", "Imus", "Cavite", "0922-8605748", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Cavite", "3F One CT Tower JP Rizal St., Bgy Asis III, Mendez, Cavite", "Mendez", "Cavite", "(046) 861-3013", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Cagayan de Oro", "G/F Physician's Bldg P. Burgos cor T. Chavez Sts, Cagayan de Oro", "Cagayan de Oro City", "Misamis Oriental", "(088) 231-2014", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Batangas City", "Desiree Bldg., Bgy Alangilan, Diversion Road, Batangas City", "Batangas City", "Batangas", "(043) 722-0351", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Bicol", "Miranda Plaza, Rizal St., Legaspi City", "Legazpi City", "Albay", "(052) 481-5211", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Caraga", "Units 10-12 RC Intino Bldg. JC Aquino Ave. Parela Subdivision Butuan City", "Butuan City", "Agusan del Norte", "(085) 341-4488; (085) 341-3641", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Davao City", "J.P. Laurel Ave., Bajada, Davao City", "Davao City", "Davao del Sur", "(082) 300-8300", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of St. Alexius (Alexian Brothers Hospital)", "Alexian Brothers Hospital Matina, Davao City", "Davao City", "Davao del Sur", "(082) 299-3064", "affiliated clinic"),
    ("The Nephro Group", "Nephrology Center of Cebu", "3/F Juanita Bldg, Kamputhaw, Cebu City", "Cebu City", "Cebu", "0932-8712093", "training-page location"),
]

# ---------------------------------------------------------------------------
# TresMedica (operator of One Dialysis Center + LGU partnership centers)
# ---------------------------------------------------------------------------
TM_URL = "https://tresmedica.com/centers/"
TRESMEDICA = [
    # name, address, city, province, phone, status, tags
    ("One Dialysis Center - Cainta", "2nd Floor, Medical Arts Building", "Cainta", "Rizal", "(02) 8813-3064", "operating", "Free for residents"),
    ("Marikina Dialysis Center", "4th Floor, Marikina Sports Complex, McDonald's Avenue, Santo Nino", "Marikina City", "Metro Manila", "(02) 8288-7592", "operating", "LGU Partnership; Free for residents; Mon-Sat 8AM-5PM"),
    ("Aksyon Agad Dialysis Center", "Mini City Hall, Road 15, Barangay Bahay Toro", "Quezon City", "Metro Manila", "(02) 8287-8662", "operating", "LGU Partnership; Free for underprivileged"),
    ("One Dialysis Center - Malabon", "LG Floor, Ospital ng Malabon, F. Sevilla Blvd., Brgy. Tanong", "Malabon City", "Metro Manila", "0916 543 0822", "operating", ""),
    ("One Dialysis Center - Marikina", "Marikina City", "Marikina City", "Metro Manila", "", "operating", ""),
    ("GT Dialysis and Diagnostic Center", "Muntinlupa City", "Muntinlupa City", "Metro Manila", "", "operating", "GT Partnership"),
    ("ILove San Mateo Dialysis Center", "San Mateo, Rizal", "San Mateo", "Rizal", "", "opening soon", "LGU Partnership"),
    ("KAISA Dialysis Center", "Sta. Cruz, Laguna", "Santa Cruz", "Laguna", "", "opening soon", "LGU Partnership"),
    ("One Dialysis Center - Mactan, Cebu", "Lapu-Lapu City, Mactan", "Lapu-Lapu City", "Cebu", "", "operating", ""),
    ("One Dialysis Center - Consolacion, Cebu", "Consolacion, Cebu", "Consolacion", "Cebu", "", "opening soon", ""),
    ("MY Mayor Cares Dialysis Center", "Purok 9, Poblacion", "", "Davao de Oro (area filter on page; not explicit)", "", "operating", "LGU Partnership"),
    ("Bukidnon Dialysis Center", "Bukidnon", "", "Bukidnon", "", "opening soon", "LGU Partnership"),
]

CURAKIDNEY_URL = "https://www.curakidney.com/"
CURAKIDNEY = [
    ("CuraKidney - Ayala Malls Feliz", "Ayala Malls Feliz, Pasig City", "Pasig City", "Metro Manila", "+6386524846", "Mon-Sat 6am-1am"),
    ("CuraKidney - Camaro Square", "Camaro Square, 87 Camaro St, Novaliches, Quezon City", "Quezon City", "Metro Manila", "+6386524846", "Monday to Saturday, 6am-1am"),
]

# ---------------------------------------------------------------------------
# News: openings / announced centres 2024-2026 (method = search_summary unless noted)
# (name, address, city, province, status, date, machines, operator, source_url, note)
# ---------------------------------------------------------------------------
NEWS = [
    ("Samar Provincial Hospital Dialysis Center", "Samar Provincial Hospital", "Catbalogan City", "Samar", "opened", "2026-03-18", "", "Provincial Government of Samar",
     "https://pia.gov.ph/news/provincial-hospital-opens-dialysis-center-expands-access-to-lifesaving-care/", "hospital-based; designed for 30-45 patients/day"),
    ("SPMC Kidney and Transplant Institute Renal Dialysis Unit", "Southern Philippines Medical Center, J.P. Laurel Ave.", "Davao City", "Davao del Sur", "opened", "2026-06-30", "133", "DOH - Southern Philippines Medical Center",
     "https://pia.gov.ph/news/spmc-kidney-center-opens-with-133-dialysis-machines/", "hospital-based; further 100-machine expansion reported Oct 2026 (businessmirror.com.ph/2026/10/27)"),
    ("One Dialysis Center Mactan", "Barangay Pajac", "Lapu-Lapu City", "Cebu", "opened", "2026-09", "", "One Dialysis Center (TresMedica)",
     "https://visayas.politiko.com.ph/2026/09/16/new-dialysis-center-opens-in-lapu-lapu/daily-feed/", ""),
    ("NephroPlus Dialysis Center - Villarosa Hospital", "inside Villarosa Hospital", "Quezon City", "Metro Manila", "opened", "2026-09", "", "NephroPlus",
     "https://mindanaodailynews.com/nephroplus-expands-footprint-to-eight-centers-across-visayas-and-mindanao-opens-new-greenfield-center-in-quezon-city/", "hospital-based greenfield centre; page fetched via WebFetch"),
    ("Alicia Dialysis Center (Prime Dialysis Center Inc.)", "Commercial Center, Barangay Aurora", "Alicia", "Isabela", "opened", "2025-03-24", "", "Prime Dialysis Center Inc.",
     "https://manilastandard.net/lgu/314577098/alicia-town-now-has-new-dialysis-center.html", ""),
    ("Pagadian City LGU Dialysis Center", "Ground floor, City Health Office", "Pagadian City", "Zamboanga del Sur", "opened", "2025-03-21", "", "Pagadian City LGU",
     "https://newsinfo.inquirer.net/2046668/pagadian-city-lgu-opens-dialysis-center", "LGU-owned"),
    ("Lingayen District Hospital Dialysis Center", "Lingayen District Hospital", "Lingayen", "Pangasinan", "opened", "2025-04", "13", "Provincial Government of Pangasinan",
     "https://www.manilatimes.net/2025/04/14/regions/new-dialysis-center-opens-in-pangasinan/2091508", "hospital-based"),
    ("Pampanga Provincial Dialysis Center 1", "Guagua", "Guagua", "Pampanga", "opened", "2025-04-11", "43", "Provincial Government of Pampanga",
     "https://pia.gov.ph/news/luzon/cl/pampanga-opens-dialysis-center-in-guagua/", ""),
    ("Malolos City Hemodialysis Center (PPP with Premier 101)", "", "Malolos", "Bulacan", "opened", "2025-09-16", "40", "City of Malolos / Premier 101 Healthcare Management Inc.",
     "https://pia.gov.ph/news/luzon/cl/first-ppp-dialysis-center-in-malolos-covered-by-philhealth/", "also manilatimes.net/2025/09/21/regions/malolos-lgu-philhealth-offer-free-dialysis-treatment/2187708"),
    ("Laguna Medical Center Free Dialysis Center", "Laguna Medical Center", "Santa Cruz", "Laguna", "opened", "2025-12-08", "", "Provincial Government of Laguna (PPP)",
     "https://journaldailynewsonline.com.ph/index.php/2025/11/19/free-dialysis-center-for-kidney-patients-to-open-in-laguna-on-december-8/", "Pakil, Cabuyao, Bay centres reported in development"),
    ("Balilihan Hemodialysis Center", "", "Balilihan", "Bohol", "turned over, not yet operational", "2025-12-09", "", "DOH-7 / Balilihan LGU",
     "https://theboholtribune.com/2025/12/14/doh-7-turns-over-hemodialysis-center-to-balilihan-lgu/", ""),
    ("Tacurong People's Dialysis Center", "", "Tacurong City", "Sultan Kudarat", "groundbreaking", "", "", "Tacurong City LGU",
     "https://tacurong.gov.ph/lgu-tacurong-breaks-ground-on-peoples-dialysis-center/", "3-storey building, 9 dialysis rooms"),
    ("Guadalupe Dialysis Center (Cebu City)", "Barangay Guadalupe", "Cebu City", "Cebu", "opened", "2026-02", "15", "Cebu City Government",
     "https://www.philstar.com/the-freeman/cebu-news/2026/02/10/2507031/city-opens-free-dialysis-centers", "free"),
    ("Talamban Dialysis Center (Cebu City)", "Barangay Talamban", "Cebu City", "Cebu", "opened", "2026-02", "10", "Cebu City Government",
     "https://www.philstar.com/the-freeman/cebu-news/2026/02/10/2507031/city-opens-free-dialysis-centers", "free"),
    ("Manila City Hemodialysis Center - Pedro Gil", "Pedro Gil", "Manila", "Metro Manila", "groundbreaking", "2026-08", "", "City of Manila",
     "https://mb.com.ph/2026/08/13/new-dialysis-center-to-rise-on-pedro-gil-in-manila", ""),
    ("Flora V. Valisno De Siojo Dialysis Center (100-machine expansion)", "Gat Andres Bonifacio Memorial Medical Center, 8001 Delpan St., Tondo", "Manila", "Metro Manila", "groundbreaking/upgrade", "2026-08", "100", "City of Manila / Prime Dialysis Center Inc.",
     "https://mb.com.ph/2026/08/28/100-machine-dialysis-center-to-offer-free-treatment-in-manila", "existing B. Braun-run 'City of Manila Dialysis Center' at same address"),
    ("Cavite City Government Dialysis Center", "", "Cavite City", "Cavite", "opened", "2026-10", "", "Cavite City LGU",
     "https://southluzon.politiko.com.ph/2026/10/06/mayor-denver-chua-inaugurates-the-cavite-city-governments-dialysis-center/daily-feed/", "free"),
    ("Alfonso Dialysis Center", "", "Alfonso", "Cavite", "announced (to start July 2026)", "2026-06", "", "Alfonso LGU",
     "https://southluzon.politiko.com.ph/2026/06/23/randy-salamat-alfonso-dialysis-center/daily-feed/", "opening not confirmed"),
    ("Ilocos Sur Medical Center Hemodialysis Unit", "Ilocos Sur Medical Center", "Candon City", "Ilocos Sur", "opened", "", "12", "Provincial Government of Ilocos Sur",
     "https://pia.gov.ph/news/ilocos-sur-medical-center-opens-hemodialysis-unit-to-enhance-patient-care/", "hospital-based"),
    ("Andres B. Bernos Memorial Hemodialysis Center", "La Paz Municipal Hospital", "La Paz", "Abra", "opened", "2024", "18", "LGU La Paz / Abra",
     "https://pia.gov.ph/free-dialysis-center-for-abrenians-opens-in-la-paz-abra/", "free; hospital-based"),
    ("Western Pangasinan District Hospital Dialysis Center", "Western Pangasinan District Hospital", "Alaminos City", "Pangasinan", "opened", "", "15", "Provincial Government of Pangasinan",
     "https://www.pangasinan.gov.ph/dialysis-center-in-wpdh-now-open/", "hospital-based"),
    ("Sarangani Provincial Dialysis Center", "", "Alabel", "Sarangani", "groundbreaking", "2024-02", "", "Provincial Government of Sarangani",
     "https://mirror.pia.gov.ph/press-releases/2024/02/28/sarangani-breaks-ground-on-first-dialysis-center-in-alabel", "opening not confirmed"),
    ("Navotas City Hospital Dialysis Unit", "Navotas City Hospital", "Navotas City", "Metro Manila", "operating (expanded)", "2024-02", "", "Navotas City LGU",
     "https://mirror.pia.gov.ph/news/2024/02/26/more-patients-can-avail-of-free-dialysis-treatment-in-navotas-city-hospital", "hospital-based; free"),
    ("Chong Hua Hospital Renal Unit", "Don Mariano Cui Street, Fuente Osmena", "Cebu City", "Cebu", "opened", "2026-06-04", "70", "Chong Hua Hospital",
     "https://chonghua.com.ph/announcement/chong-hua-hospital-opens-the-largest-dialysis-center-in-the-visayas-2/", "hospital-based; 70 DOH-authorized stations (2026 LTO); campus address from Baxter directory"),
    ("Crystal Care Hemodialysis", "", "Davao City", "Davao del Sur", "opened", "", "", "",
     "https://www.sunstar.com.ph/davao/feature/crystal-care-hemodialysis-opens-in-davao-providing-kidney-care-services", ""),
    ("American Nephrology Care and Services Corp. (ANCSC)", "Ground floor, Bridges Town Square, Plaridel St.", "Mandaue City", "Cebu", "opened", "", "", "American Nephrology Care and Services Corp.",
     "https://www.sunstar.com.ph/more-articles/new-mall-based-clinic-offers-texas-standard-hemodialysis", "mall-based"),
    ("Healthway Multi-Specialty Center One Ayala - Dialysis Center", "One Ayala", "Makati City", "Metro Manila", "opened", "2026-07", "12", "AC Health / Healthway Medical Network",
     "https://www.philstar.com/business/banking/2026/07/07/2540275/healthway-opens-biggest-multi-specialty-clinic", "12 stations"),
    ("Pampanga Provincial Dialysis Center II", "", "Apalit", "Pampanga", "opened", "2025-12", "", "Provincial Government of Pampanga",
     "https://pia.gov.ph/dialysis-center-to-open-in-pampanga-town/", ""),
]
