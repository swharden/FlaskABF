from abfBrowse.abfFolder import AbfFolder
from abfBrowse.cellsFile import CellsFile, CellNote

import abfBrowse.htmlTools
import abfBrowse.autoAnalysis
import abfBrowse.imaging

import abfBrowse.pages.frames
import abfBrowse.pages.menu
import abfBrowse.pages.parent
import abfBrowse.pages.analyze
import abfBrowse.pages.experiment
import abfBrowse.pages.origin

import os

### Customize these to reflect which computer you're using ####################################

serverXdrivePath = R"D:\X_Drive"
developerXdrivePath = R"X:"

serverCommandFilePath = R"C:\Users\LabAdmin\Documents\GitHub\pyABFauto\dev\commands.txt"
developerCommandFilePath = R"C:\Users\swharden\Documents\GitHub\pyABFauto\dev\commands.txt"

###############################################################################################

if os.path.exists(serverXdrivePath):
    LOCAL_XRIVE_PREFIX = serverXdrivePath
elif os.path.exists(developerXdrivePath):
    LOCAL_XRIVE_PREFIX = developerXdrivePath
else:
    raise Exception("no local X-drive path found")
LOCAL_XRIVE_PREFIX = os.path.abspath(LOCAL_XRIVE_PREFIX)
print("Path to X-Drive:", LOCAL_XRIVE_PREFIX)

if os.path.exists(serverCommandFilePath):
    AUTOANALYSIS_COMMAND_FILE = serverCommandFilePath
elif os.path.exists(developerCommandFilePath):
    AUTOANALYSIS_COMMAND_FILE = developerCommandFilePath
else:
    raise Exception("no local commands file found")
AUTOANALYSIS_COMMAND_FILE = os.path.abspath(AUTOANALYSIS_COMMAND_FILE)
print("Path to commands file:", AUTOANALYSIS_COMMAND_FILE)


def getUrl(localPath):
    url = os.path.abspath(localPath)
    url = url.replace(LOCAL_XRIVE_PREFIX, "X/")
    url = url.replace("\\", "/")
    if url.startswith("X//"):
        url = url.replace("X//","X/")
    return url


def getLocalPath(url):
    if not url.startswith("X/"):
        raise Exception("file path URLs must start with 'X/' or '/X/'")
    localPath = url.replace("X/", LOCAL_XRIVE_PREFIX+"/", 1)
    localPath = os.path.abspath(localPath)
    return localPath