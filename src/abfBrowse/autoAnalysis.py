import os
import abfBrowse

def addFolder(abfFolderLocalPath):

    with open(abfBrowse.AUTOANALYSIS_COMMAND_FILE) as f:
        analysisPaths = f.read()

    if not abfFolderLocalPath in analysisPaths:
        with open(abfBrowse.AUTOANALYSIS_COMMAND_FILE, 'a') as f:
            f.write(abfFolderLocalPath+"\n")
        print("  Added autoanalysis folder:", abfFolderLocalPath)


def getAnalysisText():
    with open(abfBrowse.AUTOANALYSIS_COMMAND_FILE) as f:
        commands = f.read()
    return commands
