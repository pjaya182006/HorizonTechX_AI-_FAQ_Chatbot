import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'saas-secret-crypto-hash-key-998822'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'chatbot.db')
    FAQ_JSON_PATH = os.path.join(BASE_DIR, 'data', 'faq.json')
    
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "Password123"  # Secure credentials setup
    
    CONFIDENCE_THRESHOLD = 0.35

    @staticmethod
    def init_app():
        os.makedirs(os.path.join(Config.BASE_DIR, 'database'), exist_ok=True)
        os.makedirs(os.path.join(Config.BASE_DIR, 'data'), exist_ok=True)