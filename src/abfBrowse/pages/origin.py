
import os
import abfBrowse

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    html=""
    if len(abfFolder.abfList.abfIDs):
        html += "This section is under development. Eventually it will let you create custom copy/paste blocks of Origin commands."
    else:
        html += "this is not an ABF folder..."
    return abfBrowse.htmlTools.htmlPageWrap(html)
