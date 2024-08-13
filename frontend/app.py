from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# BACKEND_URL = "http://backend-service:5000"
BACKEND_URL = "http://localhost:5000"


@app.route('/')
def index():
    app.logger.info("Rendering index.html")
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def add_data():
    app.logger.info("Frontend processing submit request")
    
    # Send the user's prompt to the backend service
    r = requests.post(BACKEND_URL+"/submit", json=request.json)
    
    return r.json()

@app.route('/history', methods=['GET'])
def get_history():
    app.logger.info("Frontend fetching chat history")
    
    # Request chat history from the backend service
    r = requests.get(BACKEND_URL+"/history")
    
    return r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
