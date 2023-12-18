# Importing Packages
from flask import Flask, render_template
import urllib.request
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg') # This is to use matplotlib in Flask or it won't show the charts
import matplotlib.pyplot as plt

# Creating app
app = Flask('app')

@app.route('/')
def home():
	""" Every thing in the website renders from this function """
	
	# This uses api to retrive players name
	url = 'https://www.balldontlie.io/api/v1/players/2931'
	response = urllib.request.urlopen(url)
	result = json.loads(response.read())
	df = pd.json_normalize(result)
	first = df.iloc[0]["first_name"]
	last = df.iloc[0]["last_name"]

	jordan_data = []
	# This retrives Micheal Jordans data from api for every season
	for year in range(1986, 2003):
		url = f'https://www.balldontlie.io/api/v1/season_averages?season={year}&player_ids[]=2931'
		response = urllib.request.urlopen(url)
		result = json.loads(response.read())
		if len(result['data']) == 0:
			pass
		else:
			jordan_data.append(result['data'][0])
			
	# The data is converted to dataframe for ease of use
	df = pd.DataFrame(jordan_data)
	df = df.drop('player_id', axis = 1)
	# These function calls plot the graph for the website 
	line_plot(df)
	fgm_fga_chart(df)
	fg3m_fg3a_chart(df)
	games_played_chart(df)

	# This returns the data from API to the website using Flask
	return render_template("index.html", first = first, last = last, df = df)

def line_plot(df):
	"""This function plots Jordan's Points Per Season"""
	plt.figure().clear()
	plt.style.use("dark_background")
	plt.plot(df['season'], df["pts"], color = 'green', label = 'Points')
	plt.xlabel("Season")
	plt.ylabel("Points")
	plt.savefig('static/assets/images/charts/line_chart.png', transparent = True)
	return None

def fgm_fga_chart(df):
	"""This function plots Jordan's FGM VS FGA"""
	plt.figure().clear()
	plt.style.use("dark_background")
	plt.plot(df['season'], df["fgm"], color = 'green', label = 'FGM')
	plt.plot(df['season'], df["fga"], color = 'blue', label = 'FGA')
	plt.xlabel("Season")
	plt.legend()
	plt.savefig('static/assets/images/charts/fgm_fga_chart.png', transparent = True)
	return None

def fg3m_fg3a_chart(df):
	"""This function plots Jordan's FG3M VS FG3A"""
	plt.figure().clear()
	plt.style.use("dark_background")
	plt.plot(df['season'], df["fg3m"], color = 'green', label = 'FG3M')
	plt.plot(df['season'], df["fg3a"], color = 'blue', label = 'FG3A')
	plt.xlabel("Season")
	plt.legend()
	plt.savefig('static/assets/images/charts/fg3m_fg3a_chart.png', transparent = True)
	return None

def games_played_chart(df):
	"""This function plots Jordan's Number Of Games Per Season"""
	plt.figure().clear()
	plt.style.use("dark_background")
	plt.plot(df['season'], df["games_played"], color = 'blue', label = 'Number of Games Played per Season')
	plt.xlabel("Season")
	plt.ylabel("Number of Games Played per Season")
	plt.savefig('static/assets/images/charts/games_played_chart.png', transparent = True)
	return None

# This runs the app on local server
app.run(host='0.0.0.0', port=8000, debug = True)