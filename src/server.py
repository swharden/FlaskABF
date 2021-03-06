import time
import os
import sys

import flask
from flask import request
app = flask.Flask(__name__)

import abfBrowse


def showRequest(pathUrl, request):
    print(f"REQUEST: {request.url}")
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
    Send the binary content of a file on the X drive
    """
    #showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath("X/"+pathUrl)
    print("  serving", os.path.basename(pathLocal))
    if os.path.isdir(pathLocal):
        return f"directory index of [{pathLocal}]"
    elif os.path.isfile(pathLocal):
        return flask.send_file(pathLocal)
    else:
        return f"ERROR: path does not exist [{pathLocal}]"


@app.route('/ABFviewer/<path:pathUrl>')
def showAbfView(pathUrl):
    """
    Display a frameset containing a menu and an ABFfolder
    """
    showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath(pathUrl)
    if os.path.isdir(pathLocal):
        return abfBrowse.pages.frames.generateHtml(pathUrl)
    else:
        return f"ERROR: path does not exist [{pathUrl}]"


@app.route('/ABFmenu/<path:pathUrl>')
def showAbfMenu(pathUrl):
    """
    Display the menu for an ABF folder
    """
    showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath(pathUrl)
    if os.path.isdir(pathLocal):
        return abfBrowse.pages.menu.generateHtml(pathLocal)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFparent/<path:pathUrl>', methods=['POST', 'GET'])
def showAbfParent(pathUrl):
    """
    Display the ABF list and data for a parent ABF.
      - also processes changes to cells.txt
      - also deletes graphs for child ABFs
      - also marks ABFs as ignored
      - also analyzes new ABFs
      - also marks ABFs as ignored
    """
    showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath(pathUrl)
    if os.path.isfile(pathLocal):

        if ('colorCode' in request.form.keys()):
            print("Processing a change to cells.txt...")
            cellsFile = abfBrowse.CellsFile(request.form['abfFolderPath'])
            cellsFile.modify(
                request.form['abfID'],
                request.form['colorCode'],
                request.form['comment'],
                abfBrowse.AUTOANALYSIS_FOLDER_NAME)

        if ('deleteGraphsForChildren' in request.args.keys()):
            print("Deleting graphs for children...")
            abfFldr = abfBrowse.AbfFolder(os.path.dirname(pathLocal))
            abfFldr.deleteChildGraphs(os.path.basename(pathLocal))
            print("complete.")

        if ('ignoreABF' in request.args.keys()):
            ignoreAbf = request.args['ignoreABF']
            ignoreAbfPath = os.path.join(os.path.dirname(pathLocal), ignoreAbf)
            print(f"ignoring ABF: {ignoreAbfPath}")
            os.rename(ignoreAbfPath, ignoreAbfPath+".ignored")

        return abfBrowse.pages.parent.generateHtml(pathLocal)
    else:
        return f"ERROR: does not exist: [{pathLocal}.abf]"


@app.route('/ABForigin/<path:pathUrl>')
def showAbfOrigin(pathUrl):
    showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath(pathUrl)
    if os.path.isdir(pathLocal):
        return abfBrowse.pages.origin.generateHtml(pathLocal)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFanalyze/<path:pathUrl>')
def showAbfAnalyze(pathUrl):
    showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath(pathUrl)
    if os.path.isdir(pathLocal):
        return abfBrowse.pages.analyze.generateHtml(pathLocal)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFexperiment/<path:pathUrl>', methods=['POST', 'GET'])
def showAbfExperiment(pathUrl):
    showRequest(pathUrl, request)
    pathLocal = abfBrowse.getLocalPath(pathUrl)
    if os.path.isdir(pathLocal):
        if ('experimentText' in request.form.keys()):
            exp = abfBrowse.experimentNotes.ExperimentNotes(pathLocal)
            exp.write(request.form['experimentText'])
        return abfBrowse.pages.experiment.generateHtml(pathLocal)
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
