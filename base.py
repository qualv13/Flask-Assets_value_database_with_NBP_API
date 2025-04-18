from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

LOCAL_TIMEZONE = pytz.timezone('Europe/Warsaw')


class Asset(db.Model): # Majątek
  __tablename__ = 'assets'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  value = db.Column(db.Integer, nullable=False)
  currency = db.Column(db.String(3), nullable=False)
  is_pln = db.Column(db.Boolean, default=False)
  time_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(LOCAL_TIMEZONE))
  time_updated = db.Column(db.DateTime(timezone=True), onupdate=lambda: datetime.now(LOCAL_TIMEZONE))


class Rate(db.Model):
    __tablename__ = 'rates'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), nullable=False)
    currency = db.Column(db.String(20), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
