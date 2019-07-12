import time
import os

import flask
from flask import request
app = flask.Flask(__name__)

import abfBrowse


def localPathFromUrl(url):
    """Convert a URL to a local path (/X/ -> drive letter)"""
    if url.startswith("X/"):
        url = url[2:]
    localPath = os.path.join(abfBrowse.LOCAL_DRIVE_LETTER+':/', url)
    return localPath

def replaceLocalPath(html):
    """Convert local paths to URL format (drive letter -> /X/)"""
    html = html.replace(abfBrowse.LOCAL_DRIVE_LETTER+":/", "X/")
    return html

def showRequest(pathUrl):
    print()
    print(f"REQUEST: {pathUrl}")

@app.route('/')
def showIndex():
    html = "<h1>TEST LINKS</h1>"
    html += "<div><a href='/ABFviewer/X/Data/SD/Piriform Oxytocin/00 pilot experiments/2019-01-08 stim TR L3P'>test folder</a></div>"
    return html


@app.route('/X/<path:pathUrl>')
def showFileOrFolder(pathUrl):
    showRequest(pathUrl)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        return f"directory index of [{pathLocal}]"
    elif os.path.isfile(pathLocal):
        return flask.send_file(pathLocal)
    else:
        return f"ERROR: path does not exist [{pathLocal}]"


@app.route('/ABFviewer/X/<path:pathUrl>')
def showAbfView(pathUrl):
    showRequest(pathUrl)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.frames.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: path does not exist [{pathUrl}]"


@app.route('/ABFmenu/X/<path:pathUrl>')
def showAbfMenu(pathUrl):
    showRequest(pathUrl)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.menu.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFparent/X/<path:pathUrl>', methods=['POST', 'GET'])
def showAbfParent(pathUrl):
    showRequest(pathUrl)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isfile(pathLocal):
        if request.method == 'POST':
            try:
                abfFolderPath = request.form['abfFolderPath']
                abfID = request.form['abfID']
                colorCode = request.form['colorCode']
                comment = request.form['comment']
                print(f"updating cell notes in [{abfFolderPath}]:")
                print(f"ABFID: {abfID}, colorCode: {colorCode}, comment: {comment}")
                cellsFile = abfBrowse.CellsFile(abfFolderPath)
                cellsFile.modify(abfID, colorCode, comment, "swhlab")
                print("success!")
            except:
                print("bad POST, no change to cells file")
        html = abfBrowse.pages.parent.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist: [{pathLocal}.abf]"


@app.route('/ABFfolder/X/<path:pathUrl>')
def showAbfFolder(pathUrl):
    showRequest(pathUrl)
    pathLocal = localPathFromUrl(pathUrl)
    if os.path.isdir(pathLocal):
        html = abfBrowse.pages.project.generateHtml(pathLocal)
        return replaceLocalPath(html)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


if __name__ == '__main__':
    app.run(host="192.168.1.225", port="8080")
