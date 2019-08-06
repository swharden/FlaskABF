
import os
import abfBrowse
import pyabf

def getDataLine(abfFilePath):
    abf = pyabf.ABF(abfFilePath, loadData=False)
    comments = " | ".join(abf.tagComments)
    return f"{abf.abfID}, {abf.protocol}, {comments}"

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

    html = f"<div style='color: #AAA; background-color: #EEE; padding: 10px;'><pre id='cellList'>{html}</pre></div>"
    return html

def generateHtml(pathLocal):

    abfFolder = abfBrowse.AbfFolder(pathLocal)
    html=""
    if len(abfFolder.abfList.abfIDs):
        html += "<div style='font-size: 150%; font-weight: bold;'>Origin Command Generator</div>"
        html += "<div><i>this page is being actively developed...</i></div>"
        html += getJavaBlock(abfFolder)    
    else:
        html += "this is not an ABF folder..."
    html = f"<div style='margin: 10px;'>{html}</div>"
    return abfBrowse.htmlTools.htmlPageWrap(html)
