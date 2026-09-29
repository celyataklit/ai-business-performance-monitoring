# 4-5 minute Loom script

## 0:00-0:35 — Problem
“Hi, I’m Celya. I built this AI-ready Business Performance Monitoring and Alert System as a portfolio demonstration. The problem I wanted to solve is common in growing multi-market businesses: teams manually pull reports, reconcile KPIs, and managers often see issues too late. The dataset here is synthetic, so I’m not presenting these results as a former employer deployment.”

## 0:35-1:20 — Architecture
“Raw daily market and team data enters the pipeline. Python and SQL create a trusted KPI layer: conversion rate, customer acquisition cost, contribution margin and margin percentage. I intentionally keep these calculations deterministic and auditable. Then a rolling anomaly layer compares each market and team with its own recent baseline.”

## 1:20-2:20 — Automation
“Here is the pipeline. It validates the data, calculates the metrics, creates rolling z-scores and flags exceptions such as revenue below baseline, CAC above baseline or margin deterioration. Each alert includes a human-readable reason. This is the type of workflow I would schedule daily and connect to Slack, Teams or email in production.”

## 2:20-3:15 — Scorecard and manager output
“The system also produces a scorecard and an automated weekly manager summary. Instead of asking a manager to inspect every dashboard tile, the workflow surfaces the exceptions first. The summary is AI-ready: an approved language model could turn the deterministic findings into role-specific narratives, while the underlying numbers remain controlled and reproducible.”

## 3:15-4:10 — Measured result
“In this demo the pipeline processes 1,440 market-team-day records automatically and produces the KPI layer, exception queue, scorecard and management summary in one run. Because this is synthetic data, I don’t claim production hours saved. In a real deployment I would establish a before-and-after baseline and value the automation using monthly hours saved, loaded labor cost, time-to-detection and any verified margin impact.”

## 4:10-4:45 — Why it matters
“What I like about this system is that it goes beyond a dashboard. It creates repeatable scorekeeping, exception detection and a management action loop. My next production extensions would be warehouse ingestion, scheduled execution, Slack or email alerts, lead-attribution metrics and controlled LLM summaries. Thank you.”
