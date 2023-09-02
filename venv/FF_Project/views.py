from flask import Flask,render_template,url_for,flash,redirect, request, Blueprint
from FF_Project import db
from FF_Project.models import FantastyFootball
from FF_Project.creds import lg_id,espn_s2,swid,year
import sqlite3
from espn_api.football import League
import pandas as pd
import os

core = Blueprint('core',__name__)

@core.route('/')
def standings():
    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
    conn.row_factory = sqlite3.Row
    stand = conn.execute("WITH "
                     "a AS "
                     "(SELECT team_name, SUM(points_scored) AS Total_Points_Scored, SUM(points_against) AS Total_Points_Against, AVG(mov) AS AVG_MOV "
                     "FROM fantasyfootballdata "
                     f"WHERE season = {year} "
                     "GROUP BY team_name), "
                     ""
                     "b AS "
                     "(SELECT team_name, COUNT(mov) AS wins "
                     "FROM fantasyfootballdata "
                     "WHERE mov > 0 "
                     f"AND season = {year} "
                     "GROUP BY team_name "
                     "ORDER BY wins DESC), "
                     ""
                     "c AS "
                     "(SELECT team_name, COUNT(mov) AS losses "
                     "FROM fantasyfootballdata "
                     "WHERE mov < 0 "
                     f"AND season = {year} "
                     "GROUP BY team_name "
                     "ORDER BY losses DESC) "
                     ""
                     ""
                     "SELECT a.team_name, b.wins, c.losses, a.Total_Points_Scored, a.Total_Points_Against, a.AVG_MOV "
                     ""
                     "FROM a "
                     ""
                     "LEFT JOIN b AS b ON b.team_name = a.team_name "
                     "LEFT JOIN c AS c ON c.team_name = a.team_name "
                     ""
                     "ORDER BY b.wins DESC, a.Total_Points_Scored DESC ").fetchall()
    conn.close()
    return render_template('standings.html', stand=stand)

@core.route('/alldata')
def all_data():
    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
    conn.row_factory = sqlite3.Row
    items = conn.execute('SELECT * FROM fantasyfootballdata').fetchall()
    conn.close()
    return render_template('weekly_data.html', items=items)

@core.route('/badluckindex')
def bad_luck_index():

    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
    conn.row_factory = sqlite3.Row
    bad_luck = conn.execute(""
                         "SELECT a.team_name AS team_name, ROUND(SUM((b.average_points_scored - a.points_against)),2) AS total_luck_index "
                         "FROM fantasyfootballdata a "
                         "LEFT JOIN "
                         "(SELECT team_name, AVG(points_scored) AS average_points_scored "
                         "FROM fantasyfootballdata "
                         "GROUP BY team_name "
                         "ORDER BY average_points_scored) AS b "
                         "ON a.opponent = b.team_name "
                         f"WHERE season = {year} "
                         "GROUP BY a.team_name "
                         "ORDER BY total_luck_index DESC;").fetchall()
    conn.close()

    return render_template('bad_luck_index.html', bad_luck=bad_luck)
@core.route('/graph')
def graph():
    pass
@core.route('/<id>')
def player_profile(id):

    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
    conn.row_factory = sqlite3.Row

    #gets team id for url
    team_id = FantastyFootball.query.filter_by(id=id)

    team_id_name = conn.execute(f"SELECT team_name FROM roster WHERE team_id = {id}").fetchone()

    #roster
    roster = conn.execute(f"SELECT * FROM roster WHERE team_id = {id}").fetchall()

    conn.close()

    # current week

    #biggest blowout

    #biggest lose

    return render_template('player_profile.html', team_id_name=team_id_name, team_id=team_id, roster=roster)
@core.route('/trade_activity')
def trade_activity():
    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
    conn.row_factory = sqlite3.Row
    items = conn.execute(f"SELECT * FROM activity WHERE season = {year}").fetchall()
    conn.close()
    return render_template('trade_activity.html', items=items)
@core.route('/side_bets')
def side_bets():
    pass


    

