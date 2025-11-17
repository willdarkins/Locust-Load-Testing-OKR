# Locust Load Testing POC

This repository contains a Proof of Concept (POC) for load testing our React application using Locust Cloud.

## 📋 Project Overview

**Purpose**: Evaluate Locust Cloud for load testing our React application with ~2 load tests per month.

**Meeting Notes**: See internal documentation for detailed requirements and Q&A from the Locust sales meeting (Nov 17, 2025).

## 🎯 POC Goals

1. **Validate Free Tier Viability**: Test if 200 VU hours/month meets our needs
2. **Integration Testing**: Verify Datadog, GitHub Actions, and Slack integrations
3. **Team Learning**: Build Python/Locust expertise with minimal current experience
4. **Technical Validation**: Confirm support for GraphQL and Redis Pub/Sub testing

## 📊 Key Metrics from Sales Meeting

- **Current Usage**: ~2 load tests per month
- **Peak Load**: ~100 concurrent virtual users (VUs)
- **Free Plan**: 200 VU hours/month, max 100 concurrent VUs
- **Calculation**: 2-hour test × 50 VUs = 100 VU hours per test
- **Data Retention**: 180 days (same for free and paid)

## 🏗️ Project Structure

```
locust-poc/
├── tests/              # Locust test files (locustfiles)
├── scenarios/          # Reusable test scenarios
├── utils/              # Helper functions and utilities
├── config/             # Configuration files
├── results/            # Test results and reports (gitignored)
├── .github/workflows/  # GitHub Actions for CI/CD integration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Access to staging environment

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd locust-poc
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

### Running Tests Locally

```bash
# Run with Locust web UI (recommended for development)
locust -f tests/basic_test.py --host=https://your-staging-url.com

# Run headless (for CI/CD)
locust -f tests/basic_test.py --host=https://your-staging-url.com \
  --users 10 --spawn-rate 2 --run-time 1m --headless
```

## 📚 Understanding Locust Concepts

### Virtual Users (VUs)
- **What**: Simulated users that execute your test scenarios
- **Example**: 50 VUs means 50 concurrent simulated users hitting your app

### Virtual User Hours (VU Hours)
- **Calculation**: Number of VUs × Test duration in hours
- **Example**: 100 VUs running for 2 hours = 200 VU hours
- **Why it matters**: This is how Locust Cloud bills usage

### Spawn Rate
- **What**: How quickly VUs are added to reach target user count
- **Example**: Spawn rate of 5/sec means adding 5 new users every second
- **Best Practice**: Gradual ramp-up prevents overwhelming the system

### Test Scenarios
- **User Tasks**: Individual actions a user performs (login, browse, checkout)
- **Task Weighting**: Frequency of different actions (e.g., browsing is 3x more common than checkout)
- **Wait Times**: Realistic pauses between actions (simulating user think time)

## 🔧 Integration Points

### Datadog Integration
- **Purpose**: Correlate load test metrics with application performance
- **Benefit**: See which database queries slow down, API error rates, memory spikes
- **Status**: Pending setup and testing

### GitHub Actions Integration
- **Purpose**: Automated load testing in CI/CD pipeline
- **Use Case**: Gate deployments if performance degrades >20%
- **Status**: Workflow template created

### Slack Integration
- **Purpose**: Real-time notifications of test results and issues
- **Status**: Pending testing

### Jira Integration
- **Purpose**: Automated ticket creation for performance threshold breaches
- **Status**: To be implemented

## 📈 Free Plan Capacity Analysis

### Scenario: 2 Tests per Month

**Test Profile**:
- Duration: 2 hours per test
- Concurrent VUs: 50
- VU Hours per test: 50 × 2 = 100 VU hours

**Monthly Usage**:
- 2 tests × 100 VU hours = 200 VU hours ✅ (exactly at free tier limit)

**Recommendation**: Start with free tier but monitor closely. Any additional tests or longer duration will require Premium plan ($399/month for 5,000 VU hours).

## 🎓 Learning Resources

### For Team Members New to Python
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Learn Python in Y Minutes](https://learnxinyminutes.com/docs/python/)

### Locust Documentation
- [Locust Official Docs](https://docs.locust.io/)
- [Writing a Locustfile](https://docs.locust.io/en/stable/writing-a-locustfile.html)

### Load Testing Best Practices
- Start small: Begin with 10-20 VUs to verify test accuracy
- Ramp up gradually: Use realistic spawn rates
- Monitor system resources: Watch CPU, memory, database during tests
- Test in staging: Never run load tests against production without approval

## 🔍 Next Steps for POC

- [ ] Set up Locust Cloud account (free tier)
- [ ] Create basic test scenario for our React app
- [ ] Test GraphQL and Redis Pub/Sub protocols
- [ ] Configure Datadog integration
- [ ] Set up GitHub Actions workflow
- [ ] Test Slack notifications
- [ ] Run initial 2-hour test with 50 VUs
- [ ] Document findings and recommendations
- [ ] Present results to stakeholders

## 📝 Notes from Sales Meeting

- **Start Strategy**: Begin with free version, assess capacity needs
- **Testing Location**: US-only, using AWS cloud
- **Seat Licensing**: Unlimited users can access the SaaS platform
- **Support**: Premium includes professional support via email
- **Preference Note**: Team prefers Google Cloud, but Locust uses AWS

## 🤝 Contributing

Since this is a POC, please document your learnings and questions as you work through the setup. This will help the entire team understand Locust better.

## 📞 Contact

- **Locust Sales Rep**: [Contact from meeting]
- **Internal Champion**: Bailey (for STG environment setup)

## 📄 License

Internal use only - [Your Company Name]
