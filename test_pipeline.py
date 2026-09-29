from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def test_outputs_exist():
    assert (ROOT/'data/processed/kpi_daily.csv').exists()
    assert (ROOT/'outputs/alerts.csv').exists()
def test_kpis():
    df=pd.read_csv(ROOT/'data/processed/kpi_daily.csv')
    for c in ['conversion_rate','cac','contribution_margin','margin_pct','alert']:
        assert c in df.columns
    assert df['conversion_rate'].between(0,1).all()
