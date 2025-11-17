# Quick Start Guide - Get Running in 5 Minutes

This guide gets you from zero to running your first load test in 5 minutes.

## ⚡ 5-Minute Quick Start

### Step 1: Clone & Install (2 minutes)

```bash
# Clone the repository
git clone <your-repo-url>
cd locust-poc

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env - MINIMUM required:
# TARGET_HOST=https://your-staging-url.com
nano .env  # or use any editor
```

### Step 3: Run Your First Test (2 minutes)

**Option A: With Web UI (Recommended for First Time)**
```bash
locust -f tests/basic_test.py --host=https://your-staging-url.com
```

Then:
1. Open browser to `http://localhost:8089`
2. Enter: 10 users, spawn rate 2
3. Click "Start swarming"
4. Watch the magic happen! 🎉

**Option B: Quick Validation (Headless)**
```bash
python locust_helper.py quick tests/basic_test.py --host=https://your-staging-url.com
```

Results will be in `results/report.html`

## 🎯 What You Should See

### In the Terminal:
```
[2024-11-17 10:00:00] Starting Locust 2.20.0
[2024-11-17 10:00:00] Starting web interface at http://0.0.0.0:8089
```

### In the Browser (Web UI):
- **Type**: GET requests to various endpoints
- **Name**: Homepage, Product List, etc.
- **# Requests**: Increasing numbers
- **# Fails**: Should be 0 or very low
- **Median (ms)**: Response times (should be < 1000ms)
- **Current RPS**: Requests per second

### Good Signs ✅:
- Requests are going through (# Requests increasing)
- Low failure rate (< 1%)
- Response times are stable
- No error messages in console

### Warning Signs ⚠️:
- High failure rate (> 5%)
- Increasing response times over time
- Lots of red error messages
- Requests timing out

## 🔍 Understanding What's Happening

When you start a test with 10 users and spawn rate 2:

1. **Second 0**: Test starts, no users yet
2. **Second 1**: 2 users spawn, start making requests
3. **Second 2**: 2 more users spawn (total: 4)
4. **Second 3**: 2 more users spawn (total: 6)
5. **Second 4**: 2 more users spawn (total: 8)
6. **Second 5**: 2 more users spawn (total: 10) ✅ Target reached!
7. **Seconds 5+**: All 10 users continuously make requests until you stop

Each virtual user (VU):
- Makes a request
- Waits 1-3 seconds (the `wait_time` we configured)
- Makes another request
- Repeats until test ends

## 📊 Key Metrics Explained

### Response Time Percentiles
- **50th (median)**: Half of requests are faster than this
- **95th**: 95% of requests are faster than this
- **99th**: 99% of requests are faster than this

**Example**: If p95 = 500ms, that means 95% of your users experience response times under 500ms.

### Requests Per Second (RPS)
- How many requests your system handles per second
- Higher is better (shows system capacity)
- Should remain stable during test

### Failure Rate
- Percentage of failed requests
- Should be < 1% for healthy system
- Investigate if > 5%

## 🎓 Next Steps

### For Your POC:
1. ✅ Run this quick test to verify setup
2. 📝 Read `README.md` for full overview
3. 📚 Follow `POC_GUIDE.md` for complete POC execution
4. 🔧 Customize `tests/complete_example.py` for your app
5. 📊 Set up Datadog integration (see POC_GUIDE.md)

### Learning Path:
1. **Day 1**: Get basic test running (you're here!)
2. **Day 2**: Understand the test files, modify for your endpoints
3. **Day 3**: Set up Datadog integration, run longer tests
4. **Day 4**: Test GraphQL and Redis (if applicable)
5. **Day 5**: Run full 2-hour POC test, analyze results

## 💡 Tips for Success

### For Team Members New to Python:
- You don't need to be a Python expert
- Focus on understanding the structure (classes, tasks, weights)
- All examples are heavily commented
- Ask questions! Load testing is a team skill

### For Load Testing Beginners:
- Start small (10 users) and work your way up
- Always test in staging, never production (without approval)
- Ramp up slowly (spawn rate 2-5) to avoid overwhelming system
- Compare results to baseline metrics

### Common First-Time Issues:

**"Connection refused"**
- Check if TARGET_HOST is correct
- Verify staging environment is accessible
- Try accessing the URL in your browser first

**"401 Unauthorized"**
- Your app requires authentication
- Update the `authenticate()` method in the test file
- See examples in `tests/complete_example.py`

**"Tests are slow to start"**
- This is normal! Starting virtual users takes time
- Be patient during spawn phase
- Watch the "Users" counter increase

**"Results are in wrong directory"**
- Results go to `results/` folder by default
- Look for `report.html` and `stats_*.csv` files

## 🆘 Getting Help

### Check These First:
1. `README.md` - Project overview
2. `POC_GUIDE.md` - Detailed execution guide
3. Test file comments - Inline explanations
4. `python locust_helper.py --help` - Quick commands

### Internal Resources:
- DevOps team - Staging environment access
- Bailey - STG setup assistance
- Engineering team - API/endpoint details

### External Resources:
- [Locust Documentation](https://docs.locust.io)
- Locust sales contact from meeting
- Community Slack (if you get stuck)

## ✅ Success Checklist

You've successfully completed the quick start if you:
- [ ] Installed all dependencies without errors
- [ ] Configured `.env` with at least TARGET_HOST
- [ ] Ran a test and saw requests being made
- [ ] Viewed the web UI at localhost:8089
- [ ] Saw metrics (response times, RPS, etc.)
- [ ] Generated a report.html file
- [ ] Understand the basic metrics

**Congratulations!** 🎉 You're ready to proceed with the full POC.

---

**Time to complete**: 5 minutes ⏱️  
**Difficulty**: Beginner 🟢  
**Next**: Read `POC_GUIDE.md` for full POC execution
