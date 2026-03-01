Mule Detection Framework
An Open-Source Behavioral Transaction Analysis System
The Mule Detection Framework is an open-source system designed to study and detect behavioral patterns associated with mule accounts and layered money transfer networks in financial transactions. Unlike simple anomaly detection, it models the structural behavior of fraudulent transaction chains and evaluates accounts using transparent behavioral risk indicators. This framework supports research, experimentation, and educational exploration of transaction-level fraud dynamics.

Core Problem
Modern digital payment systems enable rapid fund transfers, which fraud networks exploit by routing stolen funds through intermediary mule accounts. Mule accounts typically exhibit:
Funds received from multiple sources
Quick outbound transfers after receipt
High outgoing-to-incoming ratios
Brief existence with elevated transaction velocity
While enterprise anti-money laundering (AML) systems exist, transparent open-source frameworks for modeling mule behavior at a structural level are scarce. This project addresses that gap.

System Overview
The framework:
Generates synthetic, realistic transaction datasets
Models transactions as directed graphs
Extracts behavioral features per account
Computes transparent risk scores
Flags accounts with mule-like patterns
It serves as a simulation-based research tool, not a production banking system.

Architecture
1. Transaction Simulation Layer
Generates synthetic data mimicking:
Normal user behavior
Configurable mule chains and multi-hop transfers
Variable transaction frequency
Mixed legitimate and suspicious patterns
Each transaction includes sender ID, receiver ID, timestamp, amount, and account age.
2. Behavioral Feature Extraction
Calculates per-account indicators:
Account age
Transaction frequency (velocity)
Incoming vs. outgoing ratio
Unique sender count
Average forwarding delay
Rapid transfer clustering
3. Risk Scoring Engine
Assigns a Mule Risk Score (0–100) via rule-based logic, with contributions from:
New accounts with high activity
Rapid outgoing transfers post-receipt
Transaction bursts in short windows
Multi-hop forwarding
Future iterations will incorporate machine learning classifiers.
4. Graph-Based Network Analysis
Represents transactions as directed graphs (nodes: accounts; edges: transfers) to identify:
Central relay nodes
Layered transfer chains
High-connectivity suspicious clusters

Evaluation Strategy
Assesses:
Detection accuracy in synthetic datasets
False positive rates
Precision/recall balance
Chain detection consistency
Risk score interpretability
Emphasis is on clarity, transparency, and reproducibility.

Intended Use Cases
Academic research in fraud modeling
Educational demonstrations of mule detection
Graph-based financial analysis experiments
Foundation for ML-based fraud research

What This Project Is Not
A replacement for banking AML systems
Connected to real financial institutions
Using real customer data
Making legal accusations
It is strictly a controlled simulation and analysis framework.

Technical Stack
Python
Pandas
NetworkX
Scikit-learn (planned)
FastAPI (planned)
Synthetic data generator

Why This Project Matters
Fraud detection often targets isolated transactions, overlooking network structures. This framework models transaction systems structurally, revealing hidden laundering patterns and shifting focus from "Is this transaction unusual?" to "How does this account behave in the network?"

Impact Statement
The Mule Detection Framework offers a transparent, modular foundation for studying behavioral fraud in digital transactions, integrating simulation, behavioral analytics, and graph theory to illuminate mule account operations.
