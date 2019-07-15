"""
Code here relates to viewing/editing experiment.txt
"""

import os
import abfBrowse

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    experimentFilePath = os.path.join(pathLocal, "experiment.txt")
    html = ""
    if os.path.exists(experimentFilePath):
        with open(experimentFilePath) as f:
            experimentText = f.read()
        experimentText = experimentText.replace("\n", "<br>")
        html += "<h1>Experiment Notes</h1>"
        html += f"<div><code>{experimentFilePath}</code></div>"
        html += f"<div class='experimentTextBlock'>{experimentText}</div>"
    else:
        html += "<div>Experiment file does not exist:</div>"
        html += f"<div><code>{experimentFilePath}</code></div>"
    return abfBrowse.htmlTools.htmlPageWrap(html)
