# 🛡️ Sentinel Fortress: Advanced AI Fraud Detection System

**Sentinel Fortress** is a production-grade, high-velocity fraud detection system designed for financial institutions. It employs a **Split-Path Architecture** to handle high-throughput transactions with millisecond latency while responding to complex fraud patterns using Graph Intelligence and Agentic Active Defense.

## Key Features

*   **Fast Path (<200ms)**: Real-time blocking using **XGBoost** (trained on PaySim) and a **Circuit Breaker** resilience pattern.
*   **Deep Path (Async)**: Advanced graph mining using **GraphSAGE (GNN)** and **NetworkX** (Cycle Detection, PageRank) to detect money mule rings and loop anomalies.
*   **Zero-Trust Edge**: Behavioral biometrics SDK (`client_sdk/biometrics.js`) to detect bot-like interaction patterns.
*   **Active Defense**: Autonomous **Hunter Agents** capable of freezing assets and "immunizing" the network against detected threats.
*   **Cyberpunk SOC Dashboard**: A Next.js-based Visual Command Center for real-time threat monitoring and graph exploration.

## Architecture

The system is built on a specialized "Fast/Deep" lane architecture:

1.  **Fast Lane**: Synchronous. Input -> Circuit Breaker -> XGBoost Inference -> Decision (Allow/Block).
2.  **Deep Lane**: Asynchronous. Kafka Stream -> Graph Worker -> Neo4j/GNN -> Risk Score Update.
3.  **Command Center**: Real-time Dashboard visualizing live traffic and threats.

## Tech Stack

*   **AI/ML**: XGBoost, PyTorch Geometric (GraphSAGE), NetworkX, Pandas.
*   **Backend**: Python, FastAPI (implied structure), Kafka (Simulated).
*   **Frontend**: Next.js 14, React, Tailwind CSS, Recharts, Lucide Icons.
*   **Infrastructure**: Docker (planned), Redis (planned for caching).

## Quick Start

### Prerequisites
*   Python 3.10+
*   Node.js 18+

### 1. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Traffic Simulator (The Engine)
This script simulates live transactions, injects fraud patterns, and runs the Fast Path AI.
```bash
python3 simulate_traffic.py
```
*You should see transactions flowing with Risk Scores.*

### 3. Launch the Dashboard (The View)
Open a new terminal:
```bash
cd dashboard
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the Live SOC.

## Project Structure

*   `fast_lane/`: Real-time inference engine and circuit breaker.
*   `deep_lane/`: Graph analytics and GNN training scripts.
*   `ml_ops/`: Model training pipelines (XGBoost, GNN).
*   `dashboard/`: Next.js frontend application.
*   `agents/`: Active defense agents (Hunter, Decoy).
*   `client_sdk/`: JavaScript SDK for biometric telemetry.
*   `data_pipeline/`: ETL scripts for PaySim data.

## Testing

Run the regression suite to verify system integrity:
```bash
pytest tests/test_system.py
```

---
*Built for GILB Hackathon by Sentinel Team.*
