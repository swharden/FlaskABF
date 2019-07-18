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
    baseNames[0] = "X:"  # TODO: pull this from somewhere else

    html = "<div class='menuFileBrowser'>"
    html += "<span class='title'>Project Browser</span><br>"
    for i in range(len(allPaths)):
        padding = "&nbsp;"*i
        # TODO: make this top level
        url = '/ABFviewer/' + allPaths[i]
        url = url.replace(abfBrowse.LOCAL_XRIVE_PREFIX, "X/")
        url = url.replace("\\", "/")
        html += f"<div>{padding}<a href='{url}' target='_top'>{baseNames[i]}</a></div>"
    html += "<hr>"
    html += abfBrowse.htmlTools.copyButton("copy path", allPaths[i])
    html += abfBrowse.htmlTools.refreshButton()
    html += "</div>"

    return html


def menuParentCellList(abfFolder):
    urlExperiment = "/ABFexperiment/" + abfFolder.path.replace("\\", "/")
    urlOrigin = "/ABForigin/" + abfFolder.path.replace("\\", "/")
    html = ""
    html += "<div class='menuEphysProject'>"
    html += "<span class='title'>Electrophysiology Project</span><br>"
    html += f"<div><a href='{urlExperiment}' target='content'>Experiment Notes</a></div>"
    html += f"<div><a href='{urlOrigin}' target='content'>Origin Commands</a></div>"
    html += "</div>"

    cells = abfBrowse.CellsFile(abfFolder.path)
    unknownCells = cells.getUnknownCells(abfFolder.abfList.family.keys())

    html += "<div class='menuCellList'>"
    for line in cells.cellNotes:
        if isinstance(line, str):
            html += f"<br><div class='title'><b>{line}</b></div>"
        elif isinstance(line, abfBrowse.CellNote):
            # TODO: make this a top level function
            abfUrl = os.path.join(abfFolder.path, line.abfID+".abf")
            abfUrl = abfUrl.replace(abfBrowse.LOCAL_XRIVE_PREFIX, "X/")
            abfUrl = abfUrl.replace("\\", "/")
            abfLink = f"<a href='/ABFparent/{abfUrl}' target='content' style='background-color: {line.color};'>{line.abfID}</a>"
            if line.abfID in abfFolder.abfList.family:
                abfCount = f"({len(abfFolder.abfList.family[line.abfID])})"
            else:
                abfCount = f"(?)"
            abfComment = f"<span class='menuCellComments'>{line.comment}</span>"
            html += f"<div>{abfLink} {abfCount} {abfComment}</div>"

    html += f"<br><div class='title'><b>Unknown:</b></div>"
    for unknownCell in unknownCells:
        # TODO: make this a top level function
        abfUrl = os.path.join(abfFolder.path, unknownCell+".abf")
        abfUrl = abfUrl.replace(abfBrowse.LOCAL_XRIVE_PREFIX, "X/")
        abfUrl = abfUrl.replace("\\", "/")
        html += f"<div><a href='/ABFparent/{abfUrl}' target='content'>{unknownCell}</a></div>"

    html += "</div>"
    return html


def menuFolderContents(abfFolder):

    subFolders = glob.glob(abfFolder.path+"/*/")

    fileNames = abfFolder.abfList.fileNamesOther
    fileNames = [x for x in fileNames if not x.lower().endswith(".tif")]
    fileNames = [x for x in fileNames if not x.lower().endswith(".ignored")]
    fileNames = [x for x in fileNames if "." in x]

    html = ""
    if len(subFolders):
        html += "<div class='menuFileBrowser'>"
        html += "<div class='title'>Folders:</div>"
        for subFolder in subFolders:
            subFolder = os.path.basename(subFolder[:-1])
            #TODO: make this top level
            url = os.path.join(abfFolder.path, subFolder)
            url = url.replace(abfBrowse.LOCAL_XRIVE_PREFIX, "X/")
            url = url.replace("\\", "/")
            html += f"<div><a href='/ABFviewer/{url}' target='_top'>{subFolder}/</a></div>"
        html += "</div>"

    if len(fileNames):
        html += "<div class='menuFileBrowser'>"
        html += "<div class='title'>Files:</div>"
        for fileName in fileNames:
            #TODO: make this top level
            url = os.path.join(abfFolder.path, fileName)
            url = url.replace(abfBrowse.LOCAL_XRIVE_PREFIX, "X/")
            url = url.replace("\\", "/")
            html += f"<div><a href='/{url}' target='content'>{fileName}</a></div>"
        html += "</div>"

    return html


def generateHtml(pathLocal):
    """
    This is a file browser menu which displays electrophysiology
    data if ABFs are present in the current folder.
    """

    abfFolder = abfBrowse.AbfFolder(pathLocal)

    html = ""
    html += menuDirectoryNavigator(abfFolder.path)
    if len(abfFolder.abfList.fileNamesAbf):
        html += menuParentCellList(abfFolder)
    html += menuFolderContents(abfFolder)
    return abfBrowse.htmlTools.htmlPageWrap(html)
