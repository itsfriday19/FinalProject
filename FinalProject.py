# SI 206 2017
# Project 4
# Name: Sarah Jomaa

import json
import sqlite3
import requests
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='itsfriday19', api_key='r8ezmSnXRACSHEYKEjJY')


print ("\n\n********* NEW RUN **********\n\n")

# Caching setup:
CACHE_FNAME = "206_FinalProject_cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# takes parameter d as input
# returns d in list res sorted alphabetically
def canonical_order(d):
	alphabetized_keys = sorted(d.keys())
	res = []
	for k in alphabetized_keys:
		res.append((k, d[k]))
	return res

# takes baseurl (re-initialized each time a new URL needs to be called for a function) and params as input
# returns full url (baseurl + whatever search terms/parameters may be added)
def requestURL(baseurl, params = {}):
	req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
	prepped = req.prepare()
	return prepped.url

# function to be used to check if information is in the cache
# takes base_url, params_diction, cache_diction, cache_file, and omitted_keys as input. 
# if data not in cache, writes the data to the cache and returns the data
# if data in cache, retrieves and returns that data
def get_with_caching(base_url, params_diction, cache_diction, cache_file, omitted_keys = ['api_key']):
	filtered_params_diction = {}
	for k in params_diction:
		if k not in omitted_keys:
			filtered_params_diction[k] = params_diction[k]
	full_url = requestURL(base_url, filtered_params_diction)
	# print ("full url: " + full_url)
	if full_url in cache_diction:
		# print ("\nIn cache. Retrieving cached data for URL: " + full_url, '\n')
		return cache_diction[full_url]
	else:
		response = requests.get(base_url, params=params_diction)
		# print ("\nNot in cache. Making a request to the API, adding data to cache for URL: " + full_url, '\n')

		# add to the cache and save it
		cache_diction[full_url] = response.text
		cache_file = open(cache_file, "w")
		file_str = json.dumps(cache_diction)
		cache_file.write(file_str)
		cache_file.close()
		return response.text


# iTunes API Request

def requestITURL(baseurl, params = {}):
	itunes_response = get_with_caching(baseurl, params, CACHE_DICTION, CACHE_FNAME)
	return itunes_response


# OMDb API Request

def requestOMDbURL(baseurl, params = {}):
	ombdb_response = get_with_caching(baseurl, params, CACHE_DICTION, CACHE_FNAME)
	return ombdb_response




	################################ iTunes Results ##################################




 							 ##### Song Info #####

print ("*** iTunes Artist's Songs Data ***\n")


# takes artist as input (artist being the artist the user searches for)
# uses json to load results, returns dictionary of 19 songs by the artist and all the data attributed to the song by the API
def MakeArtistRequestToIT(artist):
	it_baseurl = 'https://itunes.apple.com/search?'
	it_url_params = {'term': artist, 'limit' : '19'}
	itunes_results = requestITURL(it_baseurl, it_url_params)
	itunes_data = json.loads(itunes_results)
	return itunes_data

# takes artist as input (artist being the artist the user searches for)
# returns a list of 16 dictionaries for the 19 songs, with the song name, artist, trackprice, 
# release date, and genre as keys and the relevant data as values
def GetArtistSongs(artist):
	itunes_data = MakeArtistRequestToIT(artist)["results"]
	returnedSongs = []
	for s in itunes_data:
		song_name = s["trackName"]
		try: 							
			trackPrice = s["trackPrice"]  # If a song by the artist doesn't have a trackPrice/it's invalid, skip trackPrice for that song and continue
		except:
			continue
		artist = s["artistName"]
		release_date = s["releaseDate"][0:10]  # Pulling first 10 characters from releaseDate data so it looks like 2004-06-08 rather than 2004-06-08T07:00:00Z
		genre = s["primaryGenreName"]
		songInfo_dict = {"song_name": song_name, "artist": artist, "trackPrice": trackPrice, "release_date": release_date, "genre": genre}
		returnedSongs.append(songInfo_dict)
	return (returnedSongs)

askArtist = input("Pick an artist to search: ")
print ("19 Songs by {}: \n".format(askArtist))
print ("\n", GetArtistSongs(askArtist), "\n\n")


# takes artist as input (artist being the artist the user searches for)
# returns a list of the top 5 songs by that artist
def Top5Songs(artist):
	topfiveSongs = []
	for d in GetArtistSongs(artist):
		topfiveSongs.append(d["song_name"])
	return topfiveSongs[0:5]

print ("Of those, {}'s top 5 songs are: \n".format(askArtist), Top5Songs(askArtist), "\n")



						 ##### iTunes Movie Info ##### 



print ("\n*** iTunes Movie Data ***\n")

# takes movie as input (movie being the movie the user searches for)
# uses json to load results, returns dictionary with movie and all the data attributed to it by the API
def MakeMovieRequestToIT(movie):
	it_baseurl = 'https://itunes.apple.com/search?'
	it_url_params = {'term': movie, 'country' : 'US', 'entity': 'movie', 'limit' : '1'}
	itunes_results = requestITURL(it_baseurl, it_url_params)
	itunes_data = json.loads(itunes_results)
	return itunes_data

# takes movie as input (movie being the movie the user searches for)
# returns dictionary of movie with the data points I pulled from itunes_data (i.e. movie name, description, track price, rental price, and genre)
def GetMovieInfo(movie):
	itunes_data = MakeMovieRequestToIT(movie)["results"][0]

	movie_name = itunes_data["trackName"]
	description = itunes_data["longDescription"]
	movie_buyPrice = itunes_data["trackPrice"]
	movie_rentPrice = itunes_data["trackRentalPrice"]
	genre = itunes_data["primaryGenreName"]

	movieInfo_dict = {"movie_name": movie_name, "description": description, "movie_buyPrice": movie_buyPrice, "movie_rentPrice": movie_rentPrice, "genre": genre}

	return (movieInfo_dict)

askMovie = input("Pick a movie title or a keyterm to search for a movie: \n")
print (GetMovieInfo(askMovie)) 




	################################ OMDb Results ##################################




print ("\n*** OMDb Movie Data ***\n")

# takes movie as input (movie being the movie the user searches for)
# uses json to load results, returns dictionary with movie and all the data attributed to it by the API
def MakeRequestToOMDb(movie):
	omdb_baseurl = "http://www.omdbapi.com/?apikey=b95d25d9&"
	omdb_params = {"t": movie, "type": "movie", "plot": "full", "r": "json"}
	omdb_results = requestOMDbURL(omdb_baseurl, omdb_params)
	omdb_data = json.loads(omdb_results)
	return omdb_data

# takes movie as input (movie being the movie the user searches for)
# returns dictionary of movie with the data points I pulled from omdb_data (i.e. imdb rating, release data, actors, and director)
def GetOMDbMovieInfo(movie):
	omdb_data = MakeRequestToOMDb(movie)

	imdb_rating = omdb_data["imdbRating"]
	release_date = omdb_data["Released"]
	actors = omdb_data["Actors"]
	director = omdb_data["Director"]
	movieInfo_dict = {"imdb_rating": imdb_rating, "release_date": release_date, "actors": actors, "director": director}
	
	return movieInfo_dict

# print (MakeRequestToOMDb(askMovie))
print (GetOMDbMovieInfo(askMovie))



		### Combined Movie Data ###


print ("\n*** Combined Movie Data ***\n")



for m in GetMovieInfo(askMovie):		# iterating into GetMovieInfo(askMovie)
	itunesMovieDict = GetMovieInfo(askMovie)	# assigning itunes movie dictionaries to variable
	omdbMovieDict = GetOMDbMovieInfo(askMovie)	# assigning omdb movie dictionaries to variable
	fullmovieInfo = {**itunesMovieDict, **omdbMovieDict}	# merging the two dictionaries

print (fullmovieInfo)




	############### Creating & Loading Database ###############



# creating sqlite file
conn = sqlite3.connect('FinalProject_DB.sqlite')
cur = conn.cursor()

# creating Songs table, setting artist, song_name, release_date, genre, trackPrice as column headers
cur.execute("DROP TABLE IF EXISTS Songs")
cur.execute("CREATE TABLE Songs (artist TEXT NOT NULL, song_name TEXT NOT NULL, release_date TEXT NOT NULL, genre TEXT NOT NULL, trackPrice INT NOT NULL)")

# interating into GetArtistSongs(askArtist)
for d in GetArtistSongs(askArtist):
	tup = d["song_name"], d["artist"], d["trackPrice"], d["release_date"], d["genre"]	# creating tuple with data points relevant to established column headers
	cur.execute('SELECT artist FROM Songs WHERE artist = ?',(tup[1],))
	if len(cur.fetchall()) == 0:
		cur.execute('INSERT INTO Songs (artist, song_name, trackPrice, release_date, genre) VALUES (?, ?, ?, ?, ?)', tup)	# inserting data points into table



conn.commit()

# creating Movie table, setting movie_name, description, genre, release_date, imdb_rating, director, actors, movie_rentPrice, and movie_buyPrice as column headers
cur.execute("DROP TABLE IF EXISTS Movie")
cur.execute("CREATE TABLE Movie (movie_name TEXT NOT NULL, description TEXT NOT NULL, genre TEXT NOT NULL, release_date TEXT NOT NULL, imdb_rating TEXT NOT NULL, director TEXT NOT NULL, actors TEXT NOT NULL, movie_rentPrice INT NOT NULL, movie_buyPrice INT NOT NULL)")

# 
for d in GetMovieInfo(askMovie): # askArtist
	tup2 = fullmovieInfo["movie_name"], fullmovieInfo["description"], fullmovieInfo["genre"], fullmovieInfo["release_date"], fullmovieInfo["imdb_rating"], fullmovieInfo["director"], fullmovieInfo["actors"], fullmovieInfo["movie_rentPrice"], fullmovieInfo["movie_buyPrice"]
	cur.execute('SELECT movie_name FROM Movie WHERE movie_name = ?', (tup2[0],))
	if len(cur.fetchall()) == 0:	# if the movie_name is not already in cur.fetchall, insert data points into table
		cur.execute('INSERT INTO Movie (movie_name, description, genre, release_date, imdb_rating, director, actors, movie_rentPrice, movie_buyPrice) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', tup2)

conn.commit()

cur.close()




	############### Creating Plotly Visualization ###############




dates = []
prices = []


# iterating into each dictionary in GetArtistSongs(askArtist) and appending the songs' release dates to list date and the songs' prices to list prices
for d in GetArtistSongs(askArtist):
	dt = dates.append(d["release_date"])
	p = prices.append(float(d["trackPrice"]))

print("\n{}'s song prices:".format(askArtist), prices)
print ("\nCreating Plotly visualization...\n")

# creating the line in a line graph
songline = go.Scatter(
    x = dates,
    y = prices,
    mode = 'markers',  # data is shown in unconnected points. Available modes are markers, lines+markers, and lines
    name = 'Songs',	   # name of line in legend
    line = dict(color = ('rgb(255, 187, 43)'), width = 5)  # color and width of the line
)

data = [songline]

# customizing layout of the graph
layout = dict(title = "Price of {}'s Songs by Release Date".format(askArtist),  # Title of the graph
              xaxis = dict(title = 'Release Date'),  # x-axis label
              yaxis = dict(title = 'Price (USD)'),   # y-axis label
              showlegend = True,	# displaying the legend
              )

fig = dict(data = data, layout = layout)
py.iplot(fig, filename ='SongsReleasedBy_DateAndPrice')  # plotting the graph, giving it a filename




