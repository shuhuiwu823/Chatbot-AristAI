# Chatbot-AristAI
This is a Flask-based web application that allows users to ask questions, process them using OpenAI's GPT model, and store the questions and answers in Firebase Firestore. The app also supports retrieving the chat history.

Features

Ask questions and receive responses from OpenAI's GPT-3.5-turbo model.
Store chat history (questions and answers) in Firebase Firestore.
Retrieve the history of all questions and answers.

Requirements

Make sure you have the following installed:

Python 3.x
Flask
OpenAI Python library
Firebase Admin SDK
Flask-CORS

Running the Application

Clone this repository or download the project files.
Ensure all dependencies are installed as per the requirements.
Set up the environment variables for OpenAI and Firebase credentials.
Start the Flask application: python3 app.py
The application will run in debug mode, accessible at http://127.0.0.1:5000.