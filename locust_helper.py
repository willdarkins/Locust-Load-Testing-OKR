#!/usr/bin/env python3
"""
Locust Helper Script

This script provides easy commands for common Locust operations.
Useful for team members new to command-line tools.

Usage:
    python locust_helper.py --help
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment...")
    
    # Check if .env exists
    if not Path('.env').exists():
        print("❌ .env file not found")
        print("💡 Copy .env.example to .env and fill in your values:")
        print("   cp .env.example .env")
        return False
    
    # Check if dependencies are installed
    try:
        import locust
        print(f"✅ Locust installed (version {locust.__version__})")
    except ImportError:
        print("❌ Locust not installed")
        print("💡 Install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    # Check if target host is set
    if not os.getenv('TARGET_HOST'):
        print("⚠️  TARGET_HOST not set in .env")
        print("💡 This is optional if you provide --host in commands")
    else:
        print(f"✅ Target host: {os.getenv('TARGET_HOST')}")
    
    print()
    return True


def run_test_ui(test_file, host=None):
    """Run Locust with web UI."""
    print(f"🚀 Starting Locust web UI...")
    print(f"📁 Test file: {test_file}")
    
    host = host or os.getenv('TARGET_HOST')
    if not host:
        print("❌ No host specified. Use --host or set TARGET_HOST in .env")
        return
    
    print(f"🎯 Target: {host}")
    print(f"🌐 Opening browser to http://localhost:8089")
    print(f"⏹️  Press Ctrl+C to stop\n")
    
    cmd = f"locust -f {test_file} --host={host}"
    subprocess.run(cmd, shell=True)


def run_test_headless(test_file, users, duration, spawn_rate=None, host=None):
    """Run Locust in headless mode (no UI)."""
    print(f"🚀 Starting Locust headless test...")
    print(f"📁 Test file: {test_file}")
    
    host = host or os.getenv('TARGET_HOST')
    if not host:
        print("❌ No host specified. Use --host or set TARGET_HOST in .env")
        return
    
    spawn_rate = spawn_rate or max(1, users // 10)
    
    print(f"🎯 Target: {host}")
    print(f"👥 Users: {users}")
    print(f"⏱️  Duration: {duration}")
    print(f"📈 Spawn rate: {spawn_rate}/sec")
    print()
    
    # Create results directory
    Path('results').mkdir(exist_ok=True)
    
    cmd = (
        f"locust -f {test_file} "
        f"--host={host} "
        f"--users={users} "
        f"--spawn-rate={spawn_rate} "
        f"--run-time={duration} "
        f"--headless "
        f"--html=results/report.html "
        f"--csv=results/stats"
    )
    
    subprocess.run(cmd, shell=True)
    
    print("\n✅ Test complete!")
    print(f"📊 Report: results/report.html")
    print(f"📈 CSV data: results/stats_*.csv")


def quick_test(test_file, host=None):
    """Run a quick 1-minute test with 10 users."""
    print("⚡ Running quick test (10 users, 1 minute)...\n")
    run_test_headless(
        test_file=test_file,
        users=10,
        duration="1m",
        spawn_rate=2,
        host=host
    )


def validate_test_file(test_file):
    """Validate that test file exists and is valid Python."""
    print(f"🔍 Validating test file: {test_file}")
    
    if not Path(test_file).exists():
        print(f"❌ File not found: {test_file}")
        return False
    
    # Try to import the file
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("locustfile", test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✅ Test file is valid Python")
        
        # Check if it has User classes
        from locust import User
        user_classes = [
            name for name, obj in module.__dict__.items()
            if isinstance(obj, type) and issubclass(obj, User) and obj != User
        ]
        
        if user_classes:
            print(f"✅ Found user classes: {', '.join(user_classes)}")
        else:
            print("⚠️  No User classes found in file")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating file: {e}")
        return False


def calculate_vu_hours(users, duration_str):
    """Calculate VU hours for a test configuration."""
    # Parse duration string (e.g., "2h", "30m", "1h30m")
    hours = 0
    
    if 'h' in duration_str:
        hours_part = duration_str.split('h')[0]
        hours += int(hours_part)
        duration_str = duration_str.split('h')[1] if 'h' in duration_str else ""
    
    if 'm' in duration_str:
        mins_part = duration_str.split('m')[0]
        if mins_part:
            hours += int(mins_part) / 60
    
    vu_hours = users * hours
    
    print(f"📊 VU Hours Calculation:")
    print(f"   Users: {users}")
    print(f"   Duration: {hours:.2f} hours")
    print(f"   VU Hours: {vu_hours:.1f}")
    print()
    print(f"Free Tier: 200 VU hours/month")
    print(f"This test: {vu_hours:.1f} VU hours ({vu_hours/200*100:.1f}% of free tier)")
    
    if vu_hours > 200:
        print(f"⚠️  This exceeds free tier! Consider:")
        print(f"   - Reduce users to {int(200/hours)}")
        print(f"   - Reduce duration to {200/users:.1f}h")
        print(f"   - Upgrade to Premium ($399/mo for 5,000 VU hours)")


def list_test_files():
    """List available test files."""
    print("📁 Available test files:\n")
    
    test_dir = Path('tests')
    if not test_dir.exists():
        print("❌ tests/ directory not found")
        return
    
    test_files = list(test_dir.glob('*.py'))
    if not test_files:
        print("No test files found in tests/")
        return
    
    for i, file in enumerate(test_files, 1):
        print(f"{i}. {file.name}")
        
        # Try to extract docstring
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                if len(lines) > 0 and '"""' in lines[0]:
                    # Find closing """
                    docstring_lines = []
                    for line in lines[1:]:
                        if '"""' in line:
                            break
                        docstring_lines.append(line.strip())
                    if docstring_lines:
                        print(f"   {docstring_lines[0]}")
        except:
            pass
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Locust Helper Script - Easy load testing commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check environment setup
  python locust_helper.py check
  
  # List available tests
  python locust_helper.py list
  
  # Run test with UI
  python locust_helper.py ui tests/basic_test.py --host https://staging.myapp.com
  
  # Run quick validation test
  python locust_helper.py quick tests/basic_test.py
  
  # Run full headless test
  python locust_helper.py run tests/basic_test.py --users 50 --duration 2h
  
  # Calculate VU hours
  python locust_helper.py calc --users 50 --duration 2h
  
  # Validate test file
  python locust_helper.py validate tests/basic_test.py
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Check command
    subparsers.add_parser('check', help='Check environment configuration')
    
    # List command
    subparsers.add_parser('list', help='List available test files')
    
    # UI command
    ui_parser = subparsers.add_parser('ui', help='Run test with web UI')
    ui_parser.add_argument('test_file', help='Path to test file')
    ui_parser.add_argument('--host', help='Target host URL')
    
    # Quick command
    quick_parser = subparsers.add_parser('quick', help='Run quick validation test')
    quick_parser.add_argument('test_file', help='Path to test file')
    quick_parser.add_argument('--host', help='Target host URL')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run headless test')
    run_parser.add_argument('test_file', help='Path to test file')
    run_parser.add_argument('--users', type=int, required=True, help='Number of users')
    run_parser.add_argument('--duration', required=True, help='Test duration (e.g., 1h, 30m)')
    run_parser.add_argument('--spawn-rate', type=int, help='Users to spawn per second')
    run_parser.add_argument('--host', help='Target host URL')
    
    # Calculate command
    calc_parser = subparsers.add_parser('calc', help='Calculate VU hours')
    calc_parser.add_argument('--users', type=int, required=True, help='Number of users')
    calc_parser.add_argument('--duration', required=True, help='Test duration (e.g., 2h)')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate test file')
    validate_parser.add_argument('test_file', help='Path to test file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'check':
        check_environment()
    
    elif args.command == 'list':
        list_test_files()
    
    elif args.command == 'ui':
        check_environment()
        run_test_ui(args.test_file, args.host)
    
    elif args.command == 'quick':
        check_environment()
        quick_test(args.test_file, args.host)
    
    elif args.command == 'run':
        check_environment()
        run_test_headless(
            args.test_file,
            args.users,
            args.duration,
            args.spawn_rate,
            args.host
        )
    
    elif args.command == 'calc':
        calculate_vu_hours(args.users, args.duration)
    
    elif args.command == 'validate':
        validate_test_file(args.test_file)


if __name__ == '__main__':
    main()
