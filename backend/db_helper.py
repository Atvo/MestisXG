import json
from bson import json_util
import pprint

def save_games_to_db(mongo, json, season, series):
	db_items = []
	for game_day in json:
		for game in game_day["Games"]:
			print(game)
			db_item = {
				"GameID": game["GameID"],
				"Season": season,
				"Series": series,
				"Processed": False
			}
			db_items.append(db_item)

	mongo.db.games.insert_many(db_items)
	print("save_games_to_db")

def get_games(mongo, season, processed):
	game_ids = []
	db_items = mongo.db.games.find( {"Season": 2020, "Processed": processed} )
	# print(len(db_items))
	for game in db_items:
		game_ids.append(game["GameID"])
	print(len(game_ids))
	return game_ids

def set_game_processed(mongo, gameID, processed):
	result = mongo.db.games.update_one( {"GameID": gameID}, {"$set": {"Processed": processed}})

# def process_penalties(mongo, gameID):

def get_penalty_timelines(gamereport_data, shot_data):
	log = gamereport_data["GameLogsUpdate"]
	home_team_id = gamereport_data["GamesUpdate"][0]["HomeTeam"]["Id"]
	away_team_id = gamereport_data["GamesUpdate"][0]["AwayTeam"]["Id"]
	penalty_timelines = {}


def save_shots_to_db(mongo, game_data, player_data, shot_data, gamereport_data, season, series, game_id):

	home_team_id = game_data.json()["HomeTeamID"]
	home_team_name = game_data.json()["HomeTeam"]
	away_team_id = game_data.json()["AwayTeamID"]
	away_team_name = game_data.json()["AwayTeam"]

	goalie_timelines = get_goalie_timelines(gamereport_data)
	penalty_timelines = get_penalty_timelines(gamereport_data)


	# Map jersey numbers to player ids
	home_team_jersey_to_id_map = {}
	away_team_jersey_to_id_map = {}
	player_id_to_name_map = {}
	for player in player_data.json():
		if player["TeamID"] == home_team_id:
			home_team_jersey_to_id_map[player["JerseyNr"]] = player["PersonID"]
		else:
			away_team_jersey_to_id_map[player["JerseyNr"]] = player["PersonID"]
		player_id_to_name_map[player["PersonID"]] = player["PlayerName"]


	shot_items = []
	idx = -1
	keyErrorCount = 0
	is_goal = 0
	for shot in shot_data.json():
		idx += 1
		x = int(float(shot["ShotX"]))
		y = int(float(shot["ShotY"]))

		# Convert left-hand shot coordinates to right-hand shot coordinates
		if shot["ShootingTeamID"] == shot["LTeamID"]:
			shotX = 1024 - x
			shotY = 514 - y
			blockingTeamID = shot["RTeamID"]
		else:
			shotX = x
			shotY = y
			blockingTeamID = shot["LTeamID"]

		if shot["ShootingTeamID"] == home_team_id:
			home_shot = True
		else:
			home_shot = False

		# Get player name
		player_name = player_id_to_name_map[shot["ShootingPlayerID"]]
		
		# print()
		# print(game_id)
		# print(idx)
		# print(player_name)
		# pprint.pprint(shot)

		plusIDs = []
		minusIDs = []
		assist1ID = ""
		assist2ID = ""

		if home_shot:
			shooting_team_name = home_team_name
		else:
			shooting_team_name = away_team_name

		if shot["EventType"] == "1" and shot["Goaltype"] != "RL":

			is_goal = 1
			# Convert jersey numbers to player ids
			if shot["Plus"] not in [None, ""]:
				plus_jersey_numbers = shot["Plus"].split(" ")
				for jersey_number in plus_jersey_numbers:
					try:
						if home_shot:
							player_id = home_team_jersey_to_id_map[jersey_number]
						else:
							player_id = away_team_jersey_to_id_map[jersey_number]
						plusIDs.append(player_id)
					except KeyError as e:
						keyErrorCount += 1
						print("keyErrorCount: " + str(keyErrorCount))
			
			if shot["Minus"] not in [None, ""]:
				minus_jersey_numbers = shot["Minus"].split(" ")
				for jersey_number in minus_jersey_numbers:
					try:
						if home_shot:
							player_id = away_team_jersey_to_id_map[jersey_number]
						else:
							player_id = home_team_jersey_to_id_map[jersey_number]
						minusIDs.append(player_id)
					except KeyError as e:
						keyErrorCount += 1
						print("keyErrorCount: " + str(keyErrorCount))

			if shot["Ass1Jersey"] not in [None, "0"]:
				try:
					if home_shot:
						assist1ID = home_team_jersey_to_id_map[shot["Ass1Jersey"]]
					else:
						assist1ID = away_team_jersey_to_id_map[shot["Ass1Jersey"]]
				except KeyError as e:
					keyErrorCount += 1
					print("keyErrorCount: " + str(keyErrorCount))

			if shot["Ass2Jersey"] not in [None, "0"]:
				try:
					if home_shot:
						assist2ID = home_team_jersey_to_id_map[shot["Ass2Jersey"]]
					else:
						assist2ID = away_team_jersey_to_id_map[shot["Ass2Jersey"]]
				except KeyError as e:
					keyErrorCount += 1
					print("keyErrorCount: " + str(keyErrorCount))


		ang = calculate_ang(shotX, shotY)
		ang_abs = abs(ang)
		dist = calculate_dist(shotX, shotY)

		shot_item = {
			"ShotX": shotX,
			"ShotY": shotY,
			"Goal": is_goal,
			"GoalX": shot["GoalX"],
			"GoalY": shot["GoalY"],
			"GameTime": shot["GameTime"],
			"ShootingTeamID": shot["ShootingTeamID"],
			"ShootingTeamName": shooting_team_name,
			"ShootingPlayerID": shot["ShootingPlayerID"],
			"ShootingPlayerName": player_name,
			"BlockingTeamID": blockingTeamID,
			"BlockingPlayerID": shot["BlockingPlayerID"],
			"EventType": shot["EventType"],
			"GoalType": shot["Goaltype"],
			"PlusIDs": plusIDs,
			"MinusIDs": minusIDs,
			"Assist1ID": assist1ID,
			"Assist2ID": assist2ID,
			"Season": season,
			"Series": series,
			"ShotAngle": ang,
			"ShotDist": dist,
			"ShotAngleAbs": ang_abs,
		}

		shot_items.append(shot_item)

	mongo.db.shots.insert_many(shot_items)
	
def get_all_teams(mongo, season, series):
	print("get_all_teams")
	teams = mongo.db.shots.distinct("ShootingTeamName", {"Season": season, "Series": series})
	print(teams)
	return teams
	
def get_all_shots(mongo, season, series):
	print("get_all_shots")
	json_shots = []
	for doc in mongo.db.shots.find():
		json_doc = json.dumps(doc, default=json_util.default)
		json_shots.append(json_doc)
	return json_shots
	
def get_shots_by_team(mongo, season, series, team_name, outcome_str):
	print("get_all_shots")
	["Kaikki", "Maalit", "Torjunnat", "Peitetyt", "Ohilaukaukset"],
	outcome_dict = {"Maalit": "1", "Torjunnat": "2", "Peitetyt": "3", "Ohilaukaukset": "0"}
	json_shots = []
	if outcome_str == "Kaikki":
		shots_cursor = mongo.db.shots.find({ "ShootingTeamName": team_name })
	else:
		shots_cursor = mongo.db.shots.find({ "ShootingTeamName": team_name, "EventType": outcome_dict[outcome_str] })
	for doc in shots_cursor:
	# for doc in mongo.db.shots.find({ "ShootingPlayerName": "KARPPINEN ATTE" }):
		json_doc = json.dumps(doc, default=json_util.default)
		json_shots.append(json_doc)
	return json_shots

def calculate_ang(x, y):
	goal_x_center = 68.4774
	goal_y_center = 257
	ang_rad = math.atan2(y - goal_y_center, x - goal_x_center)
	ang_deg = math.degrees(ang_rad)
	# print(ang_deg)
	return ang_deg

def calculate_dist(x,y):
	goal_x_center = 68.4774
	goal_y_center = 257
	dist = math.hypot(x - goal_x_center, y - goal_y_center)
	# print(dist)
	return dist