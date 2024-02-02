import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        
        artist = request.form["artist"]
        if not artist or artist == "":
            return render_template("index.html")
        
        album = request.form["album"]
        if not album or album == "":
            return render_template("index.html")

        query_params = {
            "release": album,
            "artist": artist     
        }

        MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2/release-group"
        query = build_query_string(query_params) 

        url = f"{MUSICBRAINZ_API_URL}?query={query}&fmt=json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            json_res = response.json()
            print(json_res)
            #return jsonify(json_res)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to fetch data from MusicBrainz API. {str(e)}"}), 500

        return render_template("index.html")

    return render_template("index.html")





def build_query_string(query_params):
    return "".join([f" AND {key}:{value}" for key, value in query_params.items()])