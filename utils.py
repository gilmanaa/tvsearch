from bottle import template, redirect
import json


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

def show_shows(id):
    data = getJsonFromFile(id)
    if len(data) == 2:
        return "error"
    data = json.loads(data)
    sectionTemplate = "./templates/show.tpl"
    return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=data)

def show_episodes(showId, epId):
    data = getJsonFromFile(showId)
    data = json.loads(data)["_embedded"]["episodes"]
    for episode in data:
        if episode["id"] == epId:
            ep = episode
            sectionTemplate = "./templates/episode.tpl"
            return template("./pages/index.html", version=getVersion(), sectionTemplate=sectionTemplate,
                            sectionData=ep)
    return "error"
