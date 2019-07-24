"""
Code here relates to viewing/editing experiment.txt
"""

import os
import abfBrowse

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    experimentFilePath = os.path.join(pathLocal, "experiment.txt")
    xDriveFilePath = abfBrowse.getXdrivePath(experimentFilePath)
    
    if os.path.exists(experimentFilePath):
        with open(experimentFilePath) as f:
            experimentText = f.read()
    else:
        experimentText = "## Experiment Notes ##\n"
        experimentText += "Goal: \n"
        experimentText += "Animal: \n"
        experimentText += "Internal: \n"
        experimentText += "Bath: \n"
        experimentText += "Drugs: \n"

    html = ""
    html += "<div class='title' style='font-size: 150%;'>Experiment Notes</div>"
    html += f"<div><code>{xDriveFilePath}</code></div>"
    #html += "<div><i>Lasted edited on 2019-07-24 at 10:12 am (12.7 days ago)</i></div>"

    # add warnings here

    html += f"<textarea name='experimentText' class='editBox' style='margin-top: 20px;'>{experimentText}</textarea>"
    html += "<input class='submitButton' type='submit' value='SAVE' style='margin-top: 20px;' disabled>"

    html = f"<div style='padding: 20px;'>{html}</div>"

    return abfBrowse.htmlTools.htmlPageWrap(html)
