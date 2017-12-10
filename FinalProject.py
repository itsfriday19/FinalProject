# SI 206 2017
# Project 4
# Name: Sarah Jomaa

import unittest
import itertools
import collections
import json
import sqlite3

CACHE_FNAME = "206_FinalProject_cache.json"

# Caching setup:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


    # iTunes API

    # get 100 song reviews


    # Spotify API


    # YouTube API