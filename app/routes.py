from flask import request
from http import HTTPStatus

from app import db
from models import File, Status
from utils import upload_file, delete_file, notify_preprocessor


def upload():
    """
    Upload the file to s3, and create a new object in the database. When
    upload is complete, send a notification to the preprocessor.
    """
    file = request.files["file"]
    new_file = File(name=file.filename, status=Status.IN_PROGRESS)
    db.session.add(new_file)
    db.session.commit()

    try:
        s3_url = upload_file(file)
        new_file.url = s3_url
        new_file.upload_status = Status.UPLOADED
        db.session.commit()

        notify_preprocessor(s3_url)

        return "Finished Uploading to s3, Notification Sent", HTTPStatus.OK

    except Exception as e:
        new_file.upload_status = Status.ERROR
        db.session.commit()
        return str(e), HTTPStatus.INTERNAL_SERVER_ERROR


def delete():
    """
    Delete a file from s3, but only if the status is "Done" or "Error". .
    """
    file = request.files["file"]
    existing = File.query.filter(File.filename == file.filename).one_or_none()

    if existing.UploadStatus in (Status.UPLOADED, Status.ERROR):
        try:
            delete_file(file)
            file.status = Status.DELETED
            db.session.commit()
            return HTTPStatus.OK

        except Exception as e:
            file.status = Status.ERROR
            db.session.commit()
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    return f"File upload status is: {existing.Status}. " \
           f"Upload status must be 'Done' or 'Error' to be deleted."

