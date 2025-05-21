from models.database import db

class MCCCode(db.Model):
    __tablename__ = "mcc_codes"

    code = db.Column(db.String(10), primary_key=True)
    description = db.Column(db.String(255), nullable=False)