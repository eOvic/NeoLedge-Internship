from datetime import datetime
from extensions import db  # Import db from extensions.py

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.title = title

    def __repr__(self):
        return f'<Task id: {self.id} - {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date.isoformat() if self.date else None,
            'completed': self.completed
        }
