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
    html += f"<span class='title'>PARENT: {parentNote.abfID}</span>"
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
        <input type='radio' name='color' value='{colorCode}' {checked} >
        </span>
        """
    html += "</div>"
    return html


def pageParentNotes(abfFolder, parentNote):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)
    assert isinstance(parentNote, abfBrowse.cellsFile.CellNote)

    parentPath = os.path.join(abfFolder.path, parentNote.abfID+".abf")
    url = parentPath.replace("\\", "/")
    url = "/ABFparent/" + url
    url = url.replace("//", "/")

    html = ""
    html += f"<form action='{url}' method='get' style='margin: 0px;'>"
    html += f"<div style='background-color: #DDD; padding: .5em;'>"
    html += getColorBoxesHTML()
    html += f"<input style='margin-top: 8px;' type='text' size='35' name='comment' value='{parentNote.comment}'> "
    html += f"<input type='submit' value='Submit'> "
    html += "<a href=''>refresh menu</a>"
    html += "</div>"
    html += "</form>"
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
        html += abfBrowse.htmlTools.copyButton("copy path", abfPaths[i])
        html += abfBrowse.htmlTools.copyButton(
            "setpath", "setpath \"%s\"; " % (abfPaths[i]))
        html += f"{abf.protocol}, {clampType} with {sweepCount} sweeps ({abf.sweepLengthSec} sec each, {duration} total)"

        # display messages at the end of the line
        if (len(comments)):
            html += f", <span class='abfInfoComment'>Comments: {commentsLine}</span>"
        if i == 0 and not isMemTest:
            html += f" <span class='abfInfoWarning'>WARNING: the parent ABF should be a memtest!</span>"

        html += "</div>"

    html += "</div>"
    return html


def pageParentImages(abfFolder, parentNote):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)
    assert isinstance(parentNote, abfBrowse.cellsFile.CellNote)
    html = ""
    for child in abfFolder.abfList.family[parentNote.abfID]:
        for analysisFile in abfFolder.analysisFiles:
            if analysisFile.startswith(child):
                imagePath = os.path.join(
                    abfFolder.analysisFolder, analysisFile)
                imageUrl = "/"+imagePath.replace("\\", "/")
                html += f"<a href='{imageUrl}'><img class='analysisImage' src='{imageUrl}'></a> "
    return html


def generateHtml(pathLocal):
    """
    This page shows all child data for a parent ABF.
    All child images are shown.
    Options are available to edit comments for this parent.
    """

    pathFolder = os.path.dirname(pathLocal)
    parentAbfFileName = os.path.basename(pathLocal)
    parentAbfId = os.path.splitext(parentAbfFileName)[0]
    abfFolder = abfBrowse.AbfFolder(pathFolder)

    if not parentAbfId and len(abfFolder.abfList.family):
        parentAbfId = list(abfFolder.abfList.family.keys())[0]

    if not parentAbfId in abfFolder.abfList.family.keys():
        html = f"ERROR: [{parentAbfId}] is not a parent."
        return abfBrowse.htmlTools.htmlPageWrap(html)

    cellsFile = abfBrowse.CellsFile(abfFolder.path+"/cells.txt")
    parentNote = cellsFile.getNoteForAbf(parentAbfId)

    html = ""
    html += pageParentHeader(abfFolder, parentNote)
    html += pageParentNotes(abfFolder, parentNote)
    html += pageParentChildAbfList(abfFolder, parentNote)
    html += pageParentImages(abfFolder, parentNote)
    html = abfBrowse.htmlTools.htmlPageWrap(html)

    return html
