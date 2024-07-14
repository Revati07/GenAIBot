from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Conversation

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///conversations.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Load corpus from file
with open('corpus.txt', 'r') as file:
    corpus = file.read().splitlines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    response = generate_response(user_message)
    return jsonify({'response': response})

def generate_response(user_message):
    try:
        # Generate response based on user query
        if 'best red wine' in user_message.lower():
            response = "Our best red wine is the 2015 Merlot."
        elif 'store hours' in user_message.lower():
            response = "Our store hours are from 9 AM to 9 PM every day."
        else:
            response = get_response_from_corpus(user_message)

        if response is None:
            response = "Please contact our support for more information."

        # Save the conversation
        new_conv = Conversation(message=user_message)
        session.add(new_conv)
        session.commit()

        return response
    except Exception as e:
        return str(e)

def get_response_from_corpus(user_message):
    # Simple keyword-based search
    for line in corpus:
        if user_message.lower() in line.lower():
            return line.split("?")[1].strip()  # Assuming "question? answer" format
    return None

if __name__ == '__main__':
    app.run(debug=True)
