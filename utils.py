from bottle import template, TEMPLATE_PATH
import json
import os


JSON_FOLDER = './data'
AVAILABE_SHOWS = ["7", "66", "73", "82", "112", "143", "175", "216", "1371", "1871","2993", "305"]

def getVersion():
    return "0.0.1"

def getJsonFromFile(showName):
    try:
        return template("{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=showName))
    except:
        return "{}"

def search_shows(q):
    content = []
    results = []
    for show in AVAILABE_SHOWS:
        content.append(json.loads(getJsonFromFile(show)))
    for cont in content:
        episodes = cont['_embedded']['episodes']
        for episode in episodes:
            if q in episode['name']:
                results.append({'showid':cont['id'],'episodeid':episode['id'],'text':cont['name'] + ": " + episode['name']})
            elif q in str(episode['summary']):
                results.append({'showid':cont['id'],'episodeid':episode['id'],'text':cont['name'] + ": " + episode['name']})
    return results
