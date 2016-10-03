# Lim Zhi Han Ryan, 1000985
# Nguyen Tung Lam, 1001289

import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, g, request, Response, json

def make_request(request_type, url, data={}, headers={'Content-Type': 'application/json'}, auth=False):
	if auth:
		r = request_type(url, headers=headers, json=data, auth=HTTPBasicAuth('someuser', 'unpredictable'))
	else:
		r = request_type(url, headers=headers, json=data)
	print(r.headers)
	print(r.text)
	print()


# Create a user
url = 'http://127.0.0.1:5000/users'
print("POST " + url)
user = {'username':'someuser','password':'unpredictable'}
make_request(requests.post, url, user)


# Post a movie in text/plain
url = 'http://127.0.0.1:5000/movies'
print("POST " + url)
movie = {'title':'Fight Club', 'description':'Will give you chill', 'director':'David Fincher', 'year':'1999'}
headers = {'Content-Type': 'text/plain'}
make_request(requests.post, url, movie, headers, True)


# Post a movie in json
headers = {'Content-Type': 'application/json'}
make_request(requests.post, url, movie, headers, True)

# Get all movies in text
url = 'http://127.0.0.1:5000/movies'
print("GET " + url)
headers = {'Content-Type': 'text/plain'}
make_request(requests.get, url, {}, headers, True)


# Get all movies in json
url = 'http://127.0.0.1:5000/movies'
print("GET " + url)
headers = {'Content-Type': 'application/json'}
make_request(requests.get, url, {}, headers, True)

# Get a movie
url = 'http://127.0.0.1:5000/movie/1'
print("GET " + url)
make_request(requests.get, url)

# Delete a movie
url = 'http://127.0.0.1:5000/movie/1'
print("DELETE " + url)
make_request(requests.delete, url)

# Update a movie
url = 'http://127.0.0.1:5000/movie/2'
print("PATCH " + url)
data = {'description':'this is an updated description'}
make_request(requests.patch, url, data, headers)

# Rate a movie
url = 'http://127.0.0.1:5000/movie/2/rate'
print("PATCH " + url)
data = {'rating':'3.0'}
make_request(requests.patch, url, data, headers)

# Rate again
url = 'http://127.0.0.1:5000/movie/2/rate'
data = {'rating':'5.0'}
make_request(requests.patch, url, data, headers)

# root_url = 'http://127.0.0.1:5000/movie/'
# for i in range(1, 25):
# 	url= root_url + str(i)
# 	print(url)
# 	make_request(requests.delete, url)