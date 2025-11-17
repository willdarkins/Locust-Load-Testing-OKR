# Locust POC Execution Guide

This guide walks you through executing the Proof of Concept for Locust Cloud load testing.

## 📅 POC Timeline & Milestones

### Week 1: Setup & Basic Testing
- [ ] Set up Locust Cloud account (free tier)
- [ ] Configure staging environment access
- [ ] Run first basic HTTP test
- [ ] Validate metrics collection

### Week 2: Integration Testing
- [ ] Set up Datadog integration
- [ ] Configure GitHub Actions workflow
- [ ] Test Slack notifications
- [ ] GraphQL endpoint testing

### Week 3: Advanced Testing & Documentation
- [ ] Redis Pub/Sub testing
- [ ] Run full 2-hour test with 50 VUs
- [ ] Document findings and edge cases
- [ ] Prepare presentation for stakeholders

## 🚀 Step-by-Step Execution

### Step 1: Environment Setup

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd locust-poc
```

2. **Create and activate virtual environment**:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your actual values
nano .env  # or use your preferred editor
```

### Step 2: Create Locust Cloud Account

1. Go to [Locust Cloud](https://cloud.locust.io) (or the provided URL from sales)
2. Sign up using company email
3. Choose **Free Plan** (200 VU hours/month)
4. Note your API token (you'll need it later)

**What to expect**:
- Account creation is instant
- No credit card required for free tier
- Access to web dashboard immediately

### Step 3: Run Your First Test Locally

Before using Locust Cloud, test locally to verify your setup:

```bash
# Start Locust with web UI
locust -f tests/basic_test.py --host=https://your-staging-url.com
```

**What happens**:
1. Locust starts a web server on `http://localhost:8089`
2. Open your browser and go to that URL
3. You'll see the Locust UI

**In the Locust UI**:
1. Enter number of users (start with 10)
2. Enter spawn rate (start with 2)
3. Click "Start swarming"
4. Watch real-time metrics appear

**Understanding the UI**:
- **Statistics**: Shows requests per second, response times, failures
- **Charts**: Real-time graphs of performance
- **Failures**: Any errors encountered during testing
- **Download Data**: Export results as CSV

**First Test Checklist**:
- [ ] Can reach your staging environment
- [ ] Requests are successful (no authentication errors)
- [ ] Response times are reasonable
- [ ] No unexpected failures

### Step 4: Deploy to Locust Cloud

Once local testing works, deploy to Locust Cloud:

1. **Create a project in Locust Cloud**:
   - Name: "MyApp Load Test POC"
   - Environment: Staging
   - Region: US (based on meeting notes)

2. **Upload your locustfile**:
   - Use `tests/basic_test.py` initially
   - Follow Locust Cloud's upload wizard

3. **Configure test parameters**:
   - Users: 50
   - Duration: 2 hours
   - Spawn rate: 5 users/second

4. **Start your first cloud test**:
   - Monitor from Locust Cloud dashboard
   - Should see real-time metrics

**VU Hour Calculation**:
- 50 users × 2 hours = 100 VU hours
- First test uses half your monthly free allocation (200 VU hours)
- Second test will use remaining 100 VU hours

### Step 5: Set Up Datadog Integration

**Why**: See load test metrics alongside application performance data

1. **Get Datadog credentials**:
   - Log into Datadog
   - Go to Organization Settings > API Keys
   - Copy your API key
   - Go to Application Keys > New Key
   - Copy your App key

2. **Add to .env file**:
```bash
DATADOG_API_KEY=your_api_key_here
DATADOG_APP_KEY=your_app_key_here
DATADOG_SITE=datadoghq.com
```

3. **Test locally first**:
```python
# In your locustfile, add:
from locust import events
from utils.datadog_reporter import setup_datadog_reporting

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    setup_datadog_reporting(environment)
```

4. **Run a test**:
```bash
locust -f tests/basic_test.py --host=https://your-staging-url.com \
  --users 10 --spawn-rate 2 --run-time 2m --headless
```

5. **Verify in Datadog**:
   - Go to Metrics Explorer
   - Search for "locust."
   - Should see: `locust.request.response_time`, `locust.users.active`, etc.

**What to look for in Datadog during tests**:
- Correlation between load and database query time
- Memory usage patterns
- Error rate changes
- API endpoint performance

### Step 6: GraphQL Testing

Your application uses GraphQL, so this is critical:

1. **Identify your GraphQL endpoint**:
   - Typically: `https://your-app.com/graphql`
   - Confirm with your backend team

2. **List the queries to test**:
   - User profile queries
   - Product list queries
   - Search queries
   - Any frequently-used mutations

3. **Update `tests/graphql_test.py`**:
   - Replace example queries with your actual queries
   - Use your real schema fields
   - Add authentication if needed

4. **Run GraphQL test**:
```bash
locust -f tests/graphql_test.py --host=https://your-staging-url.com \
  --users 20 --spawn-rate 2 --run-time 5m --headless
```

**GraphQL-specific things to monitor**:
- Query complexity vs response time
- N+1 query problems (watch Datadog database metrics)
- Error responses (GraphQL can return 200 with errors!)

### Step 7: Redis Pub/Sub Testing

If your app uses Redis for real-time features:

1. **Get Redis connection details**:
   - Ask DevOps/Bailey for staging Redis endpoint
   - Get credentials if authentication is required

2. **Update .env**:
```bash
REDIS_HOST=staging-redis.yourapp.com
REDIS_PORT=6379
REDIS_PASSWORD=if_needed
```

3. **Test connection first**:
```bash
python << 'EOF'
import redis
r = redis.Redis(host='your-host', port=6379)
r.ping()
print("Redis connection successful!")
EOF
```

4. **Run Redis test**:
```bash
locust -f tests/redis_test.py --host=redis://your-redis-host:6379 \
  --users 20 --spawn-rate 2 --run-time 5m --headless
```

**Redis-specific monitoring**:
- Connection count (don't exceed Redis limits)
- Message throughput
- Pub/Sub latency
- Memory usage

### Step 8: GitHub Actions Integration

Set this up to automatically run tests on code changes:

1. **Add GitHub secrets**:
   - Go to repo Settings > Secrets > Actions
   - Add: `STAGING_URL`, `DATADOG_API_KEY`, `DATADOG_APP_KEY`, `SLACK_WEBHOOK_URL`

2. **Commit the workflow**:
```bash
git add .github/workflows/load-test.yml
git commit -m "Add load testing workflow"
git push
```

3. **Test manual trigger**:
   - Go to Actions tab in GitHub
   - Click "Locust Load Test"
   - Click "Run workflow"
   - Choose parameters and run

4. **Make a test PR**:
   - Create a small code change
   - Open pull request
   - Watch load test run automatically
   - See results posted as PR comment

**What to verify**:
- [ ] Workflow completes successfully
- [ ] Results posted to Slack
- [ ] PR comment appears with results
- [ ] Artifacts (HTML report) are saved

### Step 9: Full POC Test Run

Now run your complete evaluation test:

**Test Configuration**:
- Users: 50 VUs (your peak load estimate)
- Duration: 2 hours (your typical test duration)
- Spawn rate: 5 VUs/second (gradual ramp-up)

**Pre-flight checklist**:
- [ ] Staging environment is stable
- [ ] Datadog is collecting metrics
- [ ] Slack notifications configured
- [ ] Team aware test is running

**Run the test**:
```bash
locust -f tests/basic_test.py \
  --host=https://your-staging-url.com \
  --users 50 \
  --spawn-rate 5 \
  --run-time 2h \
  --headless \
  --html=results/full_poc_test.html \
  --csv=results/full_poc_test
```

**Monitor during test**:
1. **Locust metrics**:
   - Requests per second
   - Response times (avg, median, p95, p99)
   - Error rate

2. **Datadog APM**:
   - Database query performance
   - API endpoint latencies
   - Memory and CPU usage
   - Error logs

3. **Application behavior**:
   - Any alerts triggered?
   - User-facing errors?
   - Unusual log patterns?

**VU Hours Used**: 50 users × 2 hours = 100 VU hours ✅ (within free tier)

## 📊 Evaluating Results

### Key Metrics to Analyze

1. **Response Time**:
   - What's acceptable for your app? (e.g., <500ms for API)
   - Compare p50, p95, p99 percentiles
   - Identify slow endpoints

2. **Throughput**:
   - Requests per second achieved
   - Does it match expected load?

3. **Error Rate**:
   - Should be <1% ideally
   - Investigate any errors

4. **Stability**:
   - Does performance degrade over time?
   - Memory leaks?
   - Connection pool exhaustion?

### Questions to Answer

**For Stakeholders**:
- [ ] Does Locust meet our load testing needs?
- [ ] Is the free tier sufficient? (200 VU hours/month)
- [ ] Do we need Premium? ($399/month for 5,000 VU hours)
- [ ] Are integrations (Datadog, Slack, GitHub) valuable?
- [ ] Is the learning curve acceptable for the team?

**For Technical Team**:
- [ ] Which endpoints are slowest under load?
- [ ] Are there any error patterns?
- [ ] How does database perform under load?
- [ ] Are there any bottlenecks?
- [ ] Is Redis Pub/Sub performant enough?

### Decision Matrix

| Criteria | Weight | Score (1-5) | Notes |
|----------|--------|-------------|-------|
| Ease of use | High | | |
| Cost effectiveness | High | | |
| Integration quality | Medium | | |
| Reporting clarity | Medium | | |
| Team learning curve | Medium | | |
| Protocol support | High | | |
| Cloud vs self-hosted | Low | | |

## 🎯 POC Success Criteria

### Must-Haves
- [ ] Successfully run 2 complete load tests (2 hours, 50 VUs each)
- [ ] Integrate with Datadog
- [ ] Set up GitHub Actions automation
- [ ] Test GraphQL endpoints
- [ ] Document findings clearly

### Nice-to-Haves
- [ ] Redis Pub/Sub testing
- [ ] Slack notifications working
- [ ] Team trained on Locust basics
- [ ] Custom test scenarios created
- [ ] Performance baselines established

## 🔍 Common Issues & Solutions

### Issue: Connection Errors
**Symptom**: Tests fail immediately with connection errors
**Solutions**:
- Verify staging URL is accessible
- Check firewall/VPN requirements
- Confirm authentication is working
- Test with curl first

### Issue: High Error Rates
**Symptom**: >5% of requests failing
**Solutions**:
- Reduce number of users
- Slow down spawn rate
- Check staging environment capacity
- Look for rate limiting

### Issue: Slow Response Times
**Symptom**: Response times >2 seconds
**Solutions**:
- This might be expected! Compare to production
- Check database query performance in Datadog
- Look for N+1 query problems
- Profile slow endpoints

### Issue: Can't Install Dependencies
**Symptom**: pip install fails
**Solutions**:
- Update pip: `pip install --upgrade pip`
- Use Python 3.8 or higher
- Check for conflicting packages
- Try installing one at a time

### Issue: Datadog Not Receiving Metrics
**Symptom**: No `locust.*` metrics in Datadog
**Solutions**:
- Verify API keys are correct
- Check Datadog site setting (US vs EU)
- Look for error messages in console
- Test with simple metric first

## 📝 Documentation Checklist

For successful POC completion, document:

- [ ] **Setup Instructions**: How we configured everything
- [ ] **Test Results**: Screenshots, CSV exports, findings
- [ ] **Performance Baselines**: What's "normal" for our app
- [ ] **Cost Analysis**: Actual usage vs free tier limits
- [ ] **Integration Status**: What works, what needs work
- [ ] **Team Feedback**: Learning curve, usability, satisfaction
- [ ] **Recommendations**: Should we proceed? What tier?
- [ ] **Next Steps**: If approved, what's the rollout plan?

## 🎓 Learning Resources

### For Python Beginners
- Focus on: functions, classes, dictionaries
- You don't need to be a Python expert
- The examples are well-commented

### For Locust
- Official docs: https://docs.locust.io
- Key concepts: Users, tasks, wait times
- Start with examples in this repo

### For Load Testing
- Understand: ramp-up, steady state, ramp-down
- Learn: percentiles (p50, p95, p99)
- Practice: reading performance charts

## 🤝 Getting Help

1. **Internal**: 
   - Ask DevOps team about staging environment
   - Contact Bailey for STG setup
   - Engineering team for API/GraphQL details

2. **Locust Sales**:
   - Follow up from meeting notes
   - Ask about Premium features if needed
   - Technical questions about cloud platform

3. **Community**:
   - Locust Slack community
   - Stack Overflow (tag: locust)
   - GitHub issues for bugs

## ✅ POC Completion

Once you've completed all steps:

1. **Compile Results**:
   - Gather all test reports
   - Create summary dashboard in Datadog
   - Prepare presentation slides

2. **Schedule Stakeholder Meeting**:
   - Present findings
   - Demonstrate integrations
   - Discuss recommendations
   - Get decision: proceed or not?

3. **If Approved**:
   - Decide on plan (Free, Premium, or Enterprise)
   - Set up production load testing schedule
   - Train additional team members
   - Integrate into CI/CD pipeline

4. **If Not Approved**:
   - Document reasons
   - Preserve learnings for future
   - Consider alternatives

Good luck with your POC! 🚀
