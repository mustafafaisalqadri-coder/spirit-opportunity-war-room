import pandas as pd
import numpy as np

SPIRIT_ROUTES_RAW = [
    {"route": "FLL-ATL", "monthly_pax": 450000, "spirit_share": 0.31, "competitors": ["DL", "AA"]},
    {"route": "FLL-ORD", "monthly_pax": 380000, "spirit_share": 0.28, "competitors": ["AA", "UA"]},
    {"route": "FLL-LGA", "monthly_pax": 350000, "spirit_share": 0.24, "competitors": ["DL", "AA"]},
    {"route": "MCO-ORD", "monthly_pax": 320000, "spirit_share": 0.26, "competitors": ["AA", "UA"]},
    {"route": "MCO-DFW", "monthly_pax": 300000, "spirit_share": 0.22, "competitors": ["AA", "DL"]},
    {"route": "LAS-LAX", "monthly_pax": 280000, "spirit_share": 0.19, "competitors": ["WN", "AA"]},
    {"route": "FLL-BOS", "monthly_pax": 270000, "spirit_share": 0.23, "competitors": ["DL", "AA"]},
    {"route": "MCO-LGA", "monthly_pax": 260000, "spirit_share": 0.21, "competitors": ["DL", "AA"]},
    {"route": "DFW-LGA", "monthly_pax": 250000, "spirit_share": 0.18, "competitors": ["AA", "DL"]},
    {"route": "FLL-MSP", "monthly_pax": 240000, "spirit_share": 0.29, "competitors": ["DL"]},
    {"route": "MCO-BOS", "monthly_pax": 230000, "spirit_share": 0.25, "competitors": ["DL", "AA"]},
    {"route": "LAS-ORD", "monthly_pax": 220000, "spirit_share": 0.20, "competitors": ["UA", "AA"]},
    {"route": "FLL-MIA", "monthly_pax": 210000, "spirit_share": 0.35, "competitors": ["AA"]},
    {"route": "FLL-DFW", "monthly_pax": 200000, "spirit_share": 0.22, "competitors": ["AA", "DL"]},
    {"route": "MCO-MSP", "monthly_pax": 190000, "spirit_share": 0.27, "competitors": ["DL"]},
    {"route": "LAX-LAS", "monthly_pax": 180000, "spirit_share": 0.17, "competitors": ["WN", "AA"]},
    {"route": "FLL-DTW", "monthly_pax": 170000, "spirit_share": 0.31, "competitors": ["DL"]},
    {"route": "MCO-DTW", "monthly_pax": 160000, "spirit_share": 0.28, "competitors": ["DL"]},
    {"route": "FLL-CLE", "monthly_pax": 150000, "spirit_share": 0.33, "competitors": ["DL", "AA"]},
    {"route": "MCO-PHL", "monthly_pax": 140000, "spirit_share": 0.24, "competitors": ["AA"]},
    {"route": "LAS-DFW", "monthly_pax": 130000, "spirit_share": 0.19, "competitors": ["AA"]},
    {"route": "FLL-PIT", "monthly_pax": 120000, "spirit_share": 0.36, "competitors": ["DL", "AA"]},
    {"route": "MCO-CLE", "monthly_pax": 110000, "spirit_share": 0.29, "competitors": ["DL"]},
    {"route": "FLL-BWI", "monthly_pax": 100000, "spirit_share": 0.31, "competitors": ["WN", "AA"]},
    {"route": "MCO-BNA", "monthly_pax": 90000, "spirit_share": 0.27, "competitors": ["WN", "AA"]},
]

SPIRIT_QUARTERLY_RAW = [
    {"period": "Q1 2019", "on_time_pct": 74.2, "cancel_pct": 1.8, "avg_delay": 18.4, "market_share_pct": 4.8, "load_factor": 82.3},
    {"period": "Q2 2019", "on_time_pct": 71.8, "cancel_pct": 2.1, "avg_delay": 21.2, "market_share_pct": 4.9, "load_factor": 85.1},
    {"period": "Q3 2019", "on_time_pct": 68.4, "cancel_pct": 2.4, "avg_delay": 24.8, "market_share_pct": 5.0, "load_factor": 87.4},
    {"period": "Q4 2019", "on_time_pct": 73.1, "cancel_pct": 1.9, "avg_delay": 19.6, "market_share_pct": 4.9, "load_factor": 81.2},
    {"period": "Q1 2020", "on_time_pct": 71.4, "cancel_pct": 2.2, "avg_delay": 20.8, "market_share_pct": 4.7, "load_factor": 78.4},
    {"period": "Q2 2020", "on_time_pct": 84.2, "cancel_pct": 8.9, "avg_delay": 12.1, "market_share_pct": 3.1, "load_factor": 38.2},
    {"period": "Q3 2020", "on_time_pct": 79.8, "cancel_pct": 3.4, "avg_delay": 15.6, "market_share_pct": 3.8, "load_factor": 62.4},
    {"period": "Q4 2020", "on_time_pct": 77.2, "cancel_pct": 2.8, "avg_delay": 17.9, "market_share_pct": 4.0, "load_factor": 68.1},
    {"period": "Q1 2021", "on_time_pct": 73.8, "cancel_pct": 3.1, "avg_delay": 20.2, "market_share_pct": 4.2, "load_factor": 71.3},
    {"period": "Q2 2021", "on_time_pct": 65.4, "cancel_pct": 4.8, "avg_delay": 28.9, "market_share_pct": 4.6, "load_factor": 84.7},
    {"period": "Q3 2021", "on_time_pct": 54.2, "cancel_pct": 8.1, "avg_delay": 38.4, "market_share_pct": 4.8, "load_factor": 88.2},
    {"period": "Q4 2021", "on_time_pct": 62.8, "cancel_pct": 5.2, "avg_delay": 29.6, "market_share_pct": 4.7, "load_factor": 82.1},
    {"period": "Q1 2022", "on_time_pct": 64.1, "cancel_pct": 4.9, "avg_delay": 27.8, "market_share_pct": 4.9, "load_factor": 83.4},
    {"period": "Q2 2022", "on_time_pct": 61.8, "cancel_pct": 5.8, "avg_delay": 31.2, "market_share_pct": 5.1, "load_factor": 86.9},
    {"period": "Q3 2022", "on_time_pct": 58.4, "cancel_pct": 6.4, "avg_delay": 34.8, "market_share_pct": 5.0, "load_factor": 85.3},
    {"period": "Q4 2022", "on_time_pct": 63.2, "cancel_pct": 5.1, "avg_delay": 28.4, "market_share_pct": 4.8, "load_factor": 80.7},
    {"period": "Q1 2023", "on_time_pct": 64.8, "cancel_pct": 4.7, "avg_delay": 26.9, "market_share_pct": 4.6, "load_factor": 79.8},
    {"period": "Q2 2023", "on_time_pct": 62.1, "cancel_pct": 5.3, "avg_delay": 30.4, "market_share_pct": 4.4, "load_factor": 82.3},
    {"period": "Q3 2023", "on_time_pct": 59.8, "cancel_pct": 6.1, "avg_delay": 33.2, "market_share_pct": 4.1, "load_factor": 80.1},
    {"period": "Q4 2023", "on_time_pct": 61.4, "cancel_pct": 5.8, "avg_delay": 31.8, "market_share_pct": 3.8, "load_factor": 76.4},
    {"period": "Q1 2024", "on_time_pct": 58.9, "cancel_pct": 7.2, "avg_delay": 36.4, "market_share_pct": 3.4, "load_factor": 71.2},
    {"period": "Q2 2024", "on_time_pct": 55.4, "cancel_pct": 8.8, "avg_delay": 41.8, "market_share_pct": 2.9, "load_factor": 65.8},
    {"period": "Q3 2024", "on_time_pct": 51.2, "cancel_pct": 10.4, "avg_delay": 48.2, "market_share_pct": 2.4, "load_factor": 58.4},
    {"period": "Q4 2024", "on_time_pct": 48.8, "cancel_pct": 12.1, "avg_delay": 52.8, "market_share_pct": 1.8, "load_factor": 49.2},
]

DELTA_QUARTERLY = {
    "Q1 2019": 86.2, "Q2 2019": 84.1, "Q3 2019": 83.4, "Q4 2019": 87.8,
    "Q1 2020": 85.9, "Q2 2020": 89.1, "Q3 2020": 87.2, "Q4 2020": 86.4,
    "Q1 2021": 84.8, "Q2 2021": 82.1, "Q3 2021": 78.4, "Q4 2021": 83.2,
    "Q1 2022": 82.7, "Q2 2022": 79.8, "Q3 2022": 81.2, "Q4 2022": 84.9,
    "Q1 2023": 83.4, "Q2 2023": 82.1, "Q3 2023": 80.8, "Q4 2023": 85.2,
    "Q1 2024": 84.1, "Q2 2024": 83.7, "Q3 2024": 82.4, "Q4 2024": 86.1,
}

AA_QUARTERLY = {
    "Q1 2019": 79.8, "Q2 2019": 77.4, "Q3 2019": 76.1, "Q4 2019": 80.2,
    "Q1 2020": 78.9, "Q2 2020": 82.4, "Q3 2020": 79.8, "Q4 2020": 78.1,
    "Q1 2021": 76.4, "Q2 2021": 73.8, "Q3 2021": 69.2, "Q4 2021": 74.8,
    "Q1 2022": 75.1, "Q2 2022": 72.4, "Q3 2022": 74.8, "Q4 2022": 78.2,
    "Q1 2023": 76.8, "Q2 2023": 75.4, "Q3 2023": 74.1, "Q4 2023": 78.9,
    "Q1 2024": 77.2, "Q2 2024": 76.8, "Q3 2024": 75.4, "Q4 2024": 79.1,
}

HISTORICAL_EXITS = [
    {"airline": "AirTran", "routes": "Various (acquired by WN)", "year": 2014, "fare_increase_90d": 16, "context": "Southwest acquisition, gradual wind-down"},
    {"airline": "Frontier (partial)", "routes": "Various markets", "year": 2020, "fare_increase_90d": 14, "context": "COVID restructuring, route exits"},
    {"airline": "Virgin America", "routes": "Various (acquired by AA)", "year": 2018, "fare_increase_90d": 18, "context": "Alaska Air acquisition completion"},
    {"airline": "JetBlue (select)", "routes": "Transcon markets", "year": 2023, "fare_increase_90d": 12, "context": "Strategic route pruning post-NEA"},
    {"airline": "Southwest (exits)", "routes": "Select markets", "year": 2024, "fare_increase_90d": 19, "context": "Network optimization under activist pressure"},
]


def build_routes_df():
    rows = []
    for r in SPIRIT_ROUTES_RAW:
        comp = r["competitors"]
        n = len(comp)
        capturable = r["monthly_pax"] * r["spirit_share"] * 0.65
        annual_rev = capturable * 12 * 187
        urgency = r["spirit_share"] * 10 + (1 / n) * 5

        if n >= 2:
            comp_risk = "HIGH"
        elif n == 1 and comp[0] != "WN":
            comp_risk = "MEDIUM"
        else:
            comp_risk = "LOW"

        delta_only = (n == 1 and "DL" in comp)
        has_delta = "DL" in comp
        has_aa = "AA" in comp

        if delta_only:
            best_positioned = "Delta"
        elif "DL" in comp and "AA" not in comp:
            best_positioned = "Delta"
        elif "AA" in comp and "DL" not in comp:
            best_positioned = "American"
        elif "AA" in comp and "DL" in comp:
            best_positioned = "Delta / AA"
        else:
            best_positioned = "American"

        if n == 1:
            action = "Add frequency + hold price"
        elif n == 2:
            action = "Add frequency + compete on service"
        else:
            action = "Monitor — price war likely"

        rows.append({
            "Route": r["route"],
            "Monthly Pax Lost": int(r["monthly_pax"] * r["spirit_share"]),
            "Annual Rev Opportunity ($M)": round(annual_rev / 1_000_000, 1),
            "Urgency Score": round(urgency, 1),
            "Best Positioned": best_positioned,
            "Competitive Risk": comp_risk,
            "Recommended Action": action,
            "spirit_share": r["spirit_share"],
            "monthly_pax": r["monthly_pax"],
            "capturable_pax": round(capturable),
            "competitors": comp,
            "n_competitors": n,
            "has_delta": has_delta,
            "has_aa": has_aa,
        })
    return pd.DataFrame(rows)


def build_quarterly_df():
    df = pd.DataFrame(SPIRIT_QUARTERLY_RAW)
    df["delta_on_time"] = df["period"].map(DELTA_QUARTERLY)
    df["aa_on_time"] = df["period"].map(AA_QUARTERLY)
    df["delta_cancel"] = df["period"].apply(lambda p: round(
        2.1 - 0.3 * (list(DELTA_QUARTERLY.keys()).index(p) / 23), 2
    ) if p in DELTA_QUARTERLY else None)
    df["aa_cancel"] = df["period"].apply(lambda p: round(
        2.8 - 0.1 * (list(AA_QUARTERLY.keys()).index(p) / 23), 2
    ) if p in AA_QUARTERLY else None)
    return df


def get_summary_metrics(routes_df):
    total_rev = routes_df["Annual Rev Opportunity ($M)"].sum()
    delta_routes = routes_df[routes_df["has_delta"]]["Annual Rev Opportunity ($M)"].sum()
    aa_routes = routes_df[routes_df["has_aa"]]["Annual Rev Opportunity ($M)"].sum()
    return {
        "total_rev_b": round(total_rev / 1000, 2),
        "total_routes": len(routes_df),
        "delta_rev_b": round(delta_routes / 1000, 2),
        "aa_rev_b": round(aa_routes / 1000, 2),
        "delta_overlap": routes_df["has_delta"].sum(),
        "aa_overlap": routes_df["has_aa"].sum(),
    }


def get_historical_exits_df():
    return pd.DataFrame(HISTORICAL_EXITS)


ROUTES_DF = build_routes_df()
QUARTERLY_DF = build_quarterly_df()
SUMMARY = get_summary_metrics(ROUTES_DF)
EXITS_DF = get_historical_exits_df()
