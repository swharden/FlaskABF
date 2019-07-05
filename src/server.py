import time
import os

import flask
app = flask.Flask(__name__)

import indexer
import views


@app.route('/')
def index():
    html = "<h1>Index Page</h1>"
    html += "<div><a href='/C/'>/C/</a></div>"
    html += "<div><a href='/X/'>/X/</a></div>"
    return views.htmlAround(html)


XDRIVE_LETTER = "C"


@app.route('/'+XDRIVE_LETTER+'/', defaults={'req_path': ''})
@app.route('/'+XDRIVE_LETTER+'/<path:req_path>')
def showPage_path(req_path):

    abs_path = os.path.join(XDRIVE_LETTER+':/', req_path)

    if not os.path.exists(abs_path):
        return f"NOT EXIST: {abs_path}"

    if os.path.isfile(abs_path):
        return flask.send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path))

    t1 = time.perf_counter()
    htmlDirList = indexer.folder(abs_path)
    return views.htmlAround(htmlDirList, t1)


if __name__ == '__main__':
    app.run()
