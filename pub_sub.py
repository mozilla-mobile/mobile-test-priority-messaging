import pika
import ssl
import json
from dotenv import load_dotenv
import os

load_dotenv('.env')
# example credentials
PULSE_USER = "jajohnson"
PULSE_PASSWORD = "test1234"
PULSE_URL = "pulse.mozilla.org"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

credentials = pika.PlainCredentials(PULSE_USER, PULSE_PASSWORD)
parameters = pika.ConnectionParameters(
    host=PULSE_URL,
    port=5671,
    virtual_host='/',
    credentials=credentials,
    ssl_options=pika.SSLOptions(context=ssl_context)
)

def on_message(channel, method, properties, body):
    """Callback for handling incoming Pulse messages."""
    print(f"Received message with routing key {method.routing_key}:")
    try:
        message = json.loads(body)
        print(json.dumps(message, indent=4))
    except json.JSONDecodeError:
        print("Message body is not JSON:", body)

try:
    # Establish connection
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Exchange for Taskcluster notifications
    exchange = 'exchange/taskcluster-notify/v1/notification'

    # Declare a temporary queue
    print("Declaring a temporary queue...")
    queue = channel.queue_declare(queue='queue/jajohnson/task-notifications', exclusive=True, auto_delete=True)
    queue_name = queue.method.queue
    print(f"Temporary queue declared: {queue_name}")

    # Bind the queue to the exchange with the specified routing key
    routing_key = 'primary.#.try-task'
    print(f"Binding temporary queue '{queue_name}' to exchange '{exchange}' with routing key '{routing_key}'...")
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
    print("Successfully bound to the exchange!")

    # Start consuming messages
    print("Listening for messages...")
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    channel.start_consuming()

except pika.exceptions.ChannelClosedByBroker as e:
    print(f"Channel error: {e}")
except pika.exceptions.AMQPConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()