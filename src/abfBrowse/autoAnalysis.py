import os
import abfBrowse

COMMANDS_FILE_OLD = R"X:\Lab Documents\network\htdocs\SWHLabPHP\recode\src\scripts\commands.txt"


def addNewAbfsToCommandList(abfFolderLocalPath):
    abfFolder = abfBrowse.AbfFolder(abfFolderLocalPath)
    unanalyzedAbfs = abfFolder.abfsRequiringAnalysis()

    with open(COMMANDS_FILE_OLD) as f:
        commands = f.read()
    abfsToAdd = [x for x in unanalyzedAbfs if not x in commands]

    newCommands = ""
    for abfFileName in abfsToAdd:
        print(f"adding {abfFileName} to command list...")
        abfPath = os.path.join(abfFolderLocalPath, abfFileName)
        abfPath = abfPath.replace("\\", "/")
        newCommands += f"\nanalyze2 {abfPath}"

    with open(COMMANDS_FILE_OLD, 'a') as f:
        f.write(newCommands)

def getAnalysisText():
    with open(COMMANDS_FILE_OLD) as f:
        commands = f.read()
    return commands
