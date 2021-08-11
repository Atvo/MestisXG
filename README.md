# Expected goals in Mestis

**WORK IN PROGRESS!**

## Overview
This is an ongoing project, where the aim is to create an end-to-end application for calculating expected goals (xG) metrics in Mestis (the second highest level of ice hockey in Finland) and to visualize the data. There's three different subprojects in the project:
1. Backend
2. Frontend
3. Analytics

Additionally, to tie these components together there's a docker-compose file which starts backend, database, and frontend containers.

## Background information
Expected goals is a metric that estimates the probability of scoring a point (or a goal) given a certain situation. Mestis was chosen because the shot events are publicly available in easy-to-read JSON format, so scraping the data was simple.

## Backend
The backend server is a simple Flask application, which has routes for scraping the data from the initial data source and saving the data to a database, and reading the saved data from the database.

## Frontend
The frontend was build using Vue. Currently it has only one view (team / joukkuenäkymä) implemented. In the team view the user can see heatmaps of the shots taken by a team during the 2019-2020 season and filter the shots based on the outcome of the shot.

## Analytics
The analytics contains the Python scripts for updating the data, visualizing the data, and creating the actual xG model. Currently the xG model is very simple and it takes into account only the shot angle and the distance from the goal.

## Future work
1. Finding out a sufficiently good algorithm for calculating the xG data and saving the xG model
2. Calculating and saving the xG probability of each shot
3. Create some routes in the backend server for accessing the xG data
4. Create some tables in the frontend to visualize the xG data, both on team and player level
5. Increase the data in database by scraping more shot data from other seasons as well
6. Enrich the shot data by finding out the situation (i.e. was the shot taken on even-strength, power-play, or short-handed)
