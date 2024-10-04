# Chatbot-AristAI
Chatbot AristAI is a Flask web application that integrates with OpenAI's GPT model to answer user questions. The application also uses Firebase Firestore for storing chat history, and it is deployed to AWS Lambda using Zappa.

**Features**

Ask questions and get intelligent responses from OpenAI's GPT-3.5 Turbo model.
Store and retrieve chat history in Google Firebase Firestore.
Scalable, serverless deployment on AWS using Lambda and API Gateway.

**Requirements**

- Python (3.9)
- AWS CLI
- Zappa
- OpenAI API Key
- Firebase Admin SDK credentials

**How to interact with the applicatoin**

You can access the app via: https://p7np3y6vt3.execute-api.us-east-1.amazonaws.com/dev
- Ask a Question:
Type your question into the input text box and press the "Ask" button. The chatbot will respond using OpenAI's GPT-3.5 Turbo model.
- View the Response:
The answer will appear directly below the input box after processing.
- Chat History:
Click on the "Chat History" button to view a log of previous questions and answers stored in Firebase Firestore.