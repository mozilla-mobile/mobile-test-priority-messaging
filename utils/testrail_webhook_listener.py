import requests
import os
import time
import hmac
import hashlib
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your basic authentication credentials
PASSWORD = "149.99.99.99" #example ip address
SLACK_SIGNING_SECRET = os.getenv('TESTRAIL_WEBHOOK_LISTENER_SLACK_SIGNING_SECRET')


def verify_signature(request):
    # Get the Slack headers
    slack_signature = request.headers.get("X-Slack-Signature")
    slack_timestamp = request.headers.get("X-Slack-Request-Timestamp")

    if abs(time.time() - int(slack_timestamp)) > 60 * 5:
        # If the request is older than 5 minutes, reject it
        return False

    # Create the basestring for the signature
    request_body = request.get_data(as_text=True)
    sig_basestring = f"v0:{slack_timestamp}:{request_body}"

    # Compute the hash using your signing secret
    my_signature = (
        "v0="
        + hmac.new(
            SLACK_SIGNING_SECRET.encode("utf-8"),
            sig_basestring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    )

    # Compare the computed signature with the Slack signature
    return hmac.compare_digest(my_signature, slack_signature)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verify_signature(request):
        abort(400, "Verification failed")

    data = request.get_json()

    # Handle Slack's challenge verification
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # Handle other events here
    # For example, listening for messages in a channel
    # You can add more logic here to process events
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Capture the incoming webhook payload
        payload = request.json
        print(f"Received payload: {payload}")

        # Define your Slack webhook URL
        slack_webhook_url = os.getenv('TESTRAIL_WEBHOOK_LISTENER_SLACK')

        # Forward the webhook data to Slack
        slack_message = {"text": f"Received webhook when closing Milestone: {payload}"}

        # Send the request to Slack
        response = requests.post(slack_webhook_url, json=slack_message)

        # Log the Slack response
        print(
            f"Slack response status: {response.status_code}, response: {response.text}"
        )

        # Return success/failure based on the response from Slack
        if response.status_code == 200:
            return jsonify({"status": "Message forwarded to Slack"}), 200
        else:
            return (
                jsonify({"status": "Error sending to Slack", "error": response.text}),
                500,
            )
    except Exception as e:
        print(f"Error forwarding to Slack: {e}")
        return jsonify({"status": "Error forwarding to proxy", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5299)
