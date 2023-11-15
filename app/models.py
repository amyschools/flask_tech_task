import enum
from sqlalchemy import Enum

from app import db


class Status(enum.Enum):
    """
    Possible states for file objects
    """

    PENDING = 1
    IN_PROGRESS = 2
    UPLOADED = 3
    ERROR = 4
    DELETED = 5


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    s3_url = db.Column(db.String(255), unique=False, nullable=True)
    status = db.Column(
        Enum(Status), nullable=False, default=Status.PENDING
    )
