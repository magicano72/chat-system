from database import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50))
    recipient_id = db.Column(db.String(50))

    text = db.Column(db.Text, nullable=True)
    image_data = db.Column(db.LargeBinary, nullable=True)

    timestamp = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="sent")