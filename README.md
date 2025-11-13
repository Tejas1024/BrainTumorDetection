# Brain Tumor Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10.0-orange.svg)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered web application for automated brain tumor detection and classification using deep learning. This system analyzes MRI brain scans and classifies them into four categories: Glioma, Meningioma, Pituitary tumors, or No Tumor.

## 🎯 Features

- **AI-Powered Detection**: CNN-based deep learning model for accurate tumor classification
- **Multi-Class Classification**: Detects 4 types - Glioma, Meningioma, Pituitary tumors, and No Tumor
- **Web Interface**: User-friendly Flask web application for easy image upload and analysis
- **Real-time Predictions**: Instant analysis with confidence scores
- **Patient Management**: Database system to track patients and prediction history
- **Dashboard Analytics**: Visual insights into prediction statistics and trends
- **RESTful API**: Programmatic access to prediction endpoints
- **Image Preprocessing**: Automated image enhancement and normalization
- **Secure File Handling**: Safe image upload with validation and sanitization

## 📋 Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Model Training](#model-training)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- 4GB+ RAM (8GB recommended for training)
- GPU support optional (CUDA for faster training)

### Method 1: Using pip (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/brain-tumor-detection.git
cd brain-tumor-detection
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup the application**
```bash
# Create necessary directories
mkdir -p data/training data/testing models static/uploads

# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Method 2: Using Conda

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/brain-tumor-detection.git
cd brain-tumor-detection
```

2. **Create conda environment**
```bash
conda env create -f environment.yml
conda activate brain-tumor-detection
```

### Method 3: Using Docker

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
BrainTumorDetection/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── database.py                 # Database models
├── train_model.py             # Model training script
├── requirements.txt            # Python dependencies
├── environment.yml             # Conda environment file
├── setup.py                    # Package setup configuration
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
│
├── src/                        # Source code modules
│   ├── __init__.py
│   ├── cnn_model.py           # CNN model architecture
│   ├── data_preprocessing.py  # Data preprocessing utilities
│   ├── model_evaluation.py    # Model evaluation metrics
│   └── utils.py               # Helper functions
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── main.js            # JavaScript functionality
│   └── uploads/               # Uploaded images directory
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── upload.html            # Upload page
│   ├── result.html            # Results display
│   └── dashboard.html         # Admin dashboard
│
├── data/                       # Dataset directory
│   ├── training/              # Training images
│   │   ├── glioma/
│   │   ├── meningioma/
│   │   ├── notumor/
│   │   └── pituitary/
│   └── testing/               # Testing images
│
├── models/                     # Saved models
│   └── brain_tumor_model.h5   # Trained model
│
├── notebooks/                  # Jupyter notebooks
│   ├── data_exploration.ipynb
│   └── model_training.ipynb
│
└── tests/                      # Unit tests
    ├── __init__.py
    ├── test_preprocessing.py
    └── test_model.py
```

## 💻 Usage

### Running the Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Access the web interface**
- Open your browser and navigate to `http://localhost:5000`
- Upload an MRI brain scan image
- Enter patient information
- Click "Analyze MRI Image"
- View prediction results with confidence scores

### Using the Dashboard

Access the admin dashboard at `http://localhost:5000/dashboard` to view:
- Total predictions and patients
- Recent prediction history
- Class distribution statistics
- Visual analytics

## 🧠 Model Training

### Preparing the Dataset

1. **Organize your dataset**
```
data/
├── training/
│   ├── glioma/          # Glioma tumor images
│   ├── meningioma/      # Meningioma tumor images
│   ├── notumor/         # No tumor images
│   └── pituitary/       # Pituitary tumor images
└── testing/
    ├── glioma/
    ├── meningioma/
    ├── notumor/
    └── pituitary/
```

2. **Train the model**
```bash
python train_model.py
```

### Training Configuration

Modify `config.py` to adjust training parameters:

```python
IMG_SIZE = (224, 224)      # Input image size
BATCH_SIZE = 32            # Batch size for training
EPOCHS = 50                # Number of training epochs
LEARNING_RATE = 0.001      # Learning rate
```

### Model Architecture

The CNN model includes:
- Convolutional layers with ReLU activation
- Max pooling layers
- Batch normalization
- Dropout for regularization
- Dense layers for classification
- Softmax output for 4 classes

## 📡 API Documentation

### Prediction Endpoint

**POST** `/predict`

Upload an image and get tumor classification prediction.

**Request:**
```bash
curl -X POST -F "file=@mri_scan.jpg" \
     -F "patient_name=John Doe" \
     -F "patient_email=john@example.com" \
     http://localhost:5000/predict
```

**Response:**
```json
{
  "success": true,
  "prediction": "Glioma Tumor",
  "confidence": "95.67%",
  "image_path": "static/uploads/20241113_153045_mri_scan.jpg",
  "prediction_id": 123
}
```

### Get All Predictions

**GET** `/api/predictions`

Retrieve all prediction records.

**Response:**
```json
[
  {
    "id": 123,
    "patient_name": "John Doe",
    "prediction": "Glioma Tumor",
    "confidence": 0.9567,
    "date": "2024-11-13T15:30:45"
  }
]
```

### View Specific Result

**GET** `/results/<prediction_id>`

View detailed results for a specific prediction.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///brain_tumor.db
FLASK_ENV=development
FLASK_DEBUG=1
```

### Application Configuration

Edit `config.py` for application settings:

```python
# Development
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///brain_tumor.db'

# Production
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- GIF (.gif)

Maximum file size: 16MB

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_preprocessing.py
```

### Manual Testing

1. Test image upload functionality
2. Verify prediction accuracy
3. Check database operations
4. Validate API endpoints
5. Test dashboard analytics

## 🚢 Deployment

### Production Deployment

1. **Set production environment**
```bash
export FLASK_ENV=production
```

2. **Use a production server (Gunicorn)**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Configure reverse proxy (Nginx)**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Deployment

```bash
# Build image
docker build -t brain-tumor-detection .

# Run container
docker run -p 5000:5000 brain-tumor-detection
```

### Cloud Deployment Options

- **Heroku**: Use provided `Procfile`
- **AWS EC2**: Deploy with Nginx + Gunicorn
- **Google Cloud Run**: Containerized deployment
- **Azure Web Apps**: Python web app service

## 📊 Model Performance

Expected performance metrics:
- **Accuracy**: 92-95%
- **Precision**: 90-94%
- **Recall**: 91-95%
- **F1-Score**: 91-94%

Note: Performance may vary based on dataset quality and size.

## 🔒 Security Considerations

- File upload validation and sanitization
- Secure filename handling
- SQL injection prevention (SQLAlchemy ORM)
- CSRF protection (Flask-WTF)
- Input validation on all forms
- Secure session management
- Environment variable configuration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation as needed
- Use descriptive commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- TensorFlow and Keras teams for deep learning frameworks
- Flask community for the web framework
- Medical imaging datasets providers
- Open-source contributors

## 📞 Support

For support and questions:
- Email: your.email@example.com
- Issues: [GitHub Issues](https://github.com/yourusername/brain-tumor-detection/issues)
- Documentation: [Project Wiki](https://github.com/yourusername/brain-tumor-detection/wiki)

## ⚠️ Disclaimer

This system is intended for research and educational purposes only. It should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for medical decisions.

## 🔄 Version History

- **v1.0.0** (2024-11-13)
  - Initial release
  - CNN model implementation
  - Web interface
  - Database integration
  - API endpoints

## 🗺️ Roadmap

- [ ] Add ensemble model support
- [ ] Implement explainable AI (Grad-CAM visualization)
- [ ] Multi-language support
- [ ] Mobile application
- [ ] DICOM format support
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Integration with PACS systems

---

**Made with ❤️ for advancing medical AI technology**
