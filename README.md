# Locust Load Testing with GitHub Actions

Automated load testing solution for Adcellerant's platform using Locust, integrated with GitHub Actions for CI/CD performance gates.

## 📋 Project Overview

This repository implements an automated load testing framework. The solution provides performance validation, deployment gates, and infrastructure stress testing for our React application and GraphQL API.

### Key Objectives

- ✅ Validate system performance before production deployments
- ✅ Prevent performance regressions through automated PR checks
- ✅ Establish baseline performance metrics for capacity planning

### Business Context

**Peak Traffic Analysis:** 1,286 unique users during 8-11am Wednesday windows with 54.5% active engagement  
**Testing Requirement:** Support 100+ concurrent virtual users with <1% failure rate

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                          │
│  ┌────────────────────┐      ┌──────────────────────────┐  │
│  │  load-test.yml     │      │ deployment-gate.yml      │  │
│  │  (Manual Trigger)  │      │ (Disabled for PRs)       │  │
│  └────────────────────┘      └──────────────────────────┘  │
│            │                            │                   │
│            └────────────┬───────────────┘                   │
│                         ▼                                   │
│              ┌────────────────────┐                         │
│              │  Locust Test Run   │                         │
│              │  - Execute tests   │                         │
│              │  - Check thresholds│                         │
│              │  - Generate reports│                         │
│              └────────────────────┘                         │
│                         │                                   │
│          ┌──────────────┼──────────────┐                   │
│          ▼              ▼               ▼                   │
│    ┌─────────┐   ┌──────────┐   ┌───────────┐             │
│    │ HTML    │   │   CSV    │   │ Threshold │             │
│    │ Report  │   │  Data    │   │  Check    │             │
│    └─────────┘   └──────────┘   └───────────┘             │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │  Staging Environment│
              │  stg.ui.marketing   │
              │  - GraphQL API      │
              │  - React App        │
              │  - Microservices    │
              └────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Access to staging environment (`stg.ui.marketing`)
- GitHub repository with Actions enabled
- FusionAuth credentials for authentication

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/willdarkins/Locust-Load-Testing-OKR.git
   cd Locust-Load-Testing-OKR
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   FUSION_AUTH_API_KEY=get from onepassword
   FUSION_AUTH_BASE_URI=get from fusionauth
   LOCUST_USERNAME=get from onepassword
   LOCUST_USER_PASSWORD=get from onepassword
   ```

5. **Run tests locally**
   ```bash
   # With web UI
   locust -f tests/line_items_table.py --host https://stg.ui.marketing

   # Headless mode
   locust -f tests/line_items_table.py \
     --headless \
     --users 50 \
     --spawn-rate 10 \
     --run-time 2m \
     --host https://stg.ui.marketing \
     --html report.html
   ```

---

## 🎮 Usage

### Manual Load Test

Trigger from GitHub Actions UI:

1. Go to **Actions** tab
2. Select **"Locust Load Test"** workflow
3. Click **"Run workflow"**
4. Configure parameters:
   - **Target URL:** Override default staging URL (optional)
   - **Users:** Number of concurrent virtual users (default: 50)
   - **Duration:** Test duration, e.g., `2m`, `5m` (default: 2m)
5. Click **"Run workflow"**


### Viewing Results

**From GitHub Actions:**
1. Navigate to the completed workflow run
2. Scroll to the bottom → **Artifacts** section
3. Download **"locust-results"** ZIP file
4. Extract and open `report.html` in your browser

**Local Results:**
- HTML Report: `report.html` (open in browser)
- CSV Statistics: `results_stats.csv`
- Failure Log: `results_failures.csv`