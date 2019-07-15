"""
?????????????????????????
"""

import os
import abfBrowse

def generateHtml(pathLocal):
    abfBrowse.autoAnalysis.addNewAbfsToCommandList(pathLocal)

    html = ""
    commands = abfBrowse.autoAnalysis.getAnalysisText()
    if len(commands):
        html += f"<h2>analyzing...</h2>"
        html += f"<code><pre>{commands}</pre></code>"
        html += abfBrowse.htmlTools.autoRefresh(1)
    else:
         html += f"analysis complete!"
    return abfBrowse.htmlTools.htmlPageWrap(html)
