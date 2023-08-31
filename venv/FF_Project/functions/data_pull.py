import datetime
import pandas as pd
from FF_Project import app, db
from FF_Project.models import FantastyFootball, Activity_Tracker
import sqlite3
from espn_api.football import League

class DataPulls():
    def __init__(self,league_id,league_year,espn_s2,swid,standings_data=None,activity_data=None, activity_amount=1000):
        self.league_id=league_id
        self.league_year=league_year
        self.espn_s2=espn_s2
        self.swid=swid
        self.standings_data=standings_data
        self.activity_data=activity_data
        self.activity_amount=activity_amount

    def standings_pull(self):
        league = League(self.league_id, self.league_year,self.espn_s2,self.swid)

        # pulls down data and actually creates/populates all data table
        for i in league.teams:
            for x in range(0, len(i.scores)):
                for y in league.scoreboard(week=(x + 1)):
                    season = self.league_year
                    team = i.team_name
                    week = x + 1
                    points_scored = i.scores[x]
                    points_against = round(i.scores[x] - i.mov[x], 2)
                    mov = round(i.mov[x], 2)

                    if i.team_name == y.home_team.team_name:
                        opponent = y.away_team.team_name
                        self.standings_data = FantastyFootball(season=season,
                                                               team_name=team,
                                                               opponent=opponent,
                                                               week=week,
                                                               points_scored=points_scored,
                                                               points_against=points_against,
                                                               mov=mov)

                        self.db_standings_commit(season, team, opponent, week, points_scored, points_against, mov)

                    elif i.team_name == y.away_team.team_name:
                        opponent = y.home_team.team_name
                        self.standings_data = FantastyFootball(season=season,
                                                               team_name=team,
                                                               opponent=opponent,
                                                               week=week,
                                                               points_scored=points_scored,
                                                               points_against=points_against,
                                                               mov=mov)
                        self.db_standings_commit(season,team,opponent,week,points_scored,points_against,mov)


    def db_standings_commit(self,season,team,opponent,week,points_scored,points_against,mov):
        # check to make sure we don't add duplicated rows. Need to find more efficient way to handle
        conn = sqlite3.connect(
            'C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
        conn.row_factory = sqlite3.Row
        exists = conn.execute("SELECT * "
                              "FROM fantasyfootballdata "
                              "WHERE season=? "
                              "AND team_name=? "
                              "AND opponent=?"
                              "AND week=? "
                              "AND points_scored=? "
                              "AND points_against=? "
                              "AND mov=?", (season, team, opponent, week, points_scored, points_against,
                                            mov,)).fetchone() is not None
        conn.close()

        if exists == True:
            pass
        else:
            db.session.add(self.standings_data)
            db.session.commit()
    
    def activity_pull(self):
        league = League(self.league_id, self.league_year,self.espn_s2,self.swid)

        activity = league.recent_activity(size=self.activity_amount)
        activity_len = len(activity)

        a_list = []
        
        for i in range(0,(activity_len)):
            data_activity = activity[i]
            a = data_activity.actions
            a_len = len(a)
            for x in range(0,(a_len)):
                season = self.league_year
                team_name = str(a[x][0])
                action_taken = a[x][1]
                player_name = str(a[x][2])
                readable_date = datetime.datetime.fromtimestamp(data_activity.date / 1000).strftime('%m-%d-%Y %H:%M:%S')
                self.activity_data = Activity_Tracker(season=season,team_name=team_name,action_taken=action_taken,player_name=player_name, readable_date=readable_date)
                self.db_activity_commit(season,team_name,action_taken,player_name,readable_date)

    def db_activity_commit(self,season,team_name,action_taken,player_name,readable_date):
        # check to make sure we don't add duplicated rows. Need to find more efficient way to handle
        conn = sqlite3.connect(
            'C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
        conn.row_factory = sqlite3.Row
        exists = conn.execute("SELECT * "
                              "FROM activity "
                              "WHERE season=? "
                              "AND team_name=? "
                              "AND action_taken=? "
                              "AND player_name=? "
                              "AND readable_date=?", (season,team_name, action_taken, player_name, readable_date, )).fetchone() is not None
        conn.close()

        if exists == True:
            pass
        else:
            db.session.add(self.activity_data)
            db.session.commit()
