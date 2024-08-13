from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set up the SQLAlchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Define the chat history model
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

def create_chat_history_table():
    with app.app_context():
        db.create_all()  # Creates the table if it doesn't exist

# Call the function to create the table
create_chat_history_table()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    response = model.generate_content(data['prompt'])

    # Save the chat to the database
    chat_history = ChatHistory(user_input=data['prompt'], ai_response=response.text)
    db.session.add(chat_history)
    db.session.commit()

    response = {
        'status': 'success',
        'message': 'Data received successfully!',
        'received_data': response.text
    }
    return jsonify(response)

@app.route('/history', methods=['GET'])
def history():
    # Get the last 10 chats
    chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(10).all()
    chat_list = [{'user_input': chat.user_input, 'ai_response': chat.ai_response, 'timestamp': chat.timestamp} for chat in chats]
    print(chat_list)
    return jsonify(chat_list)

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True,port=5000)
