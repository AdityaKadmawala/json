"""Bundle the main CSVs into one Excel workbook: data/PH_dialysis_centers.xlsx"""
import pandas as pd
sheets = {
    'centers': 'data/dialysis_centers_philippines.csv',
    'legal_regulatory': 'data/legal/legal_regulatory_events.csv',
    'ownership': 'data/corporate/ownership.csv',
    'entities': 'data/corporate/entities.csv',
    'financials_volume': 'data/corporate/financials_volume.csv',
    'market_context': 'data/market/market_context.csv',
    'operators': 'data/operators/operators.csv',
    'chain_branches': 'data/operators/chain_branches.csv',
    'candidates_not_in_PH': 'data/operators/not_in_philhealth_candidates.csv',
    'osm_dialysis': 'data/geo/osm_dialysis.csv',
    'directories': 'data/directories/directory_listings.csv',
    'covid_irm_2020': 'data/legal/philhealth_irm_dialysis_recipients_2020.csv',
    'fda_lto_lookups': 'data/corporate/fda_lto_lookups.csv',
    'philhealth_hospitals': 'data/philhealth_hospitals_2026-09-30.csv',
}
with pd.ExcelWriter('data/PH_dialysis_centers.xlsx', engine='openpyxl') as xw:
    for name, path in sheets.items():
        df = pd.read_csv(path, dtype=str).fillna('')
        df.to_excel(xw, sheet_name=name, index=False)
        ws = xw.sheets[name]
        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = ws.dimensions
        for col in ws.columns:
            width = min(60, max(10, max(len(str(c.value or '')) for c in col[:200]) + 2))
            ws.column_dimensions[col[0].column_letter].width = width
        print(f'{name}: {len(df)} rows')
