import os

import abfBrowse


def pageParent(abfFolder, parentAbfId=None):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)

    if not parentAbfId and len(abfFolder.abfList.family):
        parentAbfId = list(abfFolder.abfList.family.keys())[0]

    html = ""
    html += f"<h1>Parent {parentAbfId}</h1>"

    if parentAbfId in abfFolder.abfList.family.keys():
        for child in abfFolder.abfList.family[parentAbfId]:
            for analysisFile in abfFolder.analysisFiles:
                if analysisFile.startswith(child):
                    imagePath = os.path.join(
                        abfFolder.analysisFolder, analysisFile)
                    imageUrl = imagePath.replace("\\", "/")
                    html += f"<a href='{imageUrl}'><img src='{imageUrl}' height='200'></a> "
    else:
        html += f"ERROR: [{parentAbfId}] is not a parent."

    return html


def pageMenu(abfFolder):
    assert isinstance(abfFolder, abfBrowse.AbfFolder)

    html = ""
    html += "<h1>menu</h1>"

    for parent in abfFolder.abfList.family.keys():
        parentUrl = os.path.join(abfFolder.path, parent).replace("\\", "/")
        childCount = len(abfFolder.abfList.family[parent])
        html += f"<div><a href='/ABFparent/{parentUrl}' target='content'>{parent}</a> ({childCount})</div>"

    return html
