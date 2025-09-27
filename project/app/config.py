import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-demo'
    
    # Use absolute path for database to avoid working directory issues
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Get the project root directory (where this config.py is located)
        basedir = os.path.abspath(os.path.dirname(__file__))
        project_dir = os.path.dirname(basedir)  # Go up one level from app/ to project/
        instance_dir = os.path.join(project_dir, 'instance')
        db_path = os.path.join(instance_dir, 'medgen.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload