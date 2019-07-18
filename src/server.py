import time
import os
import sys

import flask
from flask import request
app = flask.Flask(__name__)

import abfBrowse


def localPathFromUrl(url):
    """Convert a URL to a local path (/X/ -> drive letter)"""
    url = url.replace("XData", "Data") #TODO: why?
    localPath = os.path.join(abfBrowse.LOCAL_XRIVE_PREFIX, url)
    localPath = os.path.abspath(localPath)
    return localPath


def replaceLocalPath(html):
    """Convert local paths to URL format (drive letter -> /X/)"""
    html = html.replace(abfBrowse.LOCAL_XRIVE_PREFIX, "X")
    return html


def showRequest(pathUrl, request):
    print()
    print(f"REQUEST: {pathUrl}")
    for key in request.args.keys():
        print(f"GET['{key}']={request.args[key]}")
    for key in request.form.keys():
        print(f"POST['{key}']={request.form[key]}")


@app.route('/')
def showIndex():
    html = "<h1>TEST LINKS</h1>"
    html += "<div><a href='/ABFviewer/X/Data/SD/Piriform Oxytocin/00 pilot experiments/2019-01-08 stim TR L3P'>test folder</a></div>"
    return html


@app.route('/X/<path:pathUrl>')
def showFileOrFolder(pathUrl):
    """
    Display the front page
    """
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        return f"directory index of [{pathLocal}]"
    elif os.path.isfile(pathLocal):
        return flask.send_file(pathLocal)
    else:
        return f"ERROR: path does not exist [{pathLocal}]"


@app.route('/ABFviewer/X/<path:pathUrl>')
def showAbfView(pathUrl):
    """
    Display a frameset containing a menu and an ABFfolder
    """
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.frames.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: path does not exist [{pathUrl}]"


@app.route('/ABFmenu/X/<path:pathUrl>')
def showAbfMenu(pathUrl):
    """
    Display the menu for an ABF folder
    """
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.menu.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFparent/X/<path:pathUrl>', methods=['POST', 'GET'])
def showAbfParent(pathUrl):
    """
    Display the ABF list and data for a parent ABF.
      - also processes changes to cells.txt
      - also deletes graphs for child ABFs
      - also marks ABFs as ignored
      - also analyzes new ABFs
    """
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isfile(pathLocal):

        if ('colorCode' in request.form.keys()):
            print("Processing a change to cells.txt...")
            cellsFile = abfBrowse.CellsFile(request.form['abfFolderPath'])
            cellsFile.modify(
                request.form['abfID'],
                request.form['colorCode'],
                request.form['comment'],
                "swhlab")

        if ('deleteGraphsForChildren' in request.args.keys()):
            print("Deleting graphs for children...")
            abfFldr = abfBrowse.AbfFolder(os.path.dirname(pathLocal))
            abfFldr.deleteChildGraphs(os.path.basename(pathLocal))
            print("complete.")

        html = abfBrowse.pages.parent.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist: [{pathLocal}.abf]"


@app.route('/ABForigin/X/<path:pathUrl>')
def showAbfOrigin(pathUrl):
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.origin.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFanalyze/X/<path:pathUrl>')
def showAbfAnalyze(pathUrl):
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.analyze.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFexperiment/X/<path:pathUrl>')
def showAbfExperiment(pathUrl):
    showRequest(pathUrl, request)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.experiment.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print("WARNING: invalid command line arguments")
        print("EXAMPLE USAGE: server.py -ip 192.168.0.123 -port 1234")
        ip = "127.0.0.1"
        port = 8080
        print("using default IP and PORT")
    else:
        ip = sys.argv[2]
        port = sys.argv[4]

    print(f"Serving on: http://{ip}:{port}")
    app.run(host=ip, port=port)
