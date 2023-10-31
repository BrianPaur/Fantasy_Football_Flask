from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint
from FF_Project import db
from FF_Project.models import FantastyFootball
from FF_Project.creds import lg_id, espn_s2, swid, year
import sqlite3
from espn_api.football import League
import pandas as pd
import os

core = Blueprint("core", __name__)


@core.route("/", methods=["POST", "GET"])
def standings():
    conn = sqlite3.connect(
        "C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite"
    )
    conn.row_factory = sqlite3.Row
    stand = conn.execute(
        "SELECT team_name, abbrev, wins, losses, points_scored, points_against, mov "
        "FROM team_data "
        "ORDER BY wins DESC, points_scored DESC "
    ).fetchall()

    current_week = pd.read_sql_query(
        "SELECT (wins + losses) AS week "
        "FROM team_data", conn)['week'].iloc[0]

    conn.close()

    return render_template("standings.html", stand=stand, current_week=current_week)

@core.route("/alldata")
def all_data():
    conn = sqlite3.connect(
        "C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite"
    )
    conn.row_factory = sqlite3.Row
    items = conn.execute("SELECT * FROM fantasyfootballdata").fetchall()
    conn.close()
    return render_template("weekly_data.html", items=items)


@core.route("/badluckindex")
def bad_luck_index():
    conn = sqlite3.connect(
        "C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite"
    )
    conn.row_factory = sqlite3.Row
    bad_luck = conn.execute(
        ""
        "SELECT a.team_name AS team_name, c.team_abbr AS team_abbr, ROUND(SUM((b.average_points_scored - a.points_against)),2) AS total_luck_index "
        "FROM fantasyfootballdata a "
        ""
        ""
        "LEFT JOIN "
        "(SELECT team_name, AVG(points_scored) AS average_points_scored "
        "FROM fantasyfootballdata "
        f"WHERE season = {year} "
        "GROUP BY team_name "
        "ORDER BY average_points_scored) AS b "
        "ON a.opponent = b.team_name "
        ""
        "LEFT JOIN "
        "(SELECT DISTINCT team_id,team_abbr,team_name FROM roster) AS c "
        "ON a.team_name = c.team_name "
        ""
        f"WHERE season = {year} "
        "GROUP BY a.team_name "
        "ORDER BY total_luck_index DESC; "
    ).fetchall()
    conn.close()

    return render_template("bad_luck_index.html", bad_luck=bad_luck)


@core.route("/graph")
def graph():
    pass

@core.route("/<abbrev>")
def player_profile(abbrev):
    conn = sqlite3.connect(
        "C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite"
    )
    conn.row_factory = sqlite3.Row

    team_id_name = conn.execute(
        f"SELECT team_name FROM roster WHERE team_abbr = '{abbrev}'"
    ).fetchone()
    
    logo = conn.execute(
        f"SELECT logo FROM team_data WHERE abbrev = '{abbrev}'"
    ).fetchone()
    
    team_info = conn.execute(
        f" Select streak_length, streak_type, acquisitions, drops, trades, waiverRank "
        f"from team_data "
        f"WHERE abbrev = '{abbrev}'"
        ).fetchone()

    # roster
    roster = conn.execute(
        f"SELECT * FROM roster WHERE team_abbr = '{abbrev}' "
        "ORDER BY CASE "
        "WHEN position = 'TQB' THEN 1 "
        "WHEN position = 'QB' THEN 2 "
        "WHEN position = 'RB' THEN 3 "
        "WHEN position = 'WR' THEN 4 "
        "WHEN position = 'TE' THEN 5 "
        "WHEN position = 'D/ST' THEN 6 "
        "WHEN position = 'K' THEN 7 "
        "ELSE 8 END"
    ).fetchall()

    conn.close()

    # current week

    # biggest blowout

    # biggest lose

    return render_template(
        "player_profile.html", team_id_name=team_id_name, roster=roster, logo=logo, team_info=team_info
    )


@core.route("/trade_activity")
def trade_activity():
    conn = sqlite3.connect(
        "C:/Users/Brian/PycharmProjects/Fantasy_Football_Flask/venv/FF_Project/data.sqlite"
    )
    conn.row_factory = sqlite3.Row
    items = conn.execute(f"SELECT * FROM activity WHERE season = {year}").fetchall()
    conn.close()
    return render_template("trade_activity.html", items=items)


@core.route("/side_bets")
def side_bets():
    pass
