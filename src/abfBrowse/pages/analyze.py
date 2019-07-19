"""
?????????????????????????
"""

import os
import abfBrowse


def generateHtml(pathLocal):
    abfBrowse.autoAnalysis.addFolder(pathLocal)

    html = "<h2>Added autoanalysis folder:</h2>"
    html += f"<div><code>{pathLocal}</code></div>"

    folderList = abfBrowse.autoAnalysis.getAnalysisText()
    folderList = folderList.replace("\n", "<br>")

    html += "<h2>Current folder list:</h2>"
    html += f"<div><code>{folderList}</code></div>"

    return abfBrowse.htmlTools.htmlPageWrap(html)
