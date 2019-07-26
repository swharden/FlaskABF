"""
Code here relates to viewing/editing experiment.txt
"""

import os
import abfBrowse


def getNotesForm(pathLocal):

    expNotes = abfBrowse.experimentNotes.ExperimentNotes(pathLocal)
    xDriveFilePath = abfBrowse.getXdrivePath(expNotes.path)
    experimentText = expNotes.getText()
    if not experimentText:
        experimentText = "## Experiment Notes ##\n"
        experimentText += "Goal: \n"
        experimentText += "Animal: \n"
        experimentText += "Internal: \n"
        experimentText += "Bath: \n"
        experimentText += "Drugs: \n"

    url = "/ABFexperiment" + abfBrowse.getUrl(pathLocal)
    url = url.replace("X:/", "/X/")

    html = ""
    html += f"<div style='font-size: 80%; font-family: consolas, monospace;'>{xDriveFilePath}</div>"
    html += f"<div style='color: #ccc; font-size: 80%;'><i>{expNotes.getEditDateString()}</i></div>"

    # add warnings here

    html += f"<form action='{url}' method='post' style='margin: 0px;'>"
    html += f"<textarea name='experimentText' class='editBox' style='margin-top: 20px;'>{experimentText}</textarea>"
    html += f"<input class='submitButton' type='submit' value='SAVE' style='margin-top: 20px;'>"
    html += f"</form>"

    return html


def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)

    html = "<div class='title' style='font-size: 150%;'>Experiment Notes</div>"

    if len(abfFolder.abfList.abfIDs):
        html += getNotesForm(pathLocal)
    else:
        html += '<i>this is not an ABF folder</i>'

    html = f"<div style='padding: 20px;'>{html}</div>"
    return abfBrowse.htmlTools.htmlPageWrap(html)
