from app import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    summary = db.Column(db.Text)

    def __repr__(self):
        return f"<Document {self.id}>"
