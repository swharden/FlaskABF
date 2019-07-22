"""
The parent page shows a parent ABF and its children (and images),
and provides inputs to allow updating cells.txt with color and comment.
"""

import os
import pyabf

import abfBrowse


def pageParentHeader(abfFolder, parentNote):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)
    assert isinstance(parentNote, abfBrowse.cellsFile.CellNote)
    html = ""
    html += f"<div style='background-color: {parentNote.color}; padding: .5em;'>"
    html += f"<span class='title'>PARENT: {parentNote.abfID}</span> "
    #html += abfBrowse.htmlTools.copyButton("copy path", abfFolder.path)
    html += "</div>"
    return html


def getColorBoxesHTML(currentColorCode=""):
    html = ""
    html += "<div style='margin-top: .5em; margin-bottom: .5em;'>"
    for colorCode in abfBrowse.cellsFile.COLORCODES:
        color = abfBrowse.cellsFile.COLORCODES[colorCode]
        checked = "checked" if colorCode == currentColorCode else ""
        html += f"""
        <span style='margin: 2px; padding: 5px;  border: solid 1px black; background-color: {color};'>
        <input type='radio' name='colorCode' value='{colorCode}' {checked} >
        </span>
        """
    html += "</div>"
    return html


def pageParentNotes(abfFolder, parentNote):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)
    assert isinstance(parentNote, abfBrowse.cellsFile.CellNote)

    abfPath = os.path.join(abfFolder.path, parentNote.abfID) + ".abf"
    url = "/ABFparent" + abfBrowse.getUrl(abfPath)
    urlMenu = "/ABFmenu" + abfBrowse.getUrl(os.path.dirname(abfPath))

    html = ""
    html += f"<form action='{url}' method='post' style='margin: 0px;'>"
    html += f"<input type='hidden' name='abfFolderPath' value='{abfFolder.path}' />"
    html += f"<input type='hidden' name='abfID' value='{parentNote.abfID}' />"
    html += f"<div style='background-color: #DDD; padding: .5em;'>"
    html += getColorBoxesHTML(parentNote.colorCode)
    html += f"<input style='margin-top: 8px;' type='text' size='35' name='comment' value='{parentNote.comment}'> "
    html += f"<input type='submit' value='Submit'> "
    html += f"<a href='{urlMenu}' target='menu'>refresh menu</a>"
    html += "</div>"
    html += "</form>"
    return html


def pageFolderActions(abfFolder, parentNote):

    abfPath = os.path.join(abfFolder.path, parentNote.abfID) + ".abf"
    urlParent = "/ABFparent" + abfBrowse.getUrl(abfPath)
    urlAnalyze = "/ABFanalyze" + abfBrowse.getUrl(abfFolder.path)
    urlExperiment = "/ABFexperiment" + abfBrowse.getUrl(abfFolder.path)

    html = ""
    html += "<div style='background-color: #F6F6F6; padding: .5em; color: gray'>"
    html += f"<span style='color: black;' class='title'>Actions:</span> "

    unanalyzedAbfs = abfFolder.abfsRequiringAnalysis()
    if len(unanalyzedAbfs):
        html += f"<a href='{urlAnalyze}' class='abfAnalysisNeeded'>Analyze {len(unanalyzedAbfs)} new ABFs</a> | "
    else:
        html += f"<a href='{urlAnalyze}' style='color: gray;'>No ABFs require analysis</a> | "

    html += f"<a href='{urlParent}?deleteGraphsForChildren' class='' style='color: gray;'>delete graphs</a> | "
    html += f"<a href='{urlExperiment}' class=''>experiment notes</a>"
    html += "</div>"
    return html


def pageParentChildAbfList(abfFolder, parentNote):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)
    assert isinstance(parentNote, abfBrowse.cellsFile.CellNote)
    abfs = abfFolder.abfList.family[parentNote.abfID]
    abfFileNames = [x+".abf" for x in abfs]
    abfPaths = [os.path.join(abfFolder.path, x) for x in abfFileNames]

    html = ""
    html += "<div style='background-color: #EEE; padding: .5em;'>"
    html += f"<span class='title'>CHILDREN:</span>"
    for i, abfFileName in enumerate(abfFileNames):

        # use pyABF to extract useful ABF information
        abf = pyabf.ABF(abfPaths[i], loadData=False)
        clampType = "VC" if abf.adcUnits[0] == "pA" else "IC"
        sweepCount = len(abf.sweepList)
        duration = f"{round(abf.dataLengthMin, 2)} min" if abf.dataLengthMin > 1 else f"{round(abf.dataLengthSec, 2)} sec"
        comments = []
        for tagComment, tagTimeMin in zip(abf.tagComments, abf.tagTimesMin):
            comments.append("\"%s\" at %s min" %
                            (tagComment, round(tagTimeMin, 2)))
        commentsLine = ", ".join(comments)

        # determine abf type by its protocol
        isMemTest = ("memtest" in abf.protocol.lower()
                     or "membrane" in abf.protocol.lower())

        # create the HTML row for this ABF
        html += f"<div class='abfInfoRow'>{abfFileName} "
        xDrivePath = abfBrowse.getXdrivePath(abfPaths[i])
        html += abfBrowse.htmlTools.copyButton("copy path", xDrivePath)
        html += abfBrowse.htmlTools.copyButton(
            "setpath", "setpath \"%s\"; " % (xDrivePath))
        html += f"{abf.protocol}, {clampType} with {sweepCount} sweeps ({abf.sweepLengthSec} sec each, {duration} total)"

        # display messages at the end of the line
        if (len(comments)):
            html += f", <span class='abfInfoComment'>Comments: {commentsLine}</span>"
        if i == 0 and not isMemTest:
            html += f" <span class='abfInfoWarning'>WARNING: the parent ABF should be a memtest!</span>"

        html += "</div>"

    html += "</div>"
    return html

def getHtmlForImageFilePaths(abfFolder, filePaths):
    html = ""
    for imagePath in filePaths:
        imagePath = abfFolder.analysisFolder+"/"+imagePath
        imageUrl = abfBrowse.getUrl(imagePath)
        html += f"<a href='{imageUrl}'><img src='{imageUrl}' class='analysisImage'></a> "
    return html

def pageParentImages(abfFolder, parentNote):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)
    assert isinstance(parentNote, abfBrowse.cellsFile.CellNote)
    html = ""
    for child in abfFolder.abfList.family[parentNote.abfID]:
        childImages = [x for x in abfFolder.analysisFiles if x.startswith(child)]
        micrographs = [x for x in childImages if ".tif." in x.lower()]
        analysisGraphs = [x for x in childImages if not ".tif." in x.lower()]
        html += getHtmlForImageFilePaths(abfFolder, micrographs)
        html += getHtmlForImageFilePaths(abfFolder, analysisGraphs)
    return html


def generateHtml(pathLocal):
    """
    This page shows all child data for a parent ABF.
    All child images are shown.
    Options are available to edit comments for this parent.
    """

    if not os.path.exists(pathLocal):
        return f"ERROR: file does not exist: [{pathLocal}]"

    pathFolder = os.path.dirname(pathLocal)
    parentAbfFileName = os.path.basename(pathLocal)
    parentAbfId = os.path.splitext(parentAbfFileName)[0]
    abfFolder = abfBrowse.AbfFolder(pathFolder)

    if not parentAbfId and len(abfFolder.abfList.family):
        parentAbfId = list(abfFolder.abfList.family.keys())[0]

    if not parentAbfId in abfFolder.abfList.family.keys():
        html = f"ERROR: [{pathLocal}] is not a parent ABF"
        return abfBrowse.htmlTools.htmlPageWrap(html)

    cellsFile = abfBrowse.CellsFile(abfFolder.path)
    parentNote = cellsFile.getNoteForAbf(parentAbfId)

    abfFolder.convertTifsOfParent(parentAbfId)

    html = ""
    html += pageParentHeader(abfFolder, parentNote)
    html += pageParentNotes(abfFolder, parentNote)
    html += pageParentChildAbfList(abfFolder, parentNote)
    html += pageFolderActions(abfFolder, parentNote)
    html += pageParentImages(abfFolder, parentNote)
    html = abfBrowse.htmlTools.htmlPageWrap(html)

    return html
