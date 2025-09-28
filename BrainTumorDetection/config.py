import os
from pathlib import Path

# Base configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'brain-tumor-detection-secret-key'
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / 'data'
    MODELS_DIR = BASE_DIR / 'models'
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    
    # Model configuration
    IMG_SIZE = (224, 224)
    BATCH_SIZE = 32
    EPOCHS = 50
    LEARNING_RATE = 0.001
    
    # Class names
    CLASS_NAMES = ['Glioma Tumor', 'Meningioma Tumor', 'No Tumor', 'Pituitary Tumor']
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///brain_tumor.db'
    
    # Flask configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}