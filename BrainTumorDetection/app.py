"""
Flask web application for brain tumor detection
Provides web interface for image upload and prediction
"""

import os
import cv2
import numpy as np
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import tensorflow as tf
from datetime import datetime
import logging
from config import Config, config
from database import db, Patient, Prediction
from src.utils import allowed_file, preprocess_image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Create directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODELS_DIR'], exist_ok=True)
    
    return app

app = create_app()

# Load trained model
model = None
try:
    model_path = os.path.join(app.config['MODELS_DIR'], 'brain_tumor_model.h5')
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        logger.info("Model loaded successfully")
    else:
        logger.warning("Model file not found. Please train the model first.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Upload page"""
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Preprocess image
            processed_image = preprocess_image(filepath, app.config['IMG_SIZE'])
            
            # Make prediction
            if model:
                prediction = model.predict(np.expand_dims(processed_image, axis=0))
                predicted_class = int(np.argmax(prediction))
                confidence = float(prediction[0][predicted_class])
                
                # Save prediction to database
                patient_name = request.form.get('patient_name', 'Unknown')
                patient_email = request.form.get('patient_email', '')
                
                patient = Patient(name=patient_name, email=patient_email)
                db.session.add(patient)
                db.session.flush()
                
                pred_record = Prediction(
                    patient_id=patient.id,
                    image_path=filepath,
                    predicted_class=predicted_class,
                    confidence=confidence,
                    prediction_date=datetime.utcnow()
                )
                db.session.add(pred_record)
                db.session.commit()
                
                result = {
                    'success': True,
                    'prediction': app.config['CLASS_NAMES'][predicted_class],
                    'confidence': f"{confidence*100:.2f}%",
                    'image_path': filepath,
                    'prediction_id': pred_record.id
                }
                
                return jsonify(result)
            else:
                return jsonify({'error': 'Model not loaded'})
                
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return jsonify({'error': f'Error processing image: {str(e)}'})
    else:
        return jsonify({'error': 'Invalid file type'})

@app.route('/results/<int:prediction_id>')
def view_result(prediction_id):
    """View prediction result"""
    prediction = Prediction.query.get_or_404(prediction_id)
    return render_template('result.html', prediction=prediction)

@app.route('/api/predictions')
def get_predictions():
    """Get all predictions (API endpoint)"""
    predictions = Prediction.query.order_by(Prediction.prediction_date.desc()).all()
    result = []
    for pred in predictions:
        result.append({
            'id': pred.id,
            'patient_name': pred.patient.name,
            'prediction': app.config['CLASS_NAMES'][pred.predicted_class],
            'confidence': pred.confidence,
            'date': pred.prediction_date.isoformat()
        })
    return jsonify(result)

@app.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    total_predictions = Prediction.query.count()
    total_patients = Patient.query.count()
    
    # Get recent predictions
    recent_predictions = Prediction.query.order_by(
        Prediction.prediction_date.desc()
    ).limit(10).all()
    
    # Get class distribution
    class_counts = {}
    for i, class_name in enumerate(app.config['CLASS_NAMES']):
        count = Prediction.query.filter_by(predicted_class=i).count()
        class_counts[class_name] = count
    
    return render_template('dashboard.html', 
                         total_predictions=total_predictions,
                         total_patients=total_patients,
                         recent_predictions=recent_predictions,
                         class_counts=class_counts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

