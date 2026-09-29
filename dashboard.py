from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/processed/kpi_daily.csv',parse_dates=['date'])
weekly=df.groupby(pd.Grouper(key='date',freq='W')).agg(revenue=('revenue','sum'),margin=('contribution_margin','sum'),customers=('customers','sum'),marketing=('marketing_spend','sum')).reset_index()
weekly['cac']=weekly.marketing/weekly.customers
fig,ax=plt.subplots(figsize=(10,5)); ax.plot(weekly.date,weekly.revenue,label='Revenue'); ax.plot(weekly.date,weekly.margin,label='Contribution margin'); ax.set_title('Automated Business Performance Scorecard'); ax.set_ylabel('USD'); ax.legend(); fig.tight_layout(); fig.savefig(ROOT/'outputs/performance_scorecard.png',dpi=160); plt.close(fig)
print('dashboard saved')
