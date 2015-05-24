#!/usr/local/bin/python3.4

import requests
import requests.auth
from flask import json
from flask.ext.sqlalchemy import SQLAlchemy
from app import db

REDDIT_CLIENT_ID = "gcVa0IkQVW-o9A"
REDDIT_SECRET = "Z4Q6ohFhjnX2cMAEf8vw384rGr0"

LANGUAGES = [
    "ada",
    "agda",
    "C_Programming",
    "clojure",
    "coffeescript",
    "cpp",
    "csharp",
    "d_language",
    "elixir",
    "dartlang",
    "elm",
    "erlang",
    "fsharp",
    "golang",
    "groovy",
    "hacklang",
    "haxe",
    "haskell",
    "idris",
    "iolanguage",
    "java",
    "javascript",
    "julia",
    "kotlin",
    "livescript",
    "lua",
    "mathematica",
    "matlab",
    "lisp",
    "nim",
    "ocaml",
    "octave",
    "opa",
    "ObjectiveC",
    "pascal",
    "perl",
    "php",
    "processing",
    "prolog",
    "purescript",
    "python",
    "rlanguage",
    "racket",
    "ruby",
    "rust",
    "scala",
    "scheme",
    "scratch",
    "selflanguage",
    "asm", #assembly
    "smalltalk",
    "tcl",
    "typescript",
    "visualbasic",
    "wolfram",
    "swift"
]

#LANGUAGES = ["python", "ruby"]

def get_reddit_token() -> str:
    client_auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)
    post_data = {"grant_type": "password", "username": "bulldog_in_the_dream", "password": "celine"}
    headers = {"User-Agent": "Progpop/0.1 by Bulldog"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    data = json.loads(response.text)
    return data['access_token']


def get_stats_for_language(language: str, headers: dict) -> dict:

    def get_subscribers_and_accounts_active(language: str, headers: dict) -> dict:
        response = requests.get("https://oauth.reddit.com/r/" + language + "/about", headers=headers)
        print("https://oauth.reddit.com/r/" + language + "/about")
        data = json.loads(response.text)
        accounts_active = str(data['data']['accounts_active'])
        subscribers = str(data['data']['subscribers'])
        return {'accounts_active': accounts_active, 'subscribers': subscribers}

    def get_number_of_submissions_last_month(language: str, headers: dict) -> str:
        response = requests.get("https://oauth.reddit.com/r/" + language +  "/top?sort=top&t=day&limit=100", headers=headers)
        data = json.loads(response.text)
        return str(len(data['data']['children']))

    submissions = get_number_of_submissions_last_month(language, headers)
    about = get_subscribers_and_accounts_active(language, headers)
    db.engine.execute("insert into reddit values (CURRENT_DATE, '" + language + "', " + about["subscribers"] + ", " + submissions + ", " + about["accounts_active"] + ")")
    return {"submissions": submissions, "subscribers": about["subscribers"], "accounts_active": about["accounts_active"]}



def get_all_stats() -> str:
    token = get_reddit_token()
    headers = {"Authorization": "bearer " + token, "User-Agent": "Progpop/0.1 by Bulldog"}
    response_text = ""
    for language in LANGUAGES:
        stats = get_stats_for_language(language, headers)
        stats_text = language + ". Nr of submissions last day: " + stats["submissions"] + ". Subsribers: " + stats["subscribers"] + ". Logged on: " + stats["accounts_active"] + "<br>"
        response_text += stats_text
    return response_text


#get_all_stats()