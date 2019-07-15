"""
This file contains classes which help manage ABF folder contents.
This aids in grouping ABFs and data images into clusteres by parent.
"""

import abfBrowse
import os
import glob


class AbfList:
    """
    ABF list family (parent/children) manager.

    ABF parents are identified by their abfID (their filename without extension).
    If any file in the file list starts with an abfID, that ABF is a parent.
    All subsequent files (alphabetically) are children.
    """

    def __init__(self, fileNames):
        assert isinstance(fileNames, list)
        self.fileNames = fileNames
        self._identifyAbfFiles()
        self._lookupFamily()

    def _identifyAbfFiles(self):
        """make separate lists of ABF and non-ABF files."""
        self.fileNamesAbf, self.fileNamesOther, self.abfIDs = [], [], []
        for fileName in sorted(self.fileNames):
            if str(fileName).lower().endswith(".abf"):
                self.fileNamesAbf.append(fileName)
                self.abfIDs.append(os.path.splitext(fileName)[0])
            else:
                self.fileNamesOther.append(fileName)

    def _lookupFamily(self):
        """update family parent/children dictionary (parents are keys)."""
        nonAbfFileList = ",".join(self.fileNamesOther)
        self.family = {"orphan": []}
        parent = "orphan"
        for fileName in self.fileNamesAbf:
            abfID = os.path.splitext(fileName)[0]
            if ","+abfID in nonAbfFileList:
                parent = abfID
                if not parent in self.family:
                    self.family[parent] = [abfID]
            else:
                self.family[parent] = self.family[parent] + [abfID]
        if len(self.family["orphan"]) == 0:
            self.family.pop("orphan")

    def __repr__(self):
        return f"ABF list with {len(self.fileNames)})"


class AnalysisFolder:

    def __init__(self, pathFolder):
        assert os.path.isdir(pathFolder)
        self.path = os.path.abspath(pathFolder)
        self.fileNames = sorted(os.listdir(self.path))

    def __repr__(self):
        return f"ABF analysis folder [{self.path}] with {len(self.fileNames)} files"


class AbfFolder:

    def __init__(self, pathFolder):
        assert os.path.isdir(pathFolder)

        self.path = os.path.abspath(pathFolder)
        self._scanThisFolder()
        self._scanAnalysisFolder()
        self.abfList = AbfList(self.fileNames)

    def _scanThisFolder(self):
        self.fileNames = sorted(os.listdir(self.path))
        if "Thumbs.db" in self.fileNames:
            self.fileNames.remove("Thumbs.db")

    def _scanAnalysisFolder(self):
        ANALYSIS_FOLDER_NAMES = ["autoAnalysis", "swhlab"]
        self.analysisFolder = None
        self.analysisFiles = []
        for folderName in ANALYSIS_FOLDER_NAMES:
            folderPath = os.path.join(self.path, folderName)
            if os.path.isdir(folderPath):
                self.analysisFolder = folderPath
                self.analysisFiles = sorted(os.listdir(folderPath))
                if "Thumbs.db" in self.analysisFiles:
                    self.analysisFiles.remove("Thumbs.db")
                return

    def __repr__(self):
        return f"ABF folder [{self.path}] with {len(self.fileNames)} files"

    def _stripExtension(self, abfID):
        """If abfID ends with .abf, strip the extension."""
        if abfID.lower().endswith(".abf"):
            return os.path.splitext(abfID)[0]
        else:
            return abfID

    def deleteChildGraphs(self, parentAbfID):
        """Delete graphs (in the analysis folder) for all children of the given parent."""
        parentAbfID = self._stripExtension(parentAbfID)
        children = self.abfList.family[parentAbfID]
        print(f"deleting graphs associated with {len(children)} child ABFs...")
        for childAbfID in children:
            analysisFiles = self.analysisFilesForAbf(childAbfID, skipTif=True)
            analysisFiles = [os.path.join(self.analysisFolder, x)
                             for x in analysisFiles]
            print(
                f"child {childAbfID} has {len(analysisFiles)} graphs to delete...")
            for fname in analysisFiles:
                print(f"  deleting {fname}")
                os.remove(fname)

    def analysisFilesForAbf(self, abfID, skipTif=False):
        """Return a list of filenames of images associated with an ABF."""
        abfID = self._stripExtension(abfID)
        analysisFiles = [x for x in self.analysisFiles if x.startswith(abfID)]
        if skipTif:
            analysisFiles = [
                x for x in analysisFiles if not ".tif." in x.lower()]
        return analysisFiles

    def abfsRequiringAnalysis(self):
        """Return a list of ABFs without associated graphs in the analysis folder."""
        abfs = []
        for abfFileName in self.abfList.fileNamesAbf:
            analysisFiles = self.analysisFilesForAbf(abfFileName, skipTif=True)
            if len(analysisFiles) == 0:
                abfs.append(abfFileName)
        return abfs

    def convertTifsOfParent(self, parentId):

        childTifFileNames = []
        for child in self.abfList.family[parentId]:
            for fileName in self.fileNames:
                if fileName.startswith(child) and fileName.endswith(".tif"):
                    childTifFileNames.append(fileName)

        tifsNeedingConversion = []
        for tifFileName in childTifFileNames:
            if not tifFileName+".jpg" in self.analysisFiles:
                tifsNeedingConversion.append(tifFileName)

        for tifFileName in tifsNeedingConversion:
            tifPath = os.path.join(self.path, tifFileName)
            jpgPath = os.path.join(self.analysisFolder, tifFileName+".jpg")
            abfBrowse.imaging.convertTifToJpg(tifPath, jpgPath)

        if len(tifsNeedingConversion):
            self._scanAnalysisFolder()