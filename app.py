from flask import Flask, render_template, request, jsonify # type: ignore
import google.generativeai as genai # type: ignore
import random
import requests # type: ignore
import os

# Configure your API key
GOOGLE_API_KEY = os.getenv("AIzaSyDm5-oAnXSijQczzp1lrddR_dUSnp46Fj8")  # Replace with your actual API key
genai.configure(api_key="AIzaSyDm5-oAnXSijQczzp1lrddR_dUSnp46Fj8")
app = Flask(__name__)

# Python function to analyze symptoms
def analyze_symptoms(symptoms):
    """Analyze symptoms using Gemini 2.0 Flash and return response"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""Analyze the following health symptoms described by a user and:
    1. Identify the most likely disease/condition
    2. Provide a short description of the disease/condition.
    3. List precautions in bullet points.
    4. Use very simple language and avoid medical jargons.
    
    Symptoms: {symptoms}
    
    Please format your response as:
    Disease: [Perfect Disease name]
    Description: [Brief description of the disease]
    Precautions:
    • [First precaution]
    • [Second precaution]
    • ..."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to fetch daily medical news
def get_medical_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "health",
        "country": "us",
        "apiKey": "8c0946da9fe245f9929ec085b12e922b"  # Replace with an actual News API key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if articles:
            top_article = random.choice(articles)
            return top_article["title"], top_article["urlToImage"]
    return "No news available", "https://via.placeholder.com/400"

@app.route('/')
def home():
    news_title, news_image = get_medical_news()
    return render_template('index.html', news_title=news_title, news_image=news_image)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the New Chat page
@app.route('/new-chat')
def new_chat():
    return render_template('new_chat.html')

# Route to analyze symptoms
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    symptoms = data.get('symptoms', '')
    if not symptoms:
        return jsonify({'error': 'Symptoms are required'}), 400

    result = analyze_symptoms(symptoms)
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)
