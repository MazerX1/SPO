from backend.extensions import db

class Well(db.Model):
    __tablename__ = 'wells'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    flow_rate = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    last_maintenance = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Well {self.name}>"