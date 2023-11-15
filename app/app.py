from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes import upload, delete

app = Flask(__name__)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

app.add_url_rule("/upload", "upload", upload, methods=["POST"])
app.add_url_rule("/delete", "delete", delete, methods=["POST"])

# Todo - allow users to see the state of a requested file
# app.add_url_rule("/get/<file_id>", "get", view_file_state, methods=["GET"])
