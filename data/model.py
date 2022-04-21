

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
path = "sqlite:///{0}/data/data_kaiko.db".format(os.getcwd())
app.config['SQLALCHEMY_DATABASE_URI'] = path
db = SQLAlchemy(app)


class Quote(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    ts = db.Column(db.Integer)
    exchange = db.Column(db.String(10))
    mid_price = db.Column(db.Float)
    bid_volume0_1 = db.Column(db.Float)
    bid_volume0_2 = db.Column(db.Float)
    bid_volume0_3 = db.Column(db.Float)
    bid_volume0_4 = db.Column(db.Float)
    bid_volume0_5 = db.Column(db.Float)
    bid_volume0_6 = db.Column(db.Float)
    bid_volume0_7 = db.Column(db.Float)
    bid_volume0_8 = db.Column(db.Float)
    bid_volume0_9 = db.Column(db.Float)
    bid_volume1 = db.Column(db.Float)
    bid_volume1_5 = db.Column(db.Float)
    bid_volume2 = db.Column(db.Float)
    bid_volume4 = db.Column(db.Float)
    bid_volume6 = db.Column(db.Float)
    bid_volume8 = db.Column(db.Float)
    bid_volume10 = db.Column(db.Float)
    ask_volume0_1 = db.Column(db.Float)
    ask_volume0_2 = db.Column(db.Float)
    ask_volume0_3 = db.Column(db.Float)
    ask_volume0_4 = db.Column(db.Float)
    ask_volume0_5 = db.Column(db.Float)
    ask_volume0_6 = db.Column(db.Float)
    ask_volume0_7 = db.Column(db.Float)
    ask_volume0_8 = db.Column(db.Float)
    ask_volume0_9 = db.Column(db.Float)
    ask_volume1 = db.Column(db.Float)
    ask_volume1_5 = db.Column(db.Float)
    ask_volume2 = db.Column(db.Float)
    ask_volume4 = db.Column(db.Float)
    ask_volume6 = db.Column(db.Float)
    ask_volume8 = db.Column(db.Float)
    ask_volume10 = db.Column(db.Float)
