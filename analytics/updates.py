import math
import pymongo

def update_is_goal():
	client = pymongo.MongoClient("mongodb://admin:admin@localhost", 27017)
	db = client.statsDB
	count = 0
	for doc in db.shots.find():
		doc_id = doc["_id"]
		is_goal = 0
		if doc["EventType"] == "1" and doc["GoalType"] != "RL":
			is_goal = 1
		db.shots.update_one({"_id": doc_id}, {"$set": {"Goal": is_goal}})
		count += 1

def update_ang_and_dist():
	client = pymongo.MongoClient("mongodb://admin:admin@localhost", 27017)
	db = client.statsDB
	count = 0
	for doc in db.shots.find():
	# True.shots.find().forEach(function)
		# pprint(doc)
		ang = calculate_ang(doc["ShotX"], doc["ShotY"])
		ang_abs = abs(ang)
		dist = calculate_dist(doc["ShotX"], doc["ShotY"])
		doc_id = doc["_id"]
		db.shots.update_one({"_id": doc_id}, {"$set": {"ShotDist": dist, "ShotAngle": ang, "ShotAngleAbs": ang_abs}})
		count += 1
	print(count)


def calculate_ang(x, y):
	goal_x_center = 68.4774
	goal_y_center = 257
	ang_rad = math.atan2(y - goal_y_center, x - goal_x_center)
	ang_deg = math.degrees(ang_rad)
	# print(ang_deg)
	return ang_deg

def calculate_ang_abs(x, y):
	goal_x_center = 68.4774
	goal_y_center = 257
	ang_rad = math.atan2(y - goal_y_center, x - goal_x_center)
	ang_deg = math.degrees(ang_rad)
	# print(ang_deg)
	return abs(ang_deg)

def calculate_dist(x,y):
	goal_x_center = 68.4774
	goal_y_center = 257
	dist = math.hypot(x - goal_x_center, y - goal_y_center)
	# print(dist)
	return dist

