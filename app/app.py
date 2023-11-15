from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes import upload, delete

app = Flask(__name__)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

app.add_url_rule("/upload", "upload", upload, methods=["POST"])
app.add_url_rule("/delete", "delete", delete, methods=["POST"])
