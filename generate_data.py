import csv, random
from datetime import date, timedelta
from pathlib import Path
random.seed(42)
OUT=Path(__file__).resolve().parents[1]/'data/raw/business_daily.csv'
OUT.parent.mkdir(parents=True, exist_ok=True)
markets=['Dallas-Fort Worth','Austin','College Station','Oklahoma City']
teams=['Sales','Operations','Marketing']
start=date(2026,1,1)
rows=[]
for d in range(120):
    day=start+timedelta(days=d)
    for m in markets:
      for t in teams:
        leads=max(20,int(random.gauss(80 if t=='Marketing' else 55,12)))
        conv=max(.03,min(.45,random.gauss(.18 if t=='Sales' else .12,.035)))
        customers=max(1,int(leads*conv))
        revenue=customers*max(500,random.gauss(1200,180))
        marketing=max(600,random.gauss(3200 if t=='Marketing' else 1800,450))
        labor=max(1000,random.gauss(5000 if t=='Operations' else 3600,600))
        supplier=max(400,random.gauss(2200,500))
        # inject visible anomalies
        if day.day in (7,21) and m=='Austin' and t=='Sales': revenue*=0.55
        if day.day==15 and m=='Oklahoma City' and t=='Marketing': marketing*=1.8
        rows.append([day,m,t,leads,customers,round(revenue,2),round(marketing,2),round(labor,2),round(supplier,2)])
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['date','market','team','leads','customers','revenue','marketing_spend','labor_cost','supplier_cost']); w.writerows(rows)
print(f'generated {len(rows)} rows -> {OUT}')
