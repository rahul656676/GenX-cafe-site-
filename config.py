import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = 'genxcafe-secret-key'

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Root@123'
    MYSQL_DB = 'genxcafe'

    GROQ_API_KEY = ''

    GROQ_MODEL = 'llama3-70b-8192'

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        'static/uploads'
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    WTF_CSRF_ENABLED = True

    ALLOWED_EXTENSIONS = {
        'png',
        'jpg',
        'jpeg',
        'gif',
        'webp'
    }