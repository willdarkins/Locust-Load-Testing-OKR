import sys
import csv

def check_thresholds(csv_file):

    thresholds = {
        'avg_response_time': 2000,  # milliseconds
        'failure_rate': 5,           # percentage
        'p95_response_time': 5000    # milliseconds
    }
    
    failures = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Type'] == 'Aggregated':
                continue

            avg_response = float(row.get('Average Response Time', 0))
            failure_rate = float(row.get('Failure %', 0))
            
            if avg_response > thresholds['avg_response_time']:
                failures.append(
                    f"❌ Average response time ({avg_response}ms) exceeds threshold ({thresholds['avg_response_time']}ms)"
                )
            
            if failure_rate > thresholds['failure_rate']:
                failures.append(
                    f"❌ Failure rate ({failure_rate}%) exceeds threshold ({thresholds['failure_rate']}%)"
                )
    
    if failures:
        print("\n🚨 Performance Thresholds Breached:")
        for failure in failures:
            print(failure)
        sys.exit(1)
    else:
        print("✅ All performance thresholds passed!")
        sys.exit(0)

if __name__ == '__main__':
    check_thresholds(sys.argv[1])