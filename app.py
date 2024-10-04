from flask import Flask, request, jsonify, render_template
import openai
import os
import boto3
from botocore.exceptions import ClientError
import json
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai_api_key = os.getenv('Arist_API_KEY')
openai.api_key = openai_api_key

def get_firebase_credentials():
    secret_name = "google-firebase-aristai"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    print("Secret from AWS: "+secret)
    return json.loads(secret)

def initialize_firebase():
    if not firebase_admin._apps:
        creds_dict = get_firebase_credentials()
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace('\\n', '\n')
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)

initialize_firebase()
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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=150
        )
        answer = response.choices[0].message['content'].strip()
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
    try:
        history_ref = db.collection('chat_history').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()

        history = []
        for doc in history_ref:
            history.append(doc.to_dict())

        return jsonify(history), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
