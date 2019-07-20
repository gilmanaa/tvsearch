import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, TEMPLATE_PATH, error)
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
def browse():
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

@route("/ajax/show/<id>")
def showShow(id):
    if utils.show_shows(id) == "error":
        return redirect('/error')
    template_string = utils.show_shows(id)
    template_slice = template_string.split('<section id="dynamic">')[1]
    template_slice = template_slice.split("</section>")[0]
    return template_slice

@route("/show/<id>")
def showShow(id):
    show = utils.show_shows(id)
    if show == "error":
        return redirect('/error')
    return show

@route("/ajax/show/<showId>/episode/<epId>")
def showEpisode(showId, epId):
    if utils.show_episodes(showId, epId) == "error":
        return redirect('/error')
    template_string = utils.show_episodes(showId, epId)
    template_slice = template_string.split('<section id="dynamic">')[1]
    template_slice = template_slice.split("</section>")[0]
    return template_slice

@route("/show/<showId>/episode/<epId>")
def showEpisode(showId, epId):
    episode = utils.show_episodes(showId, epId)
    if episode == "error":
        return redirect('/error')
    return episode

@route('/error')
def errors():
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})

run(host='localhost', port=os.environ.get('PORT', 5000), reloader=True)
