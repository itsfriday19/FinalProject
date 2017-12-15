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
from spotipy.oauth2 import SpotifyClientCredentials

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
		print ("\nIn cache. Retrieving cache data that goes along with the request for URL: " + full_url, '\n')
		return cache_diction[full_url]
	else:
		# step 3
		response = requests.get(base_url, params=params_diction)
		print ("\nNot in cache. Making a request to the API and adding saved data to cache file for URL: " + full_url, '\n')

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


   # Spotify API Request

def requestSpotifyURL(baseurl, params = {}):
	spotify_response = get_with_caching(baseurl, params, CACHE_DICTION, CACHE_FNAME)
	return spotify_response

#     # YouTube API Request

# def requestYTURL(baseurl, params = {}):
# 	youtube_response = get_with_caching(baseurl, params, CACHE_DICTION, CACHE_FNAME)



	################################ iTunes Results ##################################

def MakeRequestToIT(song):
	it_baseurl = 'https://itunes.apple.com/search?'
	it_url_params = {'term': song, 'country' : 'US', 'entity': 'song', 'limit' : '1'}
	itunes_results = requestITURL(it_baseurl, it_url_params)
	itunes_data = json.loads(itunes_results)
	return itunes_data

# Song Info (song name, price, artist, release date, genre)
def ExtractSongInfo(song):
	itunes_data = MakeRequestToIT(song)["results"][0]

	song_name = itunes_data["trackName"]
	trackPrice = itunes_data["trackPrice"]
	artist = itunes_data["artistName"]
	release_date = itunes_data["releaseDate"]
	genre = itunes_data["primaryGenreName"]

	songInfo_dict = {"song_name": song_name, "trackPrice": trackPrice, "artist": artist, "release_date": release_date, "genre": genre}

	return (songInfo_dict)
	


print ("*** iTunes Data ***\n", ExtractSongInfo("Passenger Side"))


# Song Reviews     # get 100 song reviews
# def ExtractSongReviews(song):
# 	songReviews_list = []



# Movie Info (price, genre, release date, upvote/downvote(?))
# def ExtractMovieInfo(movie):
# 	self.movie = movie

# 	it_baseurl = 'https://itunes.apple.com/search?'
#     it_url_params = {'term': , 'country' : 'US', 'entity': '', 'limit' : ''}
#     itunes_results = requestITURL(it_baseurl, it_url_params)
#     itunes_data = json.loads(itunes_results)

#     self.itunes_data = itunes_data


	################################ Spotify Results ##################################

# Can't get track plays, not available with the current Spotify API
# Changed to getting top ten tracks for an artist. Subject to change, most probably to song category type (aka genre)
# ---Trouble getting access token??

spotify = spotipy.Spotify()
client_credentials_manager = SpotifyClientCredentials(client_id =  '2c93b879c5684c58a98aa0aa54147716', client_secret =  '40990bfb43ff499b881ed5c6b06ffd61')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def MakeRequestToSpotify(artist):
	spotify_baseurl = "https://api.spotify.com"
	spotify_params = sp.search(q= 'artist:' + artist, type= 'artist', limit= 1)
	spotify_results = requestSpotifyURL(spotify_baseurl, spotify_params)
	spotify_data = json.loads(spotify_results)
	print ("\n\n*** Spotify Data ***\n", spotify_data)
	return spotify_data

# def ExtractArtistTopTracks(artist_id):
# 	pass

print (MakeRequestToSpotify("Passenger Side"))

	################################ YouTube Results ##################################

def MakeRequestToYT(song):
	# yt_baseurl = ""
	# yt_params = 
	# yt_results = 
	# yt_data = 
	# print ("\n\n*** YouTube Data ***\n", yt_data)
	# return yt_data
	pass




	############# Create & Load Database #############

# conn = sqlite3.connect('FinalProject_DB.sqlite')
# cur = conn.cursor()

# cur.execute("DROP TABLE IF EXISTS Songs")
# cur.execute("CREATE TABLE Songs (song_name TEXT PRIMARY KEY NOT NULL, artist TEXT NOT NULL, release_date TEXT NOT NULL, genre TEXT NOT NULL, review TEXT NOT NULL)")

# conn.commit()

# cur.execute("DROP TABLE IF EXISTS Movies")
# cur.execute("CREATE TABLE Movies (movie_name TEXT PRIMARY KEY NOT NULL, genre TEXT NOT NULL, release_date TEXT NOT NULL)")

# conn.commit()

# cur.close()
