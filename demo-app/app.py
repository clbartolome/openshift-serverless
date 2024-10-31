from flask import Flask, request
import requests
import os

app = FastAPI()

@app.get("/", methods=['GET'])
def home():
    print("/ - request")
    return {"message": os.environ.get('MESSAGE', 'Default Message')}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)