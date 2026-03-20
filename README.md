# Mule Detection Framework

> Open-source behavioral fraud detection for mule account identification in financial transaction networks.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this?

The Mule Detection Framework detects mule accounts in financial transaction networks through **explainable behavioral scoring** and **graph-based chain detection** — no black-box models, no real banking data required.

```
Victim → Mule Account → Layered Accounts → Withdrawal
```

We detect the mule accounts in the middle using synthetic data, transparent rules, and network analysis.

---

## Why it matters

Traditional fraud systems flag isolated unusual transactions — missing the **network structures** that enable large-scale laundering. This framework shifts the question from:

> *"Is this transaction unusual?"* → *"Is this account behaving like a mule across the network?"*

---

## Key Results

| Metric | Value |
|--------|-------|
| Transactions analysed | 3,000 |
| Total flow tracked | ₹7.47 Crore |
| Accounts scored | 101 |
| Mule accounts flagged | 63 |
| Avg risk score (flagged) | 59.1 / 100 |
| Max risk score | 85 / 100 |
| Suspicious chains detected | 164 |
| Top chain flow | ₹11.5 Lakh |

---

## Architecture

| Layer | Module | What it does |
|-------|--------|-------------|
| Simulation | `data_generator.py`, `csv_writer.py` | Generates 3,000 realistic transactions with mule patterns |
| Features | `feature_engineering.py` | Per-account metrics — velocity, age, amount ratios |
| Risk Engine | `risk_engine/` | Rule-based scoring (0–100), flags accounts above threshold |
| Graph Analysis | `graph_analysis/` | Detects fan-out and shared-receiver laundering chains |
| API | `api/` | FastAPI — exposes all results as JSON endpoints |

All thresholds and rules configurable via `risk_engine/config.json`.

---

## Risk Scoring Rules

| Rule | Trigger | Score |
|------|---------|-------|
| New account | Age < 30 days | +20 |
| High tx rate | > 10 tx/hr | +25 |
| Quick forward | Sends < 5 min after receiving | +30 |
| Many senders | > 5 unique incoming senders | +15 |
| High value ratio | > 50% txns above ₹30,000 | +10 |
| High fraud ratio | > 10% txns flagged | +30 |

Accounts scoring **> 35** are flagged as suspected mules. Every flag includes a human-readable reason.

---

## Project Structure

```
Mule-detection-framework/
├── data_generator.py        # Synthetic transaction generator
├── csv_writer.py            # CSV export
├── feature_engineering.py   # Feature extraction
├── model_building.py        # ML model (92% accuracy)
├── transactions.csv         # Raw generated dataset
├── risk_engine/
│   ├── config.json          # All thresholds and scores
│   ├── rules.py             # Rule definitions
│   └── scoring.py           # Main scoring engine
├── graph_analysis/
│   └── graph.py             # Network graph + chain detection
├── api/
│   └── main.py              # FastAPI application
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/Vaishnavi-poojary/Mule-detection-framework.git
cd Mule-detection-framework
pip install -r requirements.txt
```

```bash
python csv_writer.py              # Step 1 — Generate data
python feature_engineering.py    # Step 2 — Extract features
python -m risk_engine.scoring    # Step 3 — Flag mule accounts
python -m graph_analysis.graph   # Step 4 — Detect chains
uvicorn api.main:app --reload     # Step 5 — Start API
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/detect` | Run full detection pipeline |
| `GET` | `/results` | Flagged mule accounts |
| `GET` | `/chains` | Detected laundering chains |
| `GET` | `/graph` | Transaction network image |
| `GET` | `/summary` | Full stats dashboard |

Sample `/summary` response:
```json
{
  "transactions": { "total": 3000, "total_amount": 74705796.59 },
  "risk_engine": { "flagged_mule_accounts": 63, "avg_risk_score": 59.1 },
  "graph_analysis": { "chains_detected": 164, "top_flow": 1150819.01 }
}
```

---

## Testing

After running the full pipeline, verify:

```bash
# These files should exist and be non-empty
flagged_accounts.csv          # 63 flagged accounts
all_accounts.csv              # 101 total accounts
graph_analysis/chain_report.csv       # 164 chains
graph_analysis/transaction_graph.png  # Network image
```

All 5 API endpoints should return `200 OK` at `http://127.0.0.1:8000/docs`.

---

## Use Cases

- Fraud research and simulation
- Educational graph analysis demos
- Hackathon and fintech baseline projects
- Foundation for ML-based AML research

---

## Future Work

- ML anomaly detection replacing rule-based scoring
- Real-time streaming with Kafka
- Interactive web dashboard
- PageRank and betweenness centrality metrics
- Crypto wallet risk mapping

---

## Disclaimer

Research tool using synthetic data only. Not connected to any real financial institution or customer data.

---

## License

MIT — see [LICENSE](LICENSE)
