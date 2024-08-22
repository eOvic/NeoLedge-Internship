from extensions import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename
        }
