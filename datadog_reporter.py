"""
Datadog Integration for Locust Load Tests

This module handles sending Locust metrics to Datadog for correlation with
application performance metrics.

Why this matters for your POC:
- See load test metrics alongside application metrics in one place
- Correlate load with database queries, API calls, memory usage
- Easier to identify performance bottlenecks
- Historical comparison of load test results
"""

from datadog import initialize, api, statsd
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class DatadogReporter:
    """
    Sends Locust load test metrics to Datadog.
    
    This class integrates with Locust's event system to automatically
    report metrics as the test runs.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: str = "datadoghq.com"
    ):
        """
        Initialize Datadog reporter.
        
        Args:
            api_key: Datadog API key (reads from env if not provided)
            app_key: Datadog APP key (reads from env if not provided)
            site: Datadog site (datadoghq.com or datadoghq.eu)
        """
        # Get credentials from environment if not provided
        self.api_key = api_key or os.getenv('DATADOG_API_KEY')
        self.app_key = app_key or os.getenv('DATADOG_APP_KEY')
        self.site = site or os.getenv('DATADOG_SITE', 'datadoghq.com')
        
        if not self.api_key or not self.app_key:
            raise ValueError(
                "Datadog credentials not found. Set DATADOG_API_KEY and "
                "DATADOG_APP_KEY environment variables or pass them to constructor."
            )
        
        # Initialize Datadog
        options = {
            'api_key': self.api_key,
            'app_key': self.app_key,
            'api_host': f'https://api.{self.site}'
        }
        initialize(**options)
        
        # Initialize StatsD for real-time metrics
        statsd.host = f"https://api.{self.site}"
        
        # Default tags for all metrics
        self.default_tags = [
            f"environment:{os.getenv('DATADOG_ENVIRONMENT', 'staging')}",
            f"service:{os.getenv('DATADOG_SERVICE', 'locust-load-test')}",
            f"version:{os.getenv('DATADOG_VERSION', '1.0.0')}"
        ]
        
        logger.info("Datadog reporter initialized")
    
    def send_metric(
        self,
        metric_name: str,
        value: float,
        metric_type: str = "gauge",
        tags: Optional[List[str]] = None
    ):
        """
        Send a single metric to Datadog.
        
        Args:
            metric_name: Name of the metric (e.g., 'locust.requests.response_time')
            value: Metric value
            metric_type: Type of metric ('gauge', 'count', 'rate')
            tags: Additional tags for this metric
        
        Metric Naming Convention:
            locust.requests.response_time
            locust.requests.failures
            locust.users.count
            locust.requests.per_second
        """
        all_tags = self.default_tags + (tags or [])
        
        try:
            if metric_type == "gauge":
                statsd.gauge(metric_name, value, tags=all_tags)
            elif metric_type == "count":
                statsd.increment(metric_name, value, tags=all_tags)
            elif metric_type == "rate":
                statsd.rate(metric_name, value, tags=all_tags)
            else:
                logger.warning(f"Unknown metric type: {metric_type}")
        except Exception as e:
            logger.error(f"Failed to send metric {metric_name}: {e}")
    
    def report_request(
        self,
        request_type: str,
        name: str,
        response_time: float,
        success: bool
    ):
        """
        Report a single request to Datadog.
        
        This method should be called for each request Locust makes.
        
        Args:
            request_type: HTTP method (GET, POST, etc.) or protocol (GraphQL, Redis)
            name: Request name (e.g., 'Homepage', 'Login API')
            response_time: Response time in milliseconds
            success: Whether the request succeeded
        """
        tags = [
            f"request_type:{request_type}",
            f"endpoint:{name}",
            f"success:{success}"
        ]
        
        # Send response time
        self.send_metric(
            "locust.request.response_time",
            response_time,
            metric_type="gauge",
            tags=tags
        )
        
        # Send request count
        self.send_metric(
            "locust.request.count",
            1,
            metric_type="count",
            tags=tags
        )
        
        # Send failure count if failed
        if not success:
            self.send_metric(
                "locust.request.failures",
                1,
                metric_type="count",
                tags=tags
            )
    
    def report_test_summary(
        self,
        stats: Dict,
        test_name: str,
        duration_seconds: float
    ):
        """
        Report summary statistics at the end of a test.
        
        Args:
            stats: Dictionary containing test statistics
            test_name: Name of the test
            duration_seconds: Total test duration
        """
        tags = [f"test_name:{test_name}"]
        
        # Total requests
        self.send_metric(
            "locust.test.total_requests",
            stats.get('num_requests', 0),
            metric_type="gauge",
            tags=tags
        )
        
        # Total failures
        self.send_metric(
            "locust.test.total_failures",
            stats.get('num_failures', 0),
            metric_type="gauge",
            tags=tags
        )
        
        # Average response time
        self.send_metric(
            "locust.test.avg_response_time",
            stats.get('avg_response_time', 0),
            metric_type="gauge",
            tags=tags
        )
        
        # Requests per second
        rps = stats.get('num_requests', 0) / duration_seconds if duration_seconds > 0 else 0
        self.send_metric(
            "locust.test.requests_per_second",
            rps,
            metric_type="gauge",
            tags=tags
        )
        
        # Error rate percentage
        total = stats.get('num_requests', 0)
        failures = stats.get('num_failures', 0)
        error_rate = (failures / total * 100) if total > 0 else 0
        self.send_metric(
            "locust.test.error_rate",
            error_rate,
            metric_type="gauge",
            tags=tags
        )
        
        logger.info(f"Test summary sent to Datadog: {test_name}")
    
    def create_event(
        self,
        title: str,
        text: str,
        alert_type: str = "info",
        tags: Optional[List[str]] = None
    ):
        """
        Create a Datadog event (appears in event stream).
        
        Useful for marking test start/stop, deployments, incidents, etc.
        
        Args:
            title: Event title
            text: Event description (supports markdown)
            alert_type: 'info', 'warning', 'error', or 'success'
            tags: Event tags
        """
        all_tags = self.default_tags + (tags or [])
        
        try:
            api.Event.create(
                title=title,
                text=text,
                alert_type=alert_type,
                tags=all_tags,
                date_happened=int(datetime.now().timestamp())
            )
            logger.info(f"Datadog event created: {title}")
        except Exception as e:
            logger.error(f"Failed to create Datadog event: {e}")


# =============================================================================
# LOCUST EVENT HANDLERS
# =============================================================================
# These functions integrate with Locust's event system

def setup_datadog_reporting(environment):
    """
    Set up automatic Datadog reporting for Locust tests.
    
    Call this function in your locustfile to automatically send metrics.
    
    Example usage in your locustfile:
        from locust import events
        from utils.datadog_reporter import setup_datadog_reporting
        
        @events.init.add_listener
        def on_locust_init(environment, **kwargs):
            setup_datadog_reporting(environment)
    """
    from locust import events
    
    reporter = DatadogReporter()
    
    # Create event when test starts
    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        reporter.create_event(
            title="Locust Load Test Started",
            text=f"Starting load test with {environment.runner.target_user_count} users",
            alert_type="info",
            tags=["test:start"]
        )
    
    # Report each request
    @events.request.add_listener
    def on_request(
        request_type,
        name,
        response_time,
        response_length,
        exception,
        context,
        **kwargs
    ):
        success = exception is None
        reporter.report_request(
            request_type=request_type,
            name=name,
            response_time=response_time,
            success=success
        )
    
    # Report user count changes
    @events.spawning_complete.add_listener
    def on_spawning_complete(user_count, **kwargs):
        reporter.send_metric(
            "locust.users.active",
            user_count,
            metric_type="gauge"
        )
    
    # Create event and report summary when test stops
    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        stats = environment.stats.total
        
        summary_stats = {
            'num_requests': stats.num_requests,
            'num_failures': stats.num_failures,
            'avg_response_time': stats.avg_response_time,
            'max_response_time': stats.max_response_time,
            'min_response_time': stats.min_response_time,
        }
        
        reporter.report_test_summary(
            stats=summary_stats,
            test_name="locust_load_test",
            duration_seconds=environment.runner.stats.total.last_request_timestamp - 
                           environment.runner.stats.total.start_time
        )
        
        # Create event
        error_rate = (summary_stats['num_failures'] / summary_stats['num_requests'] * 100) \
                     if summary_stats['num_requests'] > 0 else 0
        
        alert_type = "error" if error_rate > 5 else "success"
        
        reporter.create_event(
            title="Locust Load Test Completed",
            text=f"""
            Test Summary:
            - Total Requests: {summary_stats['num_requests']:,}
            - Failures: {summary_stats['num_failures']:,} ({error_rate:.2f}%)
            - Avg Response Time: {summary_stats['avg_response_time']:.2f}ms
            - Max Response Time: {summary_stats['max_response_time']:.2f}ms
            """,
            alert_type=alert_type,
            tags=["test:complete"]
        )
    
    logger.info("Datadog reporting enabled for Locust tests")


# =============================================================================
# USAGE EXAMPLES
# =============================================================================
"""
Example 1: Manual metric reporting
    from utils.datadog_reporter import DatadogReporter
    
    reporter = DatadogReporter()
    reporter.send_metric("custom.metric", 42.0, tags=["custom:tag"])

Example 2: Automatic reporting in locustfile
    from locust import HttpUser, task, events
    from utils.datadog_reporter import setup_datadog_reporting
    
    @events.init.add_listener
    def on_locust_init(environment, **kwargs):
        setup_datadog_reporting(environment)
    
    class MyUser(HttpUser):
        @task
        def my_task(self):
            self.client.get("/")

Example 3: Create custom events
    from utils.datadog_reporter import DatadogReporter
    
    reporter = DatadogReporter()
    reporter.create_event(
        title="Performance Threshold Exceeded",
        text="Response time exceeded 2000ms threshold",
        alert_type="warning",
        tags=["alert:performance"]
    )

Benefits of Datadog Integration:
1. Correlate load test results with application metrics
2. See exactly which queries/APIs slow down under load
3. Historical tracking of performance over time
4. Alert on performance degradations
5. Single pane of glass for all monitoring
"""
