"""
Code here relates to viewing/editing experiment.txt
"""

import os
import abfBrowse

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    experimentFilePath = os.path.join(pathLocal, "experiment.txt")
    xDriveFilePath = abfBrowse.getXdrivePath(experimentFilePath)
    html = ""
    html += "<div class='menuFileBrowser'>"
    html += "<div class='title'>Experiment Notes</div>"
    html += f"<div><code>{xDriveFilePath}</code></div>"
    html += "<hr>"

    html += "<div class='experimentTextBlock'>"
    if os.path.exists(experimentFilePath):
        with open(experimentFilePath) as f:
            experimentText = f.read()
        html += experimentText.replace("\n", "<br>")
    else:
        html += "file does not exist"
    html += "<div>"

    html += "</div>"

    return abfBrowse.htmlTools.htmlPageWrap(html)
