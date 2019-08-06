
import os
import abfBrowse
import pyabf

specialHtml = """
<div style="margin: 10px;">
<script src="file:///C:/Users/swharden/Documents/GitHub/FlaskABF/dev/originCommands.js"></script>

<div style="font-size: 150%; font-weight: bold;">Origin Command Generator</div>

<div style='margin: 10px; padding: 10px; background-color: #FFFFAA; line-height: 150%;'>

modify:
<input type="checkbox" id="modifyNames" onchange="createCommands();" checked> names,
<input type="checkbox" id="modifyTags" onchange="createCommands();"> tags
<br> protocol: <select id="protocolList" onchange="createCommands();"></select>

<br> analysis command: <input id='customCommand' oninput="createCommands();" size="40">
<button type="button" onclick="cmdAdd('memtest');createCommands();">memtest</button>
<button type="button" onclick="cmdAdd('getstats');createCommands();">getstats</button>
<button type="button" onclick="cmdAdd('cjfmini');createCommands();">cjfmini</button>
<button type="button" onclick="cmdAdd('clear');createCommands();">clear</button>

</div>

<textarea id="originCommands" style='margin: 10px; padding: 10px; width: 95%; height: 80%; background-color: #EEE;'></textarea>
"""

def getDataLine(abfFilePath):
    abf = pyabf.ABF(abfFilePath, loadData=False)
    comments = " | ".join(abf.tagComments)
    abfPath = abfBrowse.getXdrivePath(abfFilePath)
    return f"ABF: {abfPath}, {abf.protocol}, {comments}"


def getJavaBlock(abfFolder):

    fam = abfFolder.abfList.family
    cells = abfBrowse.CellsFile(abfFolder.path)
    unknownCells = cells.getUnknownCells(abfFolder.abfList.family.keys())

    html = "# DATA FOR JAVASCRIPT\n"

    for cell in unknownCells:
        html += cell+"\n"

    for line in cells.cellNotes:
        if isinstance(line, str):
            html += f"GROUP: {line} \n"
        if isinstance(line, abfBrowse.cellsFile.CellNote):
            for childID in fam[line.abfID]:
                html += getDataLine(f"{abfFolder.path}/{childID}.abf") + "\n"

    if len(unknownCells):
        html += f"GROUP: UNKNOWN \n"
        for childID in unknownCells:
            html += getDataLine(f"{abfFolder.path}/{childID}.abf") + "\n"

    html = f"<div style='color: #AAA; background-color: #EEE; padding: 10px; margin: 10px;' id='cellListBlock'><pre id='cellList'>{html}</pre></div>"
    return html


def readOriginCommandScript():
    jsPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jsPath = os.path.join(jsPath, "originCommands.js")
    with open(jsPath) as f:
        raw = f.read()
    return f"<script>{raw}</script>"

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    html = ""
    html += readOriginCommandScript()
    html += specialHtml
    if len(abfFolder.abfList.abfIDs):
        html += getJavaBlock(abfFolder)
    else:
        html += "this is not an ABF folder..."
    html = f"<div style='margin: 10px;'>{html}</div>"
    return abfBrowse.htmlTools.htmlPageWrap(html)
