# 🗺️ Project Navigation Guide

Welcome! This guide helps you navigate the Locust POC repository.

## 🚦 Start Here

New to the project? Follow this order:

1. **PROJECT_SUMMARY.md** ← Read this first (5 min)
   - Overview of what's included
   - Your POC requirements alignment
   - Project statistics

2. **QUICKSTART.md** ← Then do this (5 min)
   - Get your first test running
   - Hands-on introduction
   - Verify everything works

3. **README.md** ← Then read this (15 min)
   - Complete project documentation
   - Setup instructions
   - Technical details

4. **POC_GUIDE.md** ← Follow this for execution (3 weeks)
   - Week-by-week execution plan
   - Detailed step-by-step instructions
   - Success criteria

5. **CHEATSHEET.md** ← Keep this handy (ongoing)
   - Quick command reference
   - Common operations
   - Troubleshooting tips

## 📁 File Organization

```
locust-poc/
│
├── 📚 DOCUMENTATION (Read these)
│   ├── PROJECT_SUMMARY.md    ← Start: Overview & stats
│   ├── QUICKSTART.md          ← Start: 5-minute quick start
│   ├── README.md              ← Read: Complete documentation
│   ├── POC_GUIDE.md           ← Follow: Execution plan
│   ├── CHEATSHEET.md          ← Reference: Commands & tips
│   └── INDEX.md               ← You are here!
│
├── 🧪 TEST FILES (Study & customize these)
│   └── tests/
│       ├── basic_test.py         ← Beginner: Start here
│       ├── complete_example.py   ← Intermediate: Full featured
│       ├── graphql_test.py       ← Advanced: GraphQL specific
│       └── redis_test.py         ← Advanced: Redis Pub/Sub
│
├── 🛠️ UTILITIES (Use these)
│   ├── utils/
│   │   └── datadog_reporter.py   ← Datadog integration
│   └── locust_helper.py           ← Command helper script
│
├── ⚙️ CONFIGURATION (Set these up)
│   ├── .env.example               ← Copy to .env and configure
│   ├── requirements.txt           ← Python dependencies
│   └── .gitignore                 ← Git ignore rules
│
└── 🔄 CI/CD (Deploy this)
    └── .github/workflows/
        └── load-test.yml          ← GitHub Actions workflow
```

## 🎯 By User Type

### If You're New to Python
1. Read: **QUICKSTART.md**
2. Study: **tests/basic_test.py** (heavily commented)
3. Run: `python locust_helper.py --help`
4. Practice: Modify task weights in basic_test.py

### If You're New to Load Testing
1. Read: **PROJECT_SUMMARY.md** (concepts explained)
2. Read: **QUICKSTART.md** (hands-on)
3. Study: "Understanding Locust Concepts" in README.md
4. Experiment: Run tests with different user counts

### If You're a DevOps Engineer
1. Read: **POC_GUIDE.md** (integration focus)
2. Study: **.github/workflows/load-test.yml**
3. Study: **utils/datadog_reporter.py**
4. Setup: Environment variables and secrets

### If You're a Product Manager
1. Read: **PROJECT_SUMMARY.md** (business alignment)
2. Review: POC scope and cost analysis
3. Track: Success metrics in POC_GUIDE.md
4. Present: Use findings for stakeholder buy-in

## 🎓 By Learning Goal

### Want to Run Your First Test?
→ **QUICKSTART.md** (5 minutes)

### Want to Understand Locust?
→ **README.md** → **tests/basic_test.py**

### Want to Test GraphQL?
→ **tests/graphql_test.py**

### Want to Test Redis?
→ **tests/redis_test.py**

### Want to Integrate with Datadog?
→ **utils/datadog_reporter.py** → **POC_GUIDE.md** (Step 5)

### Want to Automate in CI/CD?
→ **.github/workflows/load-test.yml** → **POC_GUIDE.md** (Step 8)

### Want Quick Commands?
→ **CHEATSHEET.md**

### Want the Complete POC Plan?
→ **POC_GUIDE.md**

## 🔍 By Task

### Setup & Installation
1. README.md (Prerequisites & Installation sections)
2. requirements.txt (dependencies)
3. .env.example (configuration)

### Running Tests
1. QUICKSTART.md (quick validation)
2. CHEATSHEET.md (all commands)
3. locust_helper.py (helper script)

### Writing Tests
1. tests/basic_test.py (learn structure)
2. tests/complete_example.py (full features)
3. tests/graphql_test.py (protocol specific)

### Integrations
1. utils/datadog_reporter.py (Datadog)
2. .github/workflows/load-test.yml (GitHub Actions)
3. POC_GUIDE.md Steps 5-8 (setup guides)

### Troubleshooting
1. CHEATSHEET.md (common issues)
2. QUICKSTART.md (basic troubleshooting)
3. POC_GUIDE.md (detailed solutions)

## 📊 By Project Phase

### Phase 1: Initial Setup (Day 1)
- [ ] PROJECT_SUMMARY.md
- [ ] QUICKSTART.md  
- [ ] README.md (Installation)
- [ ] .env.example → .env
- [ ] requirements.txt (install)

### Phase 2: Basic Testing (Week 1)
- [ ] tests/basic_test.py
- [ ] locust_helper.py
- [ ] CHEATSHEET.md
- [ ] Run first test successfully

### Phase 3: Integration (Week 2)
- [ ] utils/datadog_reporter.py
- [ ] .github/workflows/load-test.yml
- [ ] POC_GUIDE.md (Steps 5-8)
- [ ] Test all integrations

### Phase 4: Advanced Testing (Week 3)
- [ ] tests/graphql_test.py
- [ ] tests/redis_test.py
- [ ] tests/complete_example.py
- [ ] Full POC execution

### Phase 5: Completion
- [ ] POC_GUIDE.md (completion checklist)
- [ ] Document findings
- [ ] Stakeholder presentation
- [ ] Decision & next steps

## 🔗 Key Concepts by File

### Virtual Users (VUs)
- README.md (definition)
- QUICKSTART.md (practical example)
- tests/basic_test.py (implementation)

### VU Hours
- PROJECT_SUMMARY.md (calculation)
- POC_GUIDE.md (capacity analysis)
- locust_helper.py (calculator)

### Task Weighting
- tests/basic_test.py (explained)
- tests/complete_example.py (realistic examples)

### Response Validation
- tests/basic_test.py (basic validation)
- tests/complete_example.py (comprehensive validation)

### Datadog Integration
- utils/datadog_reporter.py (implementation)
- tests/complete_example.py (usage example)
- POC_GUIDE.md (setup guide)

## 💡 Pro Tips

### Before Starting POC
1. Read PROJECT_SUMMARY.md completely
2. Run through QUICKSTART.md successfully
3. Skim all test files to understand structure
4. Review POC_GUIDE.md timeline

### During POC
1. Keep CHEATSHEET.md open for quick reference
2. Document learnings as you go
3. Test integrations incrementally
4. Monitor Datadog during tests

### After POC
1. Complete POC_GUIDE.md checklist
2. Compile findings from all test runs
3. Use PROJECT_SUMMARY.md for presentation
4. Share learnings with team

## 🆘 Quick Help

**Can't get started?**
→ QUICKSTART.md

**Command not working?**
→ CHEATSHEET.md

**Don't understand a concept?**
→ README.md → Look for educational comments in test files

**Integration failing?**
→ POC_GUIDE.md (Step-by-step guides)

**Need to explain to stakeholders?**
→ PROJECT_SUMMARY.md

## 📈 Tracking Progress

Use this checklist to track your POC progress:

- [ ] Read PROJECT_SUMMARY.md
- [ ] Complete QUICKSTART.md
- [ ] Read README.md
- [ ] Ran first test successfully
- [ ] Customized a test file
- [ ] Set up Datadog integration
- [ ] Configured GitHub Actions
- [ ] Tested GraphQL endpoints
- [ ] Tested Redis (if applicable)
- [ ] Ran full 2-hour POC test
- [ ] Documented findings
- [ ] Completed POC_GUIDE.md checklist
- [ ] Presented to stakeholders
- [ ] Made go/no-go decision

## 🎯 Your Next Action

Based on where you are:

**Just received this project?**
→ Open **PROJECT_SUMMARY.md**

**Ready to get hands-on?**
→ Open **QUICKSTART.md**

**Need deep dive?**
→ Open **README.md**

**Starting POC execution?**
→ Open **POC_GUIDE.md**

**Need a command?**
→ Open **CHEATSHEET.md**

---

**Remember**: This is a learning project. Take your time, read the comments, and don't hesitate to experiment. Every file is designed to teach while providing production-ready code.

**Questions?** Check the relevant documentation file above, or refer to POC_GUIDE.md's "Getting Help" section.

**Good luck with your POC!** 🚀
