import os
import pyabf
import glob

import abfBrowse


def menuDirectoryNavigator(currentPath):
    """
    Given a filesystem path, return HTML links where each subfolder
    is on a new line and nested by depth.
    """

    allPaths = [currentPath]
    baseNames = [os.path.basename(currentPath)]
    while baseNames[-1]:
        shorterPath = os.path.dirname(allPaths[-1])
        allPaths.append(shorterPath)
        baseNames.append(os.path.basename(shorterPath))
    allPaths.reverse()
    baseNames.reverse()

    # remove root drive letter
    baseNames.pop(0)
    allPaths.pop(0)

    # remove folder (server only)
    if baseNames[0] == "X_Drive":
        baseNames.pop(0)
        allPaths.pop(0)

    html = "<div class='menuFileBrowser'>"
    html += "<span class='title'>Project Browser</span><br>"
    html += "<div style='color: blue;'>X:</div>"
    for i in range(len(allPaths)):
        padding = "&nbsp;"*(i+1)
        url = abfBrowse.getUrl(allPaths[i])
        html += f"<div>{padding}<a href='/ABFviewer{url}' target='_top'>{baseNames[i]}</a></div>"
    html += "<hr>"
    html += abfBrowse.htmlTools.copyButton("copy path",
                                           abfBrowse.getXdrivePath(allPaths[i]))
    html += abfBrowse.htmlTools.refreshButton()
    html += "</div>"

    return html


def menuParentCellList(abfFolder):
    urlExperiment = "/ABFexperiment" + abfBrowse.getUrl(abfFolder.path)
    urlOrigin = "/ABForigin" + abfBrowse.getUrl(abfFolder.path)
    html = ""
    html += "<div class='menuEphysProject'>"
    html += "<span class='title'>Electrophysiology Project</span><br>"
    html += f"<div><a href='{urlExperiment}' target='content'>Experiment Notes</a></div>"
    html += f"<div><a href='{urlOrigin}' target='content'>Origin Commands</a></div>"
    html += "</div>"

    cells = abfBrowse.CellsFile(abfFolder.path)
    unknownCells = cells.getUnknownCells(abfFolder.abfList.family.keys())
    activeCellMarkerId = 0

    if len(cells.cellNotes):
        html += "<div class='menuCellList'>"
        for line in cells.cellNotes:
            if isinstance(line, str):
                html += f"<br><div class='title'><b>{line}</b></div>"
            elif isinstance(line, abfBrowse.CellNote):
                abfUrl = abfBrowse.getUrl(abfFolder.path+"/"+line.abfID+".abf")
                activeCellMarkerId += 1
                abfLink = f"<a href='/ABFparent{abfUrl}' target='content' onclick='setClicked({activeCellMarkerId})' style='background-color: {line.color};'>{line.abfID}</a>"
                if line.abfID in abfFolder.abfList.family:
                    abfCount = f"({len(abfFolder.abfList.family[line.abfID])})"
                else:
                    abfCount = f"(?)"
                abfComment = f"<span class='menuCellComments'>{line.comment}</span>"
                activeCellMarker = f"<span class='abftick' style='visibility: hidden' id='{activeCellMarkerId}'>»</span>"
                html += f"<div>{activeCellMarker}{abfLink} {abfCount} {abfComment}</div>"
        html += "</div>"

    if len(unknownCells):
        html += "<div class='menuCellList'>"
        html += f"<div class='title'><b>Unlabeled:</b></div>"
        for unknownCellID in unknownCells:
            abfUrl = abfBrowse.getUrl(abfFolder.path+"/"+unknownCellID+".abf")
            abfCount = len(abfFolder.abfList.family[unknownCellID])
            activeCellMarkerId += 1
            activeCellMarker = f"<span class='abftick' style='visibility: hidden' id='{activeCellMarkerId}'>»</span>"
            html += f"<div>{activeCellMarker}<a href='/ABFparent{abfUrl}' target='content' onclick='setClicked({activeCellMarkerId})'>{unknownCellID}</a> ({abfCount})</div>"
        html += "</div>"

    return html


def menuFolderContents(abfFolder):

    subFolders = glob.glob(abfFolder.path+"/*/")

    fileNames = abfFolder.abfList.fileNamesOther
    fileNames = [x for x in fileNames if not x.lower().endswith(".tif")]
    fileNames = [x for x in fileNames if not x.lower().endswith(".ignored")]
    fileNames = [x for x in fileNames if "." in x]

    html = ""
    if len(subFolders) or len(fileNames):
        html += "<div class='menuFileBrowser'>"
        html += "<div class='title'>Folder Contents:</div>"
        for subFolder in subFolders:
            subFolder = os.path.basename(subFolder[:-1])
            # TODO: make this top level
            url = abfBrowse.getUrl(os.path.join(abfFolder.path, subFolder))
            html += f"<div><a href='/ABFviewer{url}' target='_top'>{subFolder}/</a></div>"
        for fileName in fileNames:
            url = abfBrowse.getUrl(abfFolder.path + "/" + fileName)
            html += f"<div><a href='{url}' target='content'>{fileName}</a></div>"
        html += "</div>"

    return html


def generateHtml(pathLocal):
    """
    This is a file browser menu which displays electrophysiology
    data if ABFs are present in the current folder.
    """

    abfFolder = abfBrowse.AbfFolder(pathLocal)

    html = ""
    # html += "<style>body {background-color: #FAFAFA;}</style>"
    html += menuDirectoryNavigator(abfFolder.path)
    if len(abfFolder.abfList.fileNamesAbf):
        html += menuParentCellList(abfFolder)
    html += menuFolderContents(abfFolder)
    return abfBrowse.htmlTools.htmlPageWrap(html)
