import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit():
    # Get JSON data from the request
    data = request.get_json()
    print(data)
    response = model.generate_content(data['prompt'])
    
    # # Process the data (for example, print it to the console)
    # print(f"Received data: {data}")

    # Return a JSON response
    response = {
        'status': 'success',
        'message': 'Data received successfully!',
        'received_data': response.text
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)

