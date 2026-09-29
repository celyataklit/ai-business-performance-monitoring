-- Warehouse-ready KPI model (ANSI-style SQL)
SELECT
  date, market, team,
  SUM(leads) AS leads,
  SUM(customers) AS customers,
  SUM(revenue) AS revenue,
  SUM(marketing_spend) AS marketing_spend,
  SUM(revenue) - SUM(marketing_spend + labor_cost + supplier_cost) AS contribution_margin,
  SUM(customers) * 1.0 / NULLIF(SUM(leads),0) AS conversion_rate,
  SUM(marketing_spend) * 1.0 / NULLIF(SUM(customers),0) AS cac
FROM business_daily
GROUP BY date, market, team;
