
import os
import abfBrowse

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    html=""
    if len(abfFolder.abfList.abfIDs):
        html += "origin commands for an ABF folder"
    else:
        html += "this is not an ABF folder..."
    return abfBrowse.htmlTools.htmlPageWrap(html)
