# Locust Command Cheat Sheet

Quick reference for common Locust commands and operations.

## 🚀 Basic Commands

### Start with Web UI
```bash
locust -f tests/basic_test.py --host=https://staging.myapp.com
# Opens UI at http://localhost:8089
```

### Run Headless (No UI)
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 50 \
  --spawn-rate 5 \
  --run-time 2h \
  --headless
```

### Quick Test (1 minute, 10 users)
```bash
python locust_helper.py quick tests/basic_test.py
```

## 📊 Output Options

### Generate HTML Report
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 50 \
  --spawn-rate 5 \
  --run-time 1h \
  --headless \
  --html=results/report.html
```

### Export CSV Data
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 50 \
  --spawn-rate 5 \
  --run-time 1h \
  --headless \
  --csv=results/stats
```
Creates: `results/stats_stats.csv`, `results/stats_failures.csv`, `results/stats_exceptions.csv`

### Both HTML and CSV
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 50 \
  --spawn-rate 5 \
  --run-time 1h \
  --headless \
  --html=results/report.html \
  --csv=results/stats
```

## ⚙️ Common Configurations

### Test Sizes

**Small Test (Quick Validation)**
```bash
--users 10 --spawn-rate 2 --run-time 2m
```

**Medium Test (Standard)**
```bash
--users 50 --spawn-rate 5 --run-time 30m
```

**Large Test (Full POC)**
```bash
--users 50 --spawn-rate 5 --run-time 2h
```

**Stress Test**
```bash
--users 100 --spawn-rate 10 --run-time 1h
```

### Duration Formats
- `30s` = 30 seconds
- `5m` = 5 minutes
- `2h` = 2 hours
- `1h30m` = 1.5 hours

## 🧪 Different Test Files

### Basic HTTP Test
```bash
locust -f tests/basic_test.py --host=https://staging.myapp.com
```

### GraphQL Test
```bash
locust -f tests/graphql_test.py --host=https://staging.myapp.com
```

### Redis Pub/Sub Test
```bash
locust -f tests/redis_test.py --host=redis://staging-redis.myapp.com:6379
```

### Complete Example (All Integrations)
```bash
locust -f tests/complete_example.py --host=https://staging.myapp.com
```

## 🛠️ Helper Script Commands

### Check Environment
```bash
python locust_helper.py check
```

### List Available Tests
```bash
python locust_helper.py list
```

### Validate Test File
```bash
python locust_helper.py validate tests/basic_test.py
```

### Calculate VU Hours
```bash
python locust_helper.py calc --users 50 --duration 2h
# Output: 100 VU hours
```

### Run with UI
```bash
python locust_helper.py ui tests/basic_test.py --host https://staging.myapp.com
```

### Run Quick Test
```bash
python locust_helper.py quick tests/basic_test.py
```

### Run Custom Test
```bash
python locust_helper.py run tests/basic_test.py \
  --users 50 \
  --duration 2h \
  --spawn-rate 5 \
  --host https://staging.myapp.com
```

## 📈 Real-Time Monitoring

### During Test (Web UI)
1. Open `http://localhost:8089`
2. View:
   - Current RPS (requests/second)
   - Response times (median, p95, p99)
   - Failure rate
   - Charts of performance over time

### Stop Test
- **Web UI**: Click "Stop" button
- **Command Line**: Press `Ctrl+C`
- **Headless**: Automatically stops after `--run-time`

### View Results
```bash
# Open HTML report
open results/report.html  # macOS
xdg-open results/report.html  # Linux
start results/report.html  # Windows

# View CSV in spreadsheet
open results/stats_stats.csv
```

## 🔍 Debugging Commands

### Verbose Output
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --loglevel DEBUG
```

### Test Single User (No Load)
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 1 \
  --spawn-rate 1 \
  --run-time 1m \
  --headless
```

### Check for Python Errors
```bash
python -m py_compile tests/basic_test.py
```

## 🌐 Network & Port Options

### Custom Web UI Port
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --web-port 8090
# Opens UI at http://localhost:8090
```

### Bind to Specific Interface
```bash
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --web-host 0.0.0.0
# Accessible from other machines
```

## 🎯 Advanced Options

### Specific User Class
```bash
# If you have multiple user classes in one file
locust -f tests/complete_example.py \
  --host=https://staging.myapp.com \
  BrowserUser
```

### Custom Tags
```bash
# Run only tasks with specific tags
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --tags critical
```

### Exclude Tags
```bash
# Skip tasks with specific tags
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --exclude-tags slow
```

### Step Load
```bash
# Gradually increase load
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 100 \
  --spawn-rate 10 \
  --step-load \
  --step-users 10 \
  --step-time 30s
# Adds 10 users every 30s until reaching 100
```

## 📦 Environment Variables

### Load from .env File
```bash
# Set in .env file
TARGET_HOST=https://staging.myapp.com
DATADOG_API_KEY=your_key

# Then run without --host
locust -f tests/basic_test.py
```

### Override on Command Line
```bash
TARGET_HOST=https://production.myapp.com \
locust -f tests/basic_test.py
```

## 🔗 Useful Combinations

### Full POC Test with All Outputs
```bash
locust -f tests/complete_example.py \
  --host=https://staging.myapp.com \
  --users 50 \
  --spawn-rate 5 \
  --run-time 2h \
  --headless \
  --html=results/poc_$(date +%Y%m%d_%H%M%S).html \
  --csv=results/poc_$(date +%Y%m%d_%H%M%S)
```

### Quick Comparison Test
```bash
# Before deployment
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 50 --run-time 5m --headless \
  --csv=results/before

# After deployment
locust -f tests/basic_test.py \
  --host=https://staging.myapp.com \
  --users 50 --run-time 5m --headless \
  --csv=results/after

# Compare results
python -c "import pandas as pd; \
  before = pd.read_csv('results/before_stats.csv'); \
  after = pd.read_csv('results/after_stats.csv'); \
  print('Response time change:', \
    after['Average Response Time'].mean() - before['Average Response Time'].mean())"
```

## 🆘 Troubleshooting

### Clear Previous Results
```bash
rm -rf results/*
```

### Kill Stuck Locust Process
```bash
# Find process
ps aux | grep locust

# Kill it
kill -9 <PID>
```

### Test Connection Before Load Test
```bash
curl -I https://staging.myapp.com
```

### Verify Python Version
```bash
python --version
# Should be 3.8 or higher
```

## 📝 Tips

### Save Command for Reuse
```bash
# Create alias in ~/.bashrc or ~/.zshrc
alias locust-poc='locust -f tests/complete_example.py --host=https://staging.myapp.com'

# Use it
locust-poc --users 50 --run-time 1h --headless
```

### Quick Stats Review
```bash
# After headless run
tail -20 results/stats_stats.csv | column -t -s,
```

### Watch Log File
```bash
# In one terminal, run test
locust -f tests/basic_test.py --host=https://staging.myapp.com --headless 2>&1 | tee test.log

# In another terminal, watch
tail -f test.log
```

## 🎓 Learning Resources

### Official Docs
- Docs: https://docs.locust.io
- Examples: https://docs.locust.io/en/stable/quickstart.html
- API: https://docs.locust.io/en/stable/api.html

### This Project
- Overview: `README.md`
- Full Guide: `POC_GUIDE.md`
- Quick Start: `QUICKSTART.md`
- Examples: `tests/*.py`

---

**💡 Pro Tip**: Keep this cheat sheet handy! Most commands follow the same pattern:
```
locust -f <test_file> --host=<url> [options]
```
