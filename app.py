from flask import Flask, request, jsonify, render_template
from openai import OpenAI

client = OpenAI()
import os
from openai import OpenAI

client = OpenAI()
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

openai_api_key = os.getenv('Arist_API_KEY')

cred = credentials.Certificate(os.getenv('GOOGLE_FIREBASE_ARISTAI_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({'error': 'No question provided.'}), 400

        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        max_tokens=150)
        print(response)
        answer = response.choices[0].message.content.strip()
        print(answer)

        store_question_answer(question, answer)

        return jsonify({'question': question, 'answer': answer}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def store_question_answer(question, answer):
    db.collection('chat_history').add({
        'question': question,
        'answer': answer,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

@app.route('/history', methods=['GET'])
def get_chat_history():
    history_ref = db.collection('chat_history').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()

    history = []
    for doc in history_ref:
        history.append(doc.to_dict())

    return history

if __name__ == '__main__':
    app.run(debug=True)
