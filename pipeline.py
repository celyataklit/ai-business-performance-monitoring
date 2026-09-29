from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/business_daily.csv'; PROC=ROOT/'data/processed/kpi_daily.csv'; ALERTS=ROOT/'outputs/alerts.csv'; SUMMARY=ROOT/'outputs/manager_summary.txt'

def run():
    df=pd.read_csv(RAW,parse_dates=['date'])
    df['conversion_rate']=df['customers']/df['leads']
    df['cac']=df['marketing_spend']/df['customers'].replace(0,np.nan)
    df['total_cost']=df[['marketing_spend','labor_cost','supplier_cost']].sum(axis=1)
    df['contribution_margin']=df['revenue']-df['total_cost']
    df['margin_pct']=df['contribution_margin']/df['revenue'].replace(0,np.nan)
    # 14-observation rolling baseline per market/team
    keys=['market','team']
    for metric in ['revenue','conversion_rate','cac','margin_pct']:
        g=df.groupby(keys)[metric]
        mean=g.transform(lambda s:s.shift(1).rolling(14,min_periods=7).mean())
        std=g.transform(lambda s:s.shift(1).rolling(14,min_periods=7).std()).replace(0,np.nan)
        df[f'{metric}_z']=(df[metric]-mean)/std
    conditions=(df['revenue_z']<-2)|(df['conversion_rate_z']<-2)|(df['cac_z']>2)|(df['margin_pct_z']<-2)
    df['alert']=conditions.fillna(False)
    reasons=[]
    for _,r in df.iterrows():
        x=[]
        if r.get('revenue_z',0)<-2: x.append('revenue below baseline')
        if r.get('conversion_rate_z',0)<-2: x.append('conversion below baseline')
        if r.get('cac_z',0)>2: x.append('CAC above baseline')
        if r.get('margin_pct_z',0)<-2: x.append('margin below baseline')
        reasons.append('; '.join(x))
    df['alert_reason']=reasons
    PROC.parent.mkdir(parents=True,exist_ok=True); ALERTS.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(PROC,index=False)
    alerts=df[df.alert].copy(); alerts.to_csv(ALERTS,index=False)
    latest=df['date'].max(); cur=df[df.date>=latest-pd.Timedelta(days=6)]
    prev=df[(df.date<latest-pd.Timedelta(days=6))&(df.date>=latest-pd.Timedelta(days=13))]
    def pct(a,b): return 0 if b==0 else (a-b)/abs(b)*100
    metrics={
      'Revenue':(cur.revenue.sum(),prev.revenue.sum()),
      'Customers':(cur.customers.sum(),prev.customers.sum()),
      'Contribution Margin':(cur.contribution_margin.sum(),prev.contribution_margin.sum()),
      'CAC':(cur.marketing_spend.sum()/cur.customers.sum(),prev.marketing_spend.sum()/prev.customers.sum())}
    lines=[f'AUTOMATED MANAGER SUMMARY | week ending {latest.date()}', '']
    for k,(a,b) in metrics.items(): lines.append(f'- {k}: {a:,.2f} ({pct(a,b):+.1f}% vs prior 7 days)')
    recent_alerts=alerts[alerts.date>=latest-pd.Timedelta(days=6)]
    lines += ['',f'- Alerts requiring review: {len(recent_alerts)}']
    if len(recent_alerts):
      top=recent_alerts.sort_values('contribution_margin').head(5)
      lines.append('- Priority exceptions:')
      for _,r in top.iterrows(): lines.append(f"  * {r['date'].date()} | {r['market']} | {r['team']} | {r['alert_reason']}")
    lines += ['', 'Recommended action: review flagged market/team combinations, validate source data, then investigate pricing, spend, conversion or cost drivers before operational action.']
    SUMMARY.write_text('\n'.join(lines),encoding='utf-8')
    print(f'processed {len(df)} rows; {len(alerts)} alerts')
if __name__=='__main__': run()
