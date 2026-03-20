"""
api/main.py
Member 4 – FastAPI Backend

Endpoints:
    GET  /              - Health check
    POST /detect        - Run full detection pipeline (scoring + graph)
    GET  /results       - Return flagged accounts as JSON
    GET  /chains        - Return mule chains as JSON
    GET  /graph         - Serve transaction network image
    GET  /summary       - Return overall stats

Run from project root:
    uvicorn api.main:app --reload
Then open: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import subprocess
import os
import sys

app = FastAPI(
    title="Mule Account Detection API",
    description="Open-source fraud risk engine — detects mule accounts and transaction laundering patterns.",
    version="1.0.0"
)

# Allow all origins (useful for frontend demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── File paths ─────────────────────────────────────────────────────────────────
TRANSACTIONS_CSV    = "transactions.csv"
FLAGGED_CSV         = "flagged_accounts.csv"
ALL_ACCOUNTS_CSV    = "all_accounts.csv"
CHAIN_REPORT_CSV    = "graph_analysis/chain_report.csv"
GRAPH_IMAGE         = "graph_analysis/transaction_graph.png"


# ── Helper ─────────────────────────────────────────────────────────────────────
def file_exists(path: str):
    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail=f"File '{path}' not found. Run /detect first."
        )


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check():
    """Check if the API is running."""
    return {
        "status": "running",
        "project": "Mule Account Detection Framework",
        "version": "1.0.0",
        "endpoints": ["/detect", "/results", "/chains", "/graph", "/summary", "/docs"]
    }


@app.post("/detect", tags=["Detection"])
def run_detection():
    """
    Run the full detection pipeline:
    1. Risk Scoring Engine (Member 2)
    2. Graph Analysis (Member 3)
    Generates flagged_accounts.csv, chain_report.csv, transaction_graph.png
    """
    results = {}

    # Step 1 — Run risk scoring engine
    try:
        scoring = subprocess.run(
            [sys.executable, "-m", "risk_engine.scoring"],
            capture_output=True, text=True
        )
        results["risk_engine"] = {
            "status": "success" if scoring.returncode == 0 else "error",
            "output": scoring.stdout.strip().split("\n")[-3:]  # last 3 lines
        }
    except Exception as e:
        results["risk_engine"] = {"status": "error", "output": str(e)}

    # Step 2 — Run graph analysis
    try:
        graph = subprocess.run(
            [sys.executable, "-m", "graph_analysis.graph"],
            capture_output=True, text=True
        )
        results["graph_analysis"] = {
            "status": "success" if graph.returncode == 0 else "error",
            "output": graph.stdout.strip().split("\n")[-3:]
        }
    except Exception as e:
        results["graph_analysis"] = {"status": "error", "output": str(e)}

    # Step 3 — Quick stats
    try:
        flagged_df = pd.read_csv(FLAGGED_CSV)
        chains_df  = pd.read_csv(CHAIN_REPORT_CSV)
        results["summary"] = {
            "flagged_accounts": len(flagged_df),
            "chains_detected":  len(chains_df),
        }
    except Exception:
        results["summary"] = "Run completed — check /results and /chains"

    return JSONResponse(content=results)


@app.get("/results", tags=["Detection"])
def get_flagged_accounts(limit: int = 50):
    """
    Return list of flagged mule accounts with risk scores and reasons.
    Use ?limit=100 to get more results.
    """
    file_exists(FLAGGED_CSV)
    df = pd.read_csv(FLAGGED_CSV)
    df = df.sort_values("risk_score", ascending=False).head(limit)
    return {
        "total_flagged": len(pd.read_csv(FLAGGED_CSV)),
        "showing": len(df),
        "accounts": df.to_dict(orient="records")
    }


@app.get("/chains", tags=["Detection"])
def get_chains(limit: int = 50):
    """
    Return detected mule chains (money laundering patterns).
    Use ?limit=100 to get more results.
    """
    file_exists(CHAIN_REPORT_CSV)
    df = pd.read_csv(CHAIN_REPORT_CSV)
    df = df.sort_values("total_flow", ascending=False).head(limit)
    return {
        "total_chains": len(pd.read_csv(CHAIN_REPORT_CSV)),
        "showing": len(df),
        "chains": df.to_dict(orient="records")
    }


@app.get("/graph", tags=["Visualization"])
def get_graph():
    """
    Returns the transaction network graph image.
    Red nodes = mule accounts, Green nodes = normal accounts.
    """
    file_exists(GRAPH_IMAGE)
    return FileResponse(
        GRAPH_IMAGE,
        media_type="image/png",
        filename="transaction_graph.png"
    )


@app.get("/summary", tags=["Detection"])
def get_summary():
    """
    Returns overall stats about the detection run.
    """
    summary = {}

    # Transactions
    try:
        tx_df = pd.read_csv(TRANSACTIONS_CSV)
        summary["transactions"] = {
            "total": len(tx_df),
            "fraud_flagged": int(tx_df["fraud_flag"].sum()),
            "unique_senders": int(tx_df["sender"].nunique()),
            "unique_receivers": int(tx_df["receiver"].nunique()),
            "total_amount": round(float(tx_df["amount"].sum()), 2)
        }
    except Exception:
        summary["transactions"] = "transactions.csv not found"

    # Flagged accounts
    try:
        flagged_df = pd.read_csv(FLAGGED_CSV)
        summary["risk_engine"] = {
            "total_accounts_analysed": len(pd.read_csv(ALL_ACCOUNTS_CSV)),
            "flagged_mule_accounts": len(flagged_df),
            "avg_risk_score": round(float(flagged_df["risk_score"].mean()), 1),
            "max_risk_score": int(flagged_df["risk_score"].max()),
        }
    except Exception:
        summary["risk_engine"] = "Run /detect first"

    # Chains
    try:
        chains_df = pd.read_csv(CHAIN_REPORT_CSV)
        summary["graph_analysis"] = {
            "chains_detected": len(chains_df),
            "top_flow": round(float(chains_df["total_flow"].max()), 2),
            "patterns": chains_df["pattern"].value_counts().to_dict()
            if "pattern" in chains_df.columns else {}
        }
    except Exception:
        summary["graph_analysis"] = "Run /detect first"

    return summary
