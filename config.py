import os 

class Config:
    
    # Add mysql database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:@localhost/todo' # Database configuration
    
    # Disable tracking modifications to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret kwy for CSRF Protection and session management 
    SECRET_KEY = os.environ.get('SECRET_KEY') or  "Thisismysecretkey"
    
    CKEDITOR_PKG_TYPE = 'standard'