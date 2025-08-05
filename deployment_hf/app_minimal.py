from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Simple disease prediction without pandas
def predict_disease_simple(symptoms_text):
    """Simple disease prediction using keyword matching"""
    symptoms = symptoms_text.lower().split(',')
    symptoms = [s.strip() for s in symptoms]
    
    # Simple keyword-based disease prediction
    disease_mapping = {
        'fever': ['Common Cold', 'Flu', 'COVID-19'],
        'headache': ['Migraine', 'Tension Headache', 'Sinusitis'],
        'fatigue': ['Anemia', 'Depression', 'Chronic Fatigue Syndrome'],
        'cough': ['Bronchitis', 'Pneumonia', 'Common Cold'],
        'nausea': ['Gastritis', 'Food Poisoning', 'Migraine'],
        'dizziness': ['Vertigo', 'Low Blood Pressure', 'Anxiety'],
        'chest pain': ['Angina', 'Heart Attack', 'Costochondritis'],
        'shortness of breath': ['Asthma', 'Pneumonia', 'Anxiety'],
        'joint pain': ['Arthritis', 'Fibromyalgia', 'Lupus'],
        'back pain': ['Muscle Strain', 'Herniated Disc', 'Kidney Stones']
    }
    
    possible_diseases = set()
    for symptom in symptoms:
        if symptom in disease_mapping:
            possible_diseases.update(disease_mapping[symptom])
    
    if possible_diseases:
        return "Possible conditions:\n" + "\n".join([f"• {disease}" for disease in list(possible_diseases)[:3]])
    else:
        return "No specific conditions identified. Please consult a healthcare professional for accurate diagnosis."

def answer_medical_question(question):
    """Answer medical questions using keyword matching"""
    question_lower = question.lower()
    
    # Simple response logic based on keywords
    if 'diabetes' in question_lower:
        return "Diabetes is a chronic condition that affects how your body turns food into energy. There are two main types: Type 1 and Type 2. Management includes diet, exercise, and medication."
    elif 'heart' in question_lower or 'cardiac' in question_lower:
        return "Heart disease refers to various conditions affecting the heart. Common types include coronary artery disease, heart failure, and arrhythmias. Prevention includes healthy lifestyle choices."
    elif 'cancer' in question_lower:
        return "Cancer is a group of diseases characterized by uncontrolled cell growth. Early detection and treatment are crucial. Regular screenings and healthy lifestyle can help prevent many types."
    elif 'fever' in question_lower:
        return "Fever is often a sign of infection. Rest, fluids, and over-the-counter medications can help. Seek medical attention if fever is high or persistent."
    elif 'headache' in question_lower:
        return "Headaches can have many causes including stress, dehydration, or underlying conditions. Rest, hydration, and pain relievers often help. See a doctor if severe or frequent."
    elif 'covid' in question_lower:
        return "COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. Symptoms include fever, cough, fatigue, and loss of taste/smell. Vaccination and good hygiene help prevent infection."
    elif 'blood pressure' in question_lower:
        return "Blood pressure is the force of blood against artery walls. High blood pressure (hypertension) can lead to heart disease and stroke. Regular monitoring and lifestyle changes are important."
    else:
        return "I understand your medical question. For accurate medical advice, please consult with a healthcare professional. This system is for informational purposes only."

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HealifyAI - Healthcare Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            input[type="text"], textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            button { background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #2980b9; }
            .result { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; white-space: pre-line; }
            .disclaimer { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin-top: 20px; }
            .success { color: #27ae60; }
            .error { color: #e74c3c; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 HealifyAI - Healthcare Assistant</h1>
            
            <div class="section">
                <h2>🔍 Disease Prediction</h2>
                <form id="diseaseForm">
                    <label for="symptoms">Enter symptoms (comma-separated):</label><br>
                    <textarea id="symptoms" name="symptoms" rows="3" placeholder="e.g., fever, headache, fatigue"></textarea><br>
                    <button type="submit">🔬 Predict Disease</button>
                </form>
                <div id="diseaseResult" class="result" style="display:none;"></div>
            </div>
            
            <div class="section">
                <h2>❓ Medical Q&A</h2>
                <form id="qaForm">
                    <label for="question">Ask a medical question:</label><br>
                    <textarea id="question" name="question" rows="3" placeholder="e.g., What are the symptoms of diabetes?"></textarea><br>
                    <button type="submit">💡 Get Answer</button>
                </form>
                <div id="qaResult" class="result" style="display:none;"></div>
            </div>
            
            <div class="disclaimer">
                <strong>⚠️ Important Disclaimer:</strong> This system is for informational purposes only and should not replace professional medical advice. Always consult with a healthcare professional for medical concerns.
            </div>
        </div>
        
        <script>
            document.getElementById('diseaseForm').onsubmit = function(e) {
                e.preventDefault();
                const symptoms = document.getElementById('symptoms').value;
                fetch('/predict_disease', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({symptoms: symptoms})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('diseaseResult').innerHTML = data.result;
                    document.getElementById('diseaseResult').style.display = 'block';
                });
            };
            
            document.getElementById('qaForm').onsubmit = function(e) {
                e.preventDefault();
                const question = document.getElementById('question').value;
                fetch('/answer_question', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: question})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('qaResult').innerHTML = data.result;
                    document.getElementById('qaResult').style.display = 'block';
                });
            };
        </script>
    </body>
    </html>
    '''

@app.route('/predict_disease', methods=['POST'])
def predict_disease_api():
    data = request.get_json()
    symptoms = data.get('symptoms', '')
    result = predict_disease_simple(symptoms)
    return jsonify({'result': result})

@app.route('/answer_question', methods=['POST'])
def answer_question_api():
    data = request.get_json()
    question = data.get('question', '')
    result = answer_medical_question(question)
    return jsonify({'result': result})

if __name__ == '__main__':
    print("🚀 Starting HealifyAI Healthcare Assistant...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⚠️  This system is for informational purposes only.")
    print("   Always consult healthcare professionals for medical advice.")
    app.run(debug=True, host='0.0.0.0', port=5000) 