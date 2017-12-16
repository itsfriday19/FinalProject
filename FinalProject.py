# SI 206 2017
# Project 4
# Name: Sarah Jomaa

import unittest
import itertools
import collections
import json
import sqlite3
import requests
import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# from youtube import YouTube

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

def canonical_order(d):
	alphabetized_keys = sorted(d.keys())
	res = []
	for k in alphabetized_keys:
		res.append((k, d[k]))
	return res

def requestURL(baseurl, params = {}):
	req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
	prepped = req.prepare()
	return prepped.url

def get_with_caching(base_url, params_diction, cache_diction, cache_file, omitted_keys = ['api_key']):
	filtered_params_diction = {}
	for k in params_diction:
		if k not in omitted_keys:
			filtered_params_diction[k] = params_diction[k]
	full_url = requestURL(base_url, filtered_params_diction)
	# step 1
	# print ("full url: " + full_url)
	if full_url in cache_diction:
		# step 2
		print ("\nIn cache. Retrieving cached data for URL: " + full_url, '\n')
		return cache_diction[full_url]
	else:
		# step 3
		response = requests.get(base_url, params=params_diction)
		print ("\nNot in cache. Making a request to the API, adding data to cache for URL: " + full_url, '\n')

		# add to the cache and save it permanently
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

# ### Song Info ###
# (song name, artist, price, release date, genre)

print ("*** iTunes Artist's Songs Data ***\n")

def MakeArtistRequestToIT(artist):
	it_baseurl = 'https://itunes.apple.com/search?'
	it_url_params = {'term': artist, 'limit' : '19'}
	itunes_results = requestITURL(it_baseurl, it_url_params)
	itunes_data = json.loads(itunes_results)
	return itunes_data

def GetArtistSongs(artist):
	itunes_data = MakeArtistRequestToIT(artist)["results"]
	returnedSongs = []
	for s in itunes_data:
		song_name = s["trackName"]
		trackPrice = s["trackPrice"]
		artist = s["artistName"]
		release_date = s["releaseDate"]
		genre = s["primaryGenreName"]
		songInfo_dict = {"song_name": song_name, "artist": artist, "trackPrice": trackPrice, "release_date": release_date, "genre": genre}
		returnedSongs.append(songInfo_dict)

	return (returnedSongs)

askArtist = input("Pick an artist to search: ")
print ("20 Songs by", askArtist)
print ("\n\n", GetArtistSongs(askArtist), "\n\n")

# ### Movie Info ### 
# (genre, movie name, director, description, buy and rent price)

print ("\n*** iTunes Movie Data ***\n")

def MakeMovieRequestToIT(movie):
	it_baseurl = 'https://itunes.apple.com/search?'
	it_url_params = {'term': movie, 'country' : 'US', 'entity': 'movie', 'limit' : '1'}
	itunes_results = requestITURL(it_baseurl, it_url_params)
	itunes_data = json.loads(itunes_results)
	return itunes_data

def GetMovieInfo(movie):
	itunes_data = MakeMovieRequestToIT(movie)["results"][0]

	# print (itunes_data)

	movie_name = itunes_data["trackName"]
	# director = itunes_data["artistName"]
	# release_year = itunes_data["releaseDate"]
	description = itunes_data["longDescription"]
	movie_buyPrice = itunes_data["trackPrice"]
	movie_rentPrice = itunes_data["trackRentalPrice"]
	genre = itunes_data["primaryGenreName"]

	movieInfo_dict = {"movie_name": movie_name, "director": director, "description": description, "movie_buyPrice": movie_buyPrice, "movie_rentPrice": movie_rentPrice, "genre": genre}

	return (movieInfo_dict)

askMovie = input("Pick a movie to search: ")
print (GetMovieInfo(askMovie))


	################################ OMDb Results ##################################
print ("\n*** OMDb Movie Data ***\n")

def MakeRequestToOMDb(movie):
	omdb_baseurl = "http://www.omdbapi.com/?apikey=b95d25d9&"
	omdb_params = {"t": movie, "type": "movie", "plot": "full", "r": "json"}
	omdb_results = requestOMDbURL(omdb_baseurl, omdb_params)
	omdb_data = json.loads(omdb_results)
	return omdb_data

# def GetMovieInfo(movie):
# 	omdb_data = MakeRequestToOMDb(movie)[]

# 	imdb_rating = omdb_data["imdbRating"]
# 	release_date = omdb_data["Released"]
# 	actors = omdb_data["Actors"]
#	director = omdb_data["Director"]
# 	pass

print (MakeRequestToOMDb(askMovie))

	############# Create & Load Database #############

# movie = GetMovieInfo("askMovie")

conn = sqlite3.connect('FinalProject_DB.sqlite')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Songs")
cur.execute("CREATE TABLE Songs (artist TEXT PRIMARY KEY NOT NULL, song_name TEXT NOT NULL, release_date TEXT NOT NULL, genre TEXT NOT NULL, trackPrice TEXT NOT NULL)")

for d in GetArtistSongs(askArtist):
	tup = d["song_name"], d["artist"], d["trackPrice"], d["release_date"], d["genre"]
	if len(cur.fetchall()) == 0:
		cur.execute('INSERT INTO Songs (artist, song_name, release_date, genre, trackPrice) VALUES (?, ?, ?, ?, ?)', tup)



conn.commit()

# cur.execute("DROP TABLE IF EXISTS Movies")
# cur.execute("CREATE TABLE Movies (movie_name TEXT PRIMARY KEY NOT NULL, genre TEXT NOT NULL, release_date TEXT NOT NULL)")

# conn.commit()

cur.close()
