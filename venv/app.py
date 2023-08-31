from FF_Project import app, db
from flask import render_template
from FF_Project.functions.data_pull import DataPulls
from FF_Project.creds import lg_id,espn_s2,swid,year
import sqlite3
from espn_api.football import League

# @app.before_first_request
# def on_start_up():
#     db.create_all()
#     DataPulls(lg_id,year,espn_s2,swid).standings_pull()
#     DataPulls(lg_id,year,espn_s2,swid).activity_pull()

if __name__ == '__main__':
    app.run(debug=True)