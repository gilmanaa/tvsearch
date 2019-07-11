import os
from bottle import (get, post, redirect, request, route, run, static_file,template)
import utils
import json

# Static Routes
@route('/search')
def search_page():
    sectionTemplate = os.path.dirname(__file__) + "/templates/search.tpl"
    return template(os.path.dirname(__file__) + "/pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})

@route('/browse')
def browse_page():
    data = utils.getJsonFromFile("7")
    data1 = json.loads(data)
    dataArr = [data1]
    sectionTemplate = os.path.dirname(__file__) + "/templates/browse.tpl"
    return template(os.path.dirname(__file__) + "/pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=dataArr)

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
    sectionTemplate = os.path.dirname(__file__) + "/templates/home.tpl"
    return template(os.path.dirname(__file__) + "/pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

run(host='localhost', port=os.environ.get('PORT', 5000))
