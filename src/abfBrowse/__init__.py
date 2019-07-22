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

###############################################################################################

# TODO: move all this stuff to a module

if os.path.exists(R"D:\X_Drive"):
    # server computer
    LOCAL_XRIVE_PREFIX = R"D:\X_Drive"
    AUTOANALYSIS_COMMAND_FILE = R"D:\X_Drive\Lab Documents\network\autoAnalysisFolders.txt"
else:
    # developer computer
    LOCAL_XRIVE_PREFIX = R"X:"
    AUTOANALYSIS_COMMAND_FILE = R"X:\Lab Documents\network\autoAnalysisFolders.txt"

assert os.path.exists(LOCAL_XRIVE_PREFIX)
assert os.path.exists(AUTOANALYSIS_COMMAND_FILE)

print("Path to X-Drive:", LOCAL_XRIVE_PREFIX)
print("Path to commands file:", AUTOANALYSIS_COMMAND_FILE)

###############################################################################################


def getUrl(localPath):
    url = os.path.abspath(localPath)
    url = url.replace(LOCAL_XRIVE_PREFIX, "X/")
    url = url.replace("\\", "/")
    if url.startswith("X//"):
        url = url.replace("X//", "X/")
    if ":" in LOCAL_XRIVE_PREFIX:
        url = url.replace("X", LOCAL_XRIVE_PREFIX, 1)
    print(url)
    return url


def getLocalPath(url):
    if not url.startswith("X/"):
        raise Exception("file path URLs must start with 'X/' or '/X/'")
    localPath = url.replace("X", LOCAL_XRIVE_PREFIX, 1)
    localPath = os.path.abspath(localPath)
    return localPath
