from flask import Flask, request
from cloudevents.http import CloudEvent, from_http
from cloudevents.conversion import to_binary, to_structured
import requests
import os
import signal
import sys

app = Flask(__name__)

def graceful_exit(signum, frame):
    print("Gracefully shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_exit)

@app.route("/", methods=['GET'])
def home():
  print("\n\n------------------------[GET] /------------------------")
  
  data = {"id": os.environ.get('ID', 'unknown')}
  return data, 200

@app.route("/event", methods=['get'])
def send_event():
  print("\n\n------------------------[POST] /send------------------------")
  
  ID = os.environ.get('ID', 'unknown')
  url = os.getenv('EVENT_URL')
  
  attributes = {
      "type": "com.demo.event",
      "source": ID,
  }

  data = {"message": "event sent from app with id: " + ID}

  event = CloudEvent(attributes, data)

  headers, body = to_structured(event)
  response = requests.post(url, headers=headers, data=body)

  code = 200
  if 200 <= response.status_code <= 299:
      print("Event sent successfully")
      data = {"status": "Event sent"}
      
  else:
      print(f"Error sending event: {response.status_code}, {response.text}")
      data = {"status": "Event failed"}
      code = 500
  return data, code


@app.route('/', methods=['POST'])
def handle_event():
  print("\n\n------------------------[POST] /------------------------")
  
  
  event = from_http(request.headers, request.get_data())

  # you can access cloudevent fields as seen below
  print(
    f"Found {event['id']} from {event['source']} with type "
    f"{event['type']} and specversion {event['specversion']}"
  )
  
  print("\nContent:")
  print(
    f"{event}"
  )

  return "", 204

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)