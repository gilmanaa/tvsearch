import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, TEMPLATE_PATH)
import utils
import json

TEMPLATE_PATH.insert(0, os.path.dirname(__file__))

# Static Routes


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")

@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")

@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")

@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

@route("/browse")
def search():
    resultArr = []
    for show in utils.AVAILABE_SHOWS:
        data = utils.getJsonFromFile(show)
        data = json.loads(data)
        resultArr.append(data)
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=resultArr)

@route("/search")
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

@route("/search",method="POST")
def search_shows():
    q = request.POST.get("q")
    search_results = utils.search_shows(q)
    sectionTemplate = "./templates/search_result.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {}, results=search_results, query=q)

@route("/ajax/show/<id:int>")
def showShow(id):
    data = utils.getJsonFromFile(id)
    data = json.loads(data)
    sectionTemplate = "./templates/show.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=data)

@route("/ajax/show/<showId:int>/episode/<epId:int>")
def showEpisode(showId, epId):
    data = utils.getJsonFromFile(showId)
    data = json.loads(data)["_embedded"]["episodes"]
    for episode in data:
        if episode["id"] == epId:
            data = episode
    sectionTemplate = "./templates/episode.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=data)

run(host='localhost', port=os.environ.get('PORT', 5000), reloader=True)
