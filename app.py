from flask import Flask, render_template, request
import os 
import numpy as np
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route('/train', methods=['GET'])
def training():
    os.system("python main.py")
    return "Training Successful!" 

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            # Get all input values
            features = [
                'fixed_acidity', 'volatile_acidity', 'citric_acid',
                'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
                'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol'
            ]
            
            # Convert to float and handle missing values
            data = []
            for feature in features:
                value = request.form.get(feature)
                if not value:
                    return f"Missing value for {feature}", 400
                try:
                    data.append(float(value))
                except ValueError:
                    return f"Invalid number for {feature}: {value}", 400
            
            # Reshape and predict
            data = np.array(data).reshape(1, -1)
            predictor = PredictionPipeline()
            prediction = predictor.predict(data)
            
            return render_template('results.html', prediction=str(round(prediction, 2)))
            
        except Exception as e:
            return render_template('error.html', error_message=str(e))
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # Enable debug mode