"""
Redis Pub/Sub Load Testing with Locust

This file demonstrates how to test Redis Pub/Sub with Locust.
Your application uses Redis Pub/Sub, which is different from HTTP testing.

Redis Pub/Sub Basics:
- Publishers send messages to channels
- Subscribers listen to channels
- Messages are fire-and-forget (not stored)
- Used for real-time features like notifications, chat, live updates

Load Testing Considerations:
- Can't use HttpUser (no HTTP involved!)
- Need to extend base User class
- Must manage Redis connections carefully
- Focus on message throughput and latency
"""

from locust import User, task, between, events
import redis
import json
import time
from datetime import datetime


class RedisPublisher(User):
    """
    Virtual user that publishes messages to Redis channels.
    
    Use this to simulate:
    - Backend services publishing events
    - User actions that trigger notifications
    - Real-time data updates
    """
    
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Initialize Redis connection when user starts.
        
        Important: Each virtual user gets their own Redis connection.
        With 100 VUs, you'll have 100 Redis connections!
        """
        # Replace with your Redis connection details
        self.redis_client = redis.Redis(
            host='localhost',  # Your Redis host (e.g., from STG environment)
            port=6379,
            db=0,
            decode_responses=True,  # Automatically decode bytes to strings
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
        # Test connection on startup
        try:
            self.redis_client.ping()
            print(f"Publisher {id(self)}: Redis connection successful")
        except redis.ConnectionError as e:
            print(f"Publisher {id(self)}: Failed to connect to Redis: {e}")
    
    @task(3)
    def publish_user_notification(self):
        """
        Simulate publishing a user notification.
        
        Example use case: User receives a new message, friend request, etc.
        """
        channel = "notifications:user:123"
        
        message = {
            "type": "new_message",
            "userId": "user123",
            "message": "You have a new message",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Start timing (for Locust metrics)
        start_time = time.time()
        
        try:
            # Publish message to channel
            # Returns number of subscribers who received the message
            subscriber_count = self.redis_client.publish(
                channel,
                json.dumps(message)
            )
            
            # Calculate elapsed time
            elapsed = int((time.time() - start_time) * 1000)  # Convert to milliseconds
            
            # Report success to Locust
            # This makes it show up in the Locust UI and reports
            events.request.fire(
                request_type="Redis Pub",
                name="Publish User Notification",
                response_time=elapsed,
                response_length=len(json.dumps(message)),
                exception=None,
                context={}
            )
            
            # Log if no subscribers (might indicate a problem)
            if subscriber_count == 0:
                print(f"Warning: No subscribers for channel {channel}")
                
        except redis.RedisError as e:
            # Report failure to Locust
            elapsed = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="Redis Pub",
                name="Publish User Notification",
                response_time=elapsed,
                response_length=0,
                exception=e,
                context={}
            )
            print(f"Redis publish error: {e}")
    
    @task(2)
    def publish_system_event(self):
        """
        Simulate publishing a system-wide event.
        
        Example: Deployment notification, system maintenance, etc.
        """
        channel = "system:events"
        
        message = {
            "type": "deployment",
            "service": "api-server",
            "version": "1.2.3",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        start_time = time.time()
        
        try:
            subscriber_count = self.redis_client.publish(channel, json.dumps(message))
            elapsed = int((time.time() - start_time) * 1000)
            
            events.request.fire(
                request_type="Redis Pub",
                name="Publish System Event",
                response_time=elapsed,
                response_length=len(json.dumps(message)),
                exception=None,
                context={}
            )
            
        except redis.RedisError as e:
            elapsed = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="Redis Pub",
                name="Publish System Event",
                response_time=elapsed,
                response_length=0,
                exception=e,
                context={}
            )
    
    def on_stop(self):
        """Clean up Redis connection when user stops."""
        if hasattr(self, 'redis_client'):
            self.redis_client.close()
            print(f"Publisher {id(self)}: Closed Redis connection")


class RedisSubscriber(User):
    """
    Virtual user that subscribes to Redis channels.
    
    Use this to simulate:
    - Frontend clients listening for updates
    - Microservices consuming events
    - Real-time notification systems
    
    NOTE: Subscribers are long-running connections!
    They don't follow the typical task pattern.
    """
    
    wait_time = between(0.1, 0.5)  # Shorter wait time for subscribers
    
    def on_start(self):
        """Set up subscriber connection."""
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        
        # Create a pubsub object
        self.pubsub = self.redis_client.pubsub()
        
        # Subscribe to channels
        self.pubsub.subscribe('notifications:user:123', 'system:events')
        
        # Track statistics
        self.messages_received = 0
        self.total_latency = 0
        
        print(f"Subscriber {id(self)}: Subscribed to channels")
    
    @task
    def listen_for_messages(self):
        """
        Listen for incoming messages.
        
        This is the core subscriber behavior.
        It continuously listens for messages.
        """
        start_time = time.time()
        
        try:
            # Get next message (non-blocking with timeout)
            message = self.pubsub.get_message(timeout=1.0)
            
            if message and message['type'] == 'message':
                # We received an actual message (not subscription confirmation)
                self.messages_received += 1
                
                # Try to parse message timestamp to calculate latency
                try:
                    data = json.loads(message['data'])
                    msg_timestamp = datetime.fromisoformat(data['timestamp'])
                    latency = (datetime.utcnow() - msg_timestamp).total_seconds() * 1000
                    self.total_latency += latency
                except (json.JSONDecodeError, KeyError, ValueError):
                    latency = 0
                
                # Report to Locust
                elapsed = int((time.time() - start_time) * 1000)
                events.request.fire(
                    request_type="Redis Sub",
                    name=f"Receive from {message['channel']}",
                    response_time=elapsed,
                    response_length=len(message['data']),
                    exception=None,
                    context={"latency_ms": latency}
                )
            
            # If no message, still report (shows subscriber is active)
            elif message is None:
                elapsed = int((time.time() - start_time) * 1000)
                # Don't report as a request, just continue listening
                pass
                
        except redis.RedisError as e:
            elapsed = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="Redis Sub",
                name="Receive Message",
                response_time=elapsed,
                response_length=0,
                exception=e,
                context={}
            )
    
    def on_stop(self):
        """Clean up subscriber connection."""
        if hasattr(self, 'pubsub'):
            self.pubsub.unsubscribe()
            self.pubsub.close()
        
        if hasattr(self, 'redis_client'):
            self.redis_client.close()
        
        # Print statistics
        if self.messages_received > 0:
            avg_latency = self.total_latency / self.messages_received
            print(f"Subscriber {id(self)}: Received {self.messages_received} messages, "
                  f"avg latency: {avg_latency:.2f}ms")


# =============================================================================
# COMBINED PUBLISHER/SUBSCRIBER SCENARIO
# =============================================================================

class HybridRedisUser(User):
    """
    User that both publishes and subscribes.
    Useful for testing bidirectional communication.
    """
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize both publisher and subscriber connections."""
        # Publisher connection
        self.pub_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        
        # Subscriber connection (separate connection required)
        self.sub_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        self.pubsub = self.sub_client.pubsub()
        self.pubsub.subscribe('chat:room:1')
    
    @task(2)
    def send_chat_message(self):
        """Publish a chat message."""
        message = {
            "user": "user123",
            "text": "Hello, world!",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        start_time = time.time()
        try:
            self.pub_client.publish('chat:room:1', json.dumps(message))
            elapsed = int((time.time() - start_time) * 1000)
            
            events.request.fire(
                request_type="Redis Pub/Sub",
                name="Send Chat Message",
                response_time=elapsed,
                response_length=len(json.dumps(message)),
                exception=None,
                context={}
            )
        except redis.RedisError as e:
            elapsed = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="Redis Pub/Sub",
                name="Send Chat Message",
                response_time=elapsed,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(1)
    def receive_chat_message(self):
        """Listen for chat messages."""
        start_time = time.time()
        try:
            message = self.pubsub.get_message(timeout=0.5)
            elapsed = int((time.time() - start_time) * 1000)
            
            if message and message['type'] == 'message':
                events.request.fire(
                    request_type="Redis Pub/Sub",
                    name="Receive Chat Message",
                    response_time=elapsed,
                    response_length=len(message['data']),
                    exception=None,
                    context={}
                )
        except redis.RedisError as e:
            elapsed = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="Redis Pub/Sub",
                name="Receive Chat Message",
                response_time=elapsed,
                response_length=0,
                exception=e,
                context={}
            )
    
    def on_stop(self):
        """Clean up connections."""
        if hasattr(self, 'pubsub'):
            self.pubsub.unsubscribe()
            self.pubsub.close()
        if hasattr(self, 'pub_client'):
            self.pub_client.close()
        if hasattr(self, 'sub_client'):
            self.sub_client.close()


# =============================================================================
# REDIS PUB/SUB LOAD TESTING TIPS
# =============================================================================
"""
Key Considerations:

1. CONNECTION MANAGEMENT
   - Each subscriber needs its own connection
   - Monitor Redis connection count (use Redis INFO command)
   - Be careful with 100+ subscribers (connection limits)

2. MESSAGE THROUGHPUT
   - Test with realistic message sizes
   - Monitor Redis memory usage
   - Test burst scenarios (many messages at once)

3. LATENCY MEASUREMENT
   - Include timestamps in messages
   - Calculate end-to-end latency (publish → receive)
   - Test across different network conditions

4. CHANNEL PATTERNS
   - Test both specific channels and pattern matching
   - Example: pubsub.psubscribe('user:*') matches user:123, user:456, etc.

5. ERROR SCENARIOS
   - Test connection drops
   - Test Redis server restart
   - Test network partitions

6. MONITORING WITH DATADOG
   - Track messages published/second
   - Monitor subscriber lag
   - Alert on connection failures
   - Track Redis memory usage during tests

7. REALISTIC SCENARIOS
   - Mix publishers and subscribers (not all publishers)
   - Vary message frequency (not constant rate)
   - Test idle subscribers (connected but no messages)

8. REDIS CONFIGURATION
   - Check maxclients setting (default 10000)
   - Monitor connected_clients metric
   - Watch for 'max clients reached' errors
"""

# =============================================================================
# HOW TO RUN REDIS TESTS
# =============================================================================
"""
Basic run (mix of publishers and subscribers):
  locust -f tests/redis_test.py --host=redis://your-redis-host:6379

Specific user class:
  locust -f tests/redis_test.py --host=redis://your-redis-host:6379 RedisPublisher

Test configuration example:
  locust -f tests/redis_test.py \
    --host=redis://staging-redis.yourapp.com:6379 \
    --users 50 \
    --spawn-rate 2 \
    --run-time 1h \
    --headless

Monitor during test:
  # In Redis CLI
  redis-cli
  > INFO clients
  > PUBSUB NUMSUB channel-name
  > PUBSUB NUMPAT

Important: Redis Pub/Sub tests are NOT HTTP, so:
- They won't show up in browser performance tools
- You need Redis monitoring (use Datadog Redis integration)
- Connection management is critical
"""
