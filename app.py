from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Conversation
import os

app = Flask(__name__)

# Set up the database
engine = create_engine('sqlite:///conversations.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Load the corpus
with open('corpus.txt', 'r') as file:
    corpus = file.read().splitlines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    conversation_id = data['conversation_id']
    response = generate_response(user_message, conversation_id)
    return jsonify({'response': response})

def generate_response(user_message, conversation_id):
    # Fetch conversation history
    history = session.query(Conversation).filter_by(id=conversation_id).all()
    history_text = " ".join([conv.message for conv in history])
    
    # Generate response based on corpus
    response = get_response_from_corpus(user_message)
    if response is None:
        response = "Please contact our support for more information."

    # Save the conversation
    new_conv = Conversation(id=conversation_id, message=user_message)
    session.add(new_conv)
    session.commit()

    return response

def get_response_from_corpus(user_message):
    print(f"User Message: {user_message}")
    # Simple keyword-based search
    for line in corpus:
        if user_message.lower() in line.lower():
            print(f"Found match in corpus: {line}")
            return line.split("?")[1].strip()  # Assuming "question? answer" format
    print("No match found in corpus")
    return None  # Return None if no matching response is found

if __name__ == '__main__':
    app.run(debug=True)
