from FF_Project import app, db
from flask import render_template
from FF_Project.models import FantastyFootball
import sqlite3
from espn_api.football import League

@app.before_first_request
def create_tables():
    db.create_all()

    league_id = 608256606
    league_year = 2022

    league = League(league_id, league_year)

    for i in league.teams:
        for x in range(0, len(i.scores)):
            for y in league.scoreboard(week=(x + 1)):

                team = i.team_name
                week = x + 1
                points_scored = i.scores[x]
                points_against = round(i.scores[x] - i.mov[x], 2)
                mov = round(i.mov[x], 2)

                if i.team_name == y.home_team.team_name:
                    opponent = y.away_team.team_name
                    data_input = FantastyFootball(team_name=team, opponent=opponent, week=week,
                                                  points_scored=points_scored,
                                                  points_against=points_against, mov=mov)

                    # check to make sure we don't add duplicated rows. Need to find more efficient way to handle
                    conn = sqlite3.connect(
                        'C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
                    conn.row_factory = sqlite3.Row
                    exists = conn.execute("SELECT * "
                                          "FROM fantasyfootballdata "
                                          "WHERE team_name=? "
                                          "AND opponent=?"
                                          "AND week=? "
                                          "AND points_scored=? "
                                          "AND points_against=? "
                                          "AND mov=?", (team, opponent, week, points_scored, points_against,
                                                        mov,)).fetchone() is not None
                    conn.close()

                    if exists == True:
                        pass
                    else:
                        db.session.add(data_input)
                        db.session.commit()

                elif i.team_name == y.away_team.team_name:
                    opponent = y.home_team.team_name
                    data_input = FantastyFootball(team_name=team, opponent=opponent, week=week, points_scored=points_scored,
                                                  points_against=points_against, mov=mov)

                    # check to make sure we don't add duplicated rows. Need to find more efficient way to handle
                    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
                    conn.row_factory = sqlite3.Row
                    exists = conn.execute("SELECT * "
                                          "FROM fantasyfootballdata "
                                          "WHERE team_name=? "
                                          "AND opponent=?"
                                          "AND week=? "
                                          "AND points_scored=? "
                                          "AND points_against=? "
                                          "AND mov=?",
                                          (team, opponent, week, points_scored, points_against, mov,)).fetchone() is not None
                    conn.close()

                    if exists == True:
                        pass
                    else:
                        db.session.add(data_input)
                        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)