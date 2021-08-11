import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymongo
import scipy as sp
import scipy.ndimage


## Smoothing on edges ??
def goal_ratio():
	client = pymongo.MongoClient("mongodb://admin:admin@localhost", 27017)
	db = client.statsDB
	shots = db.shots
	shots_df = pd.DataFrame(list(shots.find({"ShotX": {"$gt": 70, "$lt" : 380}})))
	goals_df = pd.DataFrame(list(shots.find({"EventType": "1", "ShotX": {"$gt": 70, "$lt" : 380}})))

	shots_shotX_df = shots_df["ShotX"]
	shots_shotY_df = shots_df["ShotY"]

	goals_shotX_df = goals_df["ShotX"]
	goals_shotY_df = goals_df["ShotY"]

	# FIX MIN MAX!
	# shots_H, shots_xedges, shots_yedges = np.histogram2d(shots_shotX_df, shots_shotY_df, bins=[120, 58])
	# goals_H, goals_xedges, goals_yedges = np.histogram2d(goals_shotX_df, goals_shotY_df, bins=[120, 58])
	shots_H, shots_xedges, shots_yedges = np.histogram2d(shots_shotX_df, shots_shotY_df, bins=[120, 58], range=[[0,1024],[0,514]])
	goals_H, goals_xedges, goals_yedges = np.histogram2d(goals_shotX_df, goals_shotY_df, bins=[120, 58], range=[[0,1024],[0,514]])

	sigma = [1.0, 1.0]
	shots_smoothed_X = sp.ndimage.filters.gaussian_filter(shots_H, sigma, mode="constant")
	goals_smoothed_X = sp.ndimage.filters.gaussian_filter(goals_H, sigma, mode="constant")
	# ratio_smoothed_X = np.divide(goals_H, shots_H, out=np.zeros_like(goals_H), where=shots_H!=0)
	# ratio_smoothed_X = sp.ndimage.filters.gaussian_filter(np.divide(goals_H, shots_H, out=np.zeros_like(goals_H), where=shots_H!=0), sigma, mode="constant")
	ratio_smoothed_X = np.divide(goals_smoothed_X, shots_smoothed_X, out=np.zeros_like(goals_smoothed_X), where=shots_smoothed_X!=0)

	print(pd.DataFrame(shots_H).describe().head())
	print()
	print(pd.DataFrame(shots_H).max())
	print(pd.DataFrame(shots_H).sum())
	print()
	print(pd.DataFrame(goals_H).max())
	print(pd.DataFrame(goals_H).sum())
	print()
	print("ratio")
	print(pd.DataFrame(ratio_smoothed_X).max())
	print(pd.DataFrame(ratio_smoothed_X).sum())
	print()
	print("idxmax")
	print(pd.DataFrame(ratio_smoothed_X).idxmax())
	print()
	print(shots_H[29][9])
	print(shots_H[30][9])
	print(goals_H[29][9])
	print(goals_H[30][9])
	print(ratio_smoothed_X[29][9])
	print(ratio_smoothed_X[30][9])
	print()
	print(shots_H[9][29])
	print(shots_H[9][30])
	print(goals_H[9][29])
	print(goals_H[9][30])
	print(shots_smoothed_X[9][29])
	print(shots_smoothed_X[9][30])
	print(goals_smoothed_X[9][29])
	print(goals_smoothed_X[9][30])
	print(ratio_smoothed_X[9][29])
	print(ratio_smoothed_X[9][30])
	print(pd.DataFrame(goals_H).describe().head())
	df = pd.DataFrame(ratio_smoothed_X)
	print(df.head())
	print(df.describe().head())


	fig = plt.figure(figsize=(120, 58))
	ax = fig.add_subplot(131, title='shots',
        aspect='equal')
	X, Y = np.meshgrid(shots_yedges, shots_xedges)
	plot = ax.pcolormesh(X, Y, shots_smoothed_X)
	fig.colorbar(plot)

	ax = fig.add_subplot(132, title='goals',
        aspect='equal')
	X, Y = np.meshgrid(shots_yedges, shots_xedges)
	plot = ax.pcolormesh(X, Y, goals_smoothed_X)
	fig.colorbar(plot)

	ax = fig.add_subplot(133, title='ratio',
        aspect='equal')
	X, Y = np.meshgrid(shots_yedges, shots_xedges)
	plot = ax.pcolormesh(X, Y, ratio_smoothed_X)
	fig.colorbar(plot)

	plt.show()

def total_goals():
	client = pymongo.MongoClient("mongodb://admin:admin@localhost", 27017)
	db = client.statsDB
	shots = db.shots
	df = pd.DataFrame(list(shots.find({"EventType": "0"})))
	print(df)
	shotX_df = df["ShotX"]
	shotY_df = df["ShotY"]


	H, xedges, yedges = np.histogram2d(shotX_df, shotY_df, bins=[120, 58])
	fig = plt.figure(figsize=(120, 58))
	ax = fig.add_subplot(141, title='pcolormesh: actual edges',
        aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, H)
	fig.colorbar(plot)
	
	sigma = [1.0, 1.0]
	smoothed_X = sp.ndimage.filters.gaussian_filter(H, sigma, mode="constant")
	ax = fig.add_subplot(142, title='smoothed_X1', aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, smoothed_X)
	fig.colorbar(plot)
	print(smoothed_X)
	print(type(smoothed_X))
	
	sigma = [2.0, 2.0]
	smoothed_X = sp.ndimage.filters.gaussian_filter(H, sigma, mode="constant")
	ax = fig.add_subplot(143, title='smoothed_X2', aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, smoothed_X)
	fig.colorbar(plot)
	
	sigma = [3.0, 3.0]
	smoothed_X = sp.ndimage.filters.gaussian_filter(H, sigma, mode="constant")
	ax = fig.add_subplot(144, title='smoothed_X3', aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, smoothed_X)
	fig.colorbar(plot)


	plt.show()

def total_shots():
	print("main")
	client = pymongo.MongoClient("mongodb://admin:admin@localhost", 27017)
	db = client.statsDB
	print(db.name)
	print(db.list_collection_names())
	shots = db.shots
	print(shots.count_documents({}))
	aggr = shots.aggregate([{ "$group": {"_id": None, "maxX": { "$max": "$ShotX" }, "maxY": { "$max": "$ShotY" }, "minX": { "$min": "$ShotX" }, "minY": { "$min": "$ShotY" } }}])
	print(list(aggr))
	df = pd.DataFrame(list(shots.find()))
	print(df)
	shotX_df = df["ShotX"]
	shotY_df = df["ShotY"]


	# H, xedges, yedges = np.histogram2d(shotX_df, shotY_df, bins=100)
	# fig = plt.figure(figsize=(100, 100))
	# ax = fig.add_subplot(131, title='pcolormesh: actual edges',
 #        aspect='equal')
	# X, Y = np.meshgrid(yedges, xedges)
	# plot = ax.pcolormesh(X, Y, H)
	# fig.colorbar(plot)

	H, xedges, yedges = np.histogram2d(shotX_df, shotY_df, bins=[120, 58])
	fig = plt.figure(figsize=(120, 58))
	ax = fig.add_subplot(141, title='pcolormesh: actual edges',
        aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, H)
	fig.colorbar(plot)
	
	sigma = [1.0, 1.0]
	smoothed_X = sp.ndimage.filters.gaussian_filter(H, sigma, mode="constant")
	ax = fig.add_subplot(142, title='smoothed_X1', aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, smoothed_X)
	fig.colorbar(plot)
	
	sigma = [2.0, 2.0]
	smoothed_X = sp.ndimage.filters.gaussian_filter(H, sigma, mode="constant")
	ax = fig.add_subplot(143, title='smoothed_X2', aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, smoothed_X)
	fig.colorbar(plot)
	
	sigma = [3.0, 3.0]
	smoothed_X = sp.ndimage.filters.gaussian_filter(H, sigma, mode="constant")
	ax = fig.add_subplot(144, title='smoothed_X3', aspect='equal')
	X, Y = np.meshgrid(yedges, xedges)
	plot = ax.pcolormesh(X, Y, smoothed_X)
	fig.colorbar(plot)


	plt.show()