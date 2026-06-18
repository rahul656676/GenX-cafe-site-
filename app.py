from flask import Flask, send_from_directory
from config import Config
from models.db import close_db

from routes.public import public
from routes.auth import auth
from routes.admin import admin
from routes.chatbot import chatbot

import os

app = Flask(__name__)

app.config.from_object(Config)

# BLUEPRINTS

app.register_blueprint(public)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(chatbot)

# CLOSE DB

app.teardown_appcontext(close_db)

# UPLOADS ROUTE

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )

# RUN

if __name__ == '__main__':

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.run(debug=True)