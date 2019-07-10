import time
import os

import flask
app = flask.Flask(__name__)

import abfBrowse

XDRIVE_LETTER = "X"


@app.route('/')
def showIndex():
    html = "<h1>TEST LINKS</h1>"
    html += "<div><a href='/X/Data/CRH-Cre/oxt-tone/OXT-preincubation'>folder</a></div>"
    html += "<div><a href='/X/Data/CRH-Cre/oxt-tone/OXT-preincubation/swhlab/19709_sh_0000.tif.jpg'>file</a></div>"
    html += "<div><a href='/ABFviewer/X/Data/CRH-Cre/oxt-tone/OXT-preincubation'>ABFviewer</a></div>"
    html += "<div><a href='/ABFmenu/X/Data/CRH-Cre/oxt-tone/OXT-preincubation'>ABFmenu</a></div>"
    html += "<div><a href='/ABFparent/X/Data/CRH-Cre/oxt-tone/OXT-preincubation/18109013'>ABFparent</a></div>"
    return html


@app.route('/X/<path:pathUrl>')
def showFileOrFolder(pathUrl):

    pathLocal = os.path.join(XDRIVE_LETTER+':/', pathUrl)

    if os.path.isdir(pathLocal):
        return f"directory index of [{pathLocal}]"
    elif os.path.isfile(pathLocal):
        return flask.send_file(pathLocal)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFviewer/X/<path:pathUrl>')
def showAbfView(pathUrl):

    pathLocal = os.path.join(XDRIVE_LETTER+':/', pathUrl)

    if os.path.isdir(pathLocal):
        html = f"""
            <html>
            <head><title>ABF Browser</title></head>
            <frameset cols='300px,100%'>
                <frame name='menu' src='/ABFmenu/X/{pathUrl}' />
                <frame name='content' src='/ABFfolder/X/{pathUrl}' />
            </frameset>
            </html>"""
        return html
    else:
        return f"ERROR: does not exist [{pathUrl}]"


@app.route('/ABFmenu/X/<path:pathUrl>')
def showAbfMenu(pathUrl):

    pathLocal = os.path.join(XDRIVE_LETTER+':/', pathUrl)

    if os.path.isdir(pathLocal):
        fldr = abfBrowse.AbfFolder(pathLocal)
        html = abfBrowse.pageMenu(fldr)
        html = html.replace(XDRIVE_LETTER+":/", "X/")
        return html
    else:
        return f"ERROR: does not exist [{pathLocal}]"


@app.route('/ABFparent/X/<path:pathUrl>')
def showAbfParent(pathUrl):

    pathLocal = os.path.join(XDRIVE_LETTER+':/', pathUrl)

    if os.path.isfile(pathLocal+".abf"):
        pathFolder = os.path.dirname(pathLocal)
        parentId = os.path.basename(pathLocal)
        fldr = abfBrowse.AbfFolder(pathFolder)
        html = abfBrowse.pageParent(fldr, parentId)
        html = html.replace(XDRIVE_LETTER+":/", "/X/")
        return html
    else:
        return f"ERROR: does not exist: [{pathLocal}.abf]"


@app.route('/ABFfolder/X/<path:pathUrl>')
def showAbfFolder(pathUrl):

    pathLocal = os.path.join(XDRIVE_LETTER+':/', pathUrl)

    if os.path.isdir(pathLocal):
        fldr = abfBrowse.AbfFolder(pathLocal)
        return str(fldr)
    else:
        return f"ERROR: does not exist [{pathLocal}]"


if __name__ == '__main__':
    app.run(host="192.168.1.225", port="8080")
