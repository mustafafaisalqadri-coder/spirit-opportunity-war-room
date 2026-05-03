# Spirit Airlines Opportunity War Room
### A Strategic Response Dashboard for U.S. Airlines

**Live Dashboard:** Run locally with `streamlit run app.py`

---

## What This Answers

1. **Which routes should Delta and American prioritize?** — Ranked by revenue opportunity, urgency score, and competitive exposure.
2. **How much revenue is available?** — $2.3B annually across Spirit's top 25 routes, sized using BTS passenger data and ULCC market share.
3. **What happens to fares?** — Interactive projector modeling 12–22% fare increases based on Spirit's historical market share per route.
4. **What's the 90-day playbook?** — A full program management framework: decision tool, Gantt timeline, risk register, and KPI targets.

---

## Methodology

- **Passenger capture rate:** 65% of Spirit passengers assumed to switch to legacy carriers (vs. drive or cancel travel), based on ULCC substitution studies.
- **Average ticket revenue:** $187 (industry average for legacy carriers on short-haul routes).
- **Urgency score:** `spirit_share × 10 + (1 / n_competitors) × 5` — higher score means act faster.
- **Fare increase model:** `base_increase = spirit_share × 45%`, tapering over 180 days as competition normalizes.
- **Historical performance:** Quarterly BTS on-time and market share data 2019–2024.

---

## Key Findings

| Metric | Value |
|---|---|
| Total annual revenue opportunity | $2.3B |
| Routes with only Delta as competitor | 5 (highest urgency) |
| Routes with only AA as competitor | 3 |
| Highest single-route opportunity | FLL-ATL ($170M) |
| Highest urgency score | FLL-PIT (8.8) |
| Estimated Delta capturable share | $1.1B |
| Estimated AA capturable share | $890M |

---

## Built With

- **Streamlit** — dashboard framework
- **Plotly** — interactive charts (dual-axis, bubble, Gantt, bar)
- **Pandas** — data modeling and opportunity sizing
- **Claude API (Anthropic)** — AI strategy analyst on Page 6
- **BTS On-Time Performance data** — historical airline performance

---

## About This Project

Built as an aviation analytics portfolio project demonstrating:
- Strategic thinking applied to a real market event (Spirit Airlines shutdown, May 2, 2026)
- Revenue management and competitive analysis methodology
- Data engineering from public government sources (BTS)
- Program management frameworks (risk register, Gantt, KPI tracking)
- Full-stack data application development

**Author:** Mustafa Qadri  
**Date:** May 2, 2026  
**Contact:** mustafa.faisal.qadri@gmail.com
