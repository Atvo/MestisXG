import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
import pymongo
import scipy as sp
import scipy.ndimage
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics




def main():
	# model = logistic_regression()
	# model = gaussian_naive_bayes()
	# model = create_model("log_reg")
	# model = create_model("gnb")
	# model = create_model("rfc")
	# model = create_model("tree")
	# model = create_model("knn")
	# model = create_model("lda")
	model = create_model("svc")
	visualize_model(model)

def visualize_model(model):
	x = np.arange(68, 380, 1)
	y = np.arange(0, 512, 1)
	print(len(x))
	print(len(y))
	angle_f = np.vectorize(calculate_ang) 
	# angle_f = np.vectorize(calculate_ang_abs) 
	dist_f = np.vectorize(calculate_dist)
	# prob_f = np.vectorize(calculate_prob)
	xx, yy = np.meshgrid(x, y, sparse=True)
	ang_arr = angle_f(x[:,None], y[None,:])
	ang_list = ang_arr.flatten()
	dist_arr = dist_f(x[:,None], y[None,:])
	dist_list = dist_arr.flatten()
	print(ang_arr)
	print(dist_arr)
	print()
	print(ang_list.shape)
	print(dist_list)
	print()
	# X_grid = np.vstack((dist_list, ang_list)).T
	X_grid = np.vstack((ang_list, dist_list)).T
	print("X_grid")
	print(X_grid)
	X_grid = StandardScaler().fit(X_grid).transform(X_grid)
	print(X_grid.shape)
	print()

	# predictions = model.predict(X_grid)
	predictions = model.predict_proba(X_grid)

	print("predictions")
	print(predictions)
	print(predictions.shape)
	print()
	
	goal_probs = predictions[:,1]
	goal_probs_grid = np.reshape(goal_probs, (-1, 512))

	print("goal_probs")
	print(goal_probs)
	print(goal_probs.shape)
	print()
	print("goal_probs_grid")
	print(goal_probs_grid)
	print(goal_probs_grid.shape)
	print(np.amax(goal_probs))
	ind = np.unravel_index(np.argmax(goal_probs_grid, axis=None), goal_probs_grid.shape)
	print(ind)
	print(goal_probs_grid[ind])

	prob_arr = None
	Z = np.random.rand(512, 312)
	print(Z.shape)
	CS = plt.pcolormesh(y, x, goal_probs_grid)
	plt.contour(y, x, goal_probs_grid, [0.05, 0.1, 0.2, 0.3, 0.4, 0.5], colors="k")
	plt.colorbar(CS)
	plt.show()

def create_model(model_type):
	client = pymongo.MongoClient("mongodb://admin:admin@localhost", 27017)
	db = client.statsDB
	shots = db.shots
	shots_df = pd.DataFrame(list(shots.find({"ShotX": {"$gt": 68, "$lt" : 380}})))

	X_var = np.asarray(shots_df[["ShotAngle", "ShotDist"]])
	# X_var = np.asarray(shots_df[["ShotAngleAbs", "ShotDist"]])
	y_var = np.asarray(shots_df["Goal"])

	X_var = StandardScaler().fit(X_var).transform(X_var)

	x_train, x_test, y_train, y_test = train_test_split(X_var, y_var, test_size=0.25, random_state=0)
	
	if model_type == "gnb":
		model = GaussianNB()
	if model_type == "log_reg":
		model = LogisticRegression()
		# model = LogisticRegression(class_weight="balanced")
	if model_type == "rfc":
		model = RandomForestClassifier()
	if model_type == "tree":
		model = DecisionTreeClassifier()
	if model_type == "knn":
		model = KNeighborsClassifier()
	if model_type == "lda":
		model = LinearDiscriminantAnalysis()
	if model_type == "svc":
		model = SVC(probability = True)
		
	model.fit(x_train, y_train)

	predictions = model.predict_proba(x_test)

	score = model.score(x_test, y_test)
	

	print(1-np.average(y_var))
	print(np.average(predictions, axis=0))

	return model

main()