from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

import json
import pprint
import random
import requests
import time

import db_helper as dbh

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://admin:admin@mongodb:27017/statsDB"
CORS(app)
mongo = PyMongo(app)

@app.route("/test", methods = ['GET', 'POST'])
def test():
	print("test")
	return "test"

@app.route("/get_games", methods = ['GET', 'POST'])
def get_games():
	print("get_games")
	url = "http://www.tilastopalvelu.fi/ih/helpers/getGames.php"
	data = {
		"dwl": "0",
		"season": "2020",
		"stgid": "168",
		"teamid": "0",
		"districtid": "0",
		"gamedays": "3",
		"dog": "2019-09-27",
	}
	r = requests.post(url, data)
	dbh.save_games_to_db(mongo, r.json(), 2020, "Mestis")
	# print(r.json())
	# print(len(r.json()))
	# matches = 0
	# for game_day in r.json():
	# 	matches += len(game_day["Games"])
	# print(matches)
	return "get_games"



@app.route("/get_shooting_map", methods = ['GET', 'POST'])
def get_shooting_map():
	print("get_shooting_map")
	games = dbh.get_games(mongo, 2020, False)
	# games = ["3935"]
	# games = ["4127"]
	get_players_url = "http://www.tilastopalvelu.fi/ih/gameshootingmap/helper/getplayers.php"
	get_shots_url = "http://www.tilastopalvelu.fi/ih/gameshootingmap/helper/getshootings.php"
	get_game_data_url = "http://www.tilastopalvelu.fi/ih/gameshootingmap/helper/getgamedata.php"
	get_gamereport_url = "http://www.tilastopalvelu.fi/ih/unsync/front1/statsapi/gamereports/getgamereportdata.php"
	idx = 0
	for game_id in games:
		data = {
			"GameID": game_id,
			"season": "2020",
		}
		print(game_id)

		game_data_response = requests.post(get_game_data_url, data)
		player_data_response = requests.post(get_players_url, data)
		shot_data_response = requests.post(get_shots_url, data)
		gamereport_data_response = requests.post(get_gamereport_url, data)
		dbh.save_shots_to_db(mongo, game_data_response, player_data_response, shot_data_response, gamereport_data_response, 2020, "Mestis", game_id)
		dbh.set_game_processed(mongo, game_id, True)
		idx += 1
		print(idx)

	return "get_shooting_map"

@app.route("/shots/team", methods = ["GET"])
def team_shots():
	team_name = request.args.get('team')
	outcome = request.args.get('outcome')
	# shots = dbh.get_all_shots(mongo, 2020, "Mestis")
	shots = dbh.get_shots_by_team(mongo, 2020, "Mestis", team_name, outcome)
	return jsonify({
		"status": "success",
		"shots": shots
		})

@app.route("/teams", methods = ["GET"])
def all_teams():
	teams = dbh.get_all_teams(mongo, 2020, "Mestis")
	return jsonify({
		"status": "success",
		"teams": teams
		})

