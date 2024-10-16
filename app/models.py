from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_instance = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    content = db.Column(db.Text, nullable=True)
    file_url = db.Column(db.String(255), nullable=True)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)

    client = db.relationship('Client', backref=db.backref('notifications', lazy=True))
