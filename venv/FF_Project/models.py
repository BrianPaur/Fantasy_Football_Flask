from FF_Project import db
from flask import Blueprint

data = Blueprint('data',__name__)

######################################################
### Schema ###########################################
######################################################

class FantastyFootball(db.Model):

    __tablename__ = 'fantasyfootballdata'

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    team_name = db.Column(db.Text)
    opponent = db.Column(db.Text)
    week = db.Column(db.Integer)
    points_scored = db.Column(db.REAL)
    points_against = db.Column(db.REAL)
    mov = db.Column(db.REAL)

    def __init__(self, season, team_name, opponent, week, points_scored, points_against, mov):
        self.season = season
        self.team_name = team_name
        self.opponent = opponent
        self.week = week
        self.points_scored = points_scored
        self.points_against = points_against
        self.mov = mov

class Activity_Tracker(db.Model):

    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    team_name = db.Column(db.Text)
    action_taken = db.Column(db.Text)
    player_name = db.Column(db.Text)
    readable_date = db.Column(db.Text)

    def __init__(self, season, team_name, action_taken, player_name, readable_date):
        self.season = season
        self.team_name = team_name
        self.action_taken = action_taken
        self.player_name = player_name
        self.readable_date = readable_date

class Roster(db.Model):

    __tablename__ = 'roster'

    id = db.Column(db.Integer, primary_key=True)
    team_abbr = db.Column(db.Text)
    team_name = db.Column(db.Text)
    team_id = db.Column(db.Integer)
    player_id = db.Column(db.Integer)
    player_name = db.Column(db.Text)
    position = db.Column(db.Text)
    position_ranking = db.Column(db.Integer)
    injury_status = db.Column(db.Text)
    acquisition_type = db.Column(db.Text)
    acquisition_date = db.Column(db.Text)

    def __init__(self, team_abbr,team_name,team_id,player_id,player_name,position,position_ranking,injury_status,acquisition_type,acquisition_date):
        self.team_abbr = team_abbr
        self.team_name = team_name
        self.team_id = team_id
        self.player_id = player_id
        self.player_name = player_name
        self.position = position
        self.position_ranking=position_ranking
        self.injury_status=injury_status
        self.acquisition_type=acquisition_type
        self.acquisition_date=acquisition_date
