from flask import render_template,url_for,flash,redirect, Blueprint
from FF_Project import db
from FF_Project.models import FantastyFootball
import sqlite3
from espn_api.football import League
import pandas as pd

core = Blueprint('core',__name__)

@core.route('/')
def standings():
    conn = sqlite3.connect('C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite')
    conn.row_factory = sqlite3.Row
    stand = conn.execute("WITH "
                     "a AS "
                     "(SELECT team_name, SUM(points_scored) AS Total_Points_Scored, SUM(points_against) AS Total_Points_Against, AVG(mov) AS AVG_MOV "
                     "FROM fantasyfootballdata "
                     "GROUP BY team_name), "
                     ""
                     "b AS "
                     "(SELECT team_name, COUNT(mov) AS wins "
                     "FROM fantasyfootballdata "
                     "WHERE mov > 0 "
                     "GROUP BY team_name "
                     "ORDER BY wins DESC), "
                     ""
                     "c AS "
                     "(SELECT team_name, COUNT(mov) AS losses "
                     "FROM fantasyfootballdata "
                     "WHERE mov < 0 "
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
    bad_luck = conn.execute("SELECT a.team_name AS team_name, ROUND(SUM((a.points_against - b.average_points_scored)),2) AS total_luck_index "
                         "FROM fantasyfootballdata a "
                         "LEFT JOIN "
                         "(SELECT team_name, AVG(points_scored) AS average_points_scored "
                         "FROM fantasyfootballdata "
                         "GROUP BY team_name "
                         "ORDER BY average_points_scored) AS b "
                         "ON a.opponent = b.team_name "
                         "GROUP BY a.team_name "
                         "ORDER BY total_luck_index;").fetchall()
    conn.close()

    return render_template('bad_luck_index.html', bad_luck=bad_luck)
    

