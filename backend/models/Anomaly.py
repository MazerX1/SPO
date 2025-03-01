from backend.extensions import db
class Anomaly(db.Model):
    __tablename__ = 'anomalies'

    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.Integer, db.ForeignKey('wells.id'))
    anomaly_type = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    norm_value = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    detected_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    well = db.relationship("Well", backref="anomalies")

    def __repr__(self):
        return f"<Anomaly {self.anomaly_type} on Well {self.well.name}>"