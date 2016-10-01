import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, g, request, Response, json


# Create a user
url = 'http://127.0.0.1:5000/users'
user = {'username':'someuser','password':'unpredictable'}
headers = {'Content-Type': 'application/json'}
r = requests.post(url, headers=headers, json=user)
print("POST " + r.url)
print(r.headers)
print(r.json())
print()

# Post a movie
url = 'http://127.0.0.1:5000/movies'
movie = {'title':'Fight Club', 'description':'Will give you chill', 'director':'David Fincher', 'year':'1999', 'rating':'4.5'}
headers = {'Content-Type': 'application/json'}
r = requests.post(url, headers=headers, json=movie, auth=HTTPBasicAuth('someuser', 'unpredictable'))
print("POST " + r.url)
print(r.headers)
print(r.json())
print()

# Get all movies
r = requests.get(url, headers=headers)
print("GET " + r.url)
print(r.headers)
print(r.json())
print()

# Get a movie
url = 'http://127.0.0.1:5000/movie/3'
r = requests.get(url, headers=headers)
print("GET " + r.url)
print(r.headers)
print(r.json())
print()

# Delete a movie
url = 'http://127.0.0.1:5000/movie/2'
r = requests.delete(url, headers=headers)
print("DELETE " + r.url)
print(r.headers)
print(r.json())
print()

# Update a movie
url = 'http://127.0.0.1:5000/movie/3'
data = {'description':'this is an updated description'}
r = requests.patch(url, headers=headers, json=data)
print("PATCH " + r.url)
print(r.headers)
print(r.json())
print()
