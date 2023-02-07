from FF_Project import db
from flask import Blueprint

data = Blueprint('data',__name__)

######################################################
### Schema ###########################################
######################################################

class FantastyFootball(db.Model):

    __tablename__ = 'fantasyfootballdata'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.Text)
    opponent = db.Column(db.Text)
    week = db.Column(db.Integer)
    points_scored = db.Column(db.REAL)
    points_against = db.Column(db.REAL)
    mov = db.Column(db.REAL)

    def __init__(self, team_name, opponent, week, points_scored, points_against, mov):
        self.team_name = team_name
        self.opponent = opponent
        self.week = week
        self.points_scored = points_scored
        self.points_against = points_against
        self.mov = mov

class BadLuckIndex(db.Model):

    __tablename__ = 'badluckindex'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.Text)
    bad_luck_index = db.Column(db.REAL)