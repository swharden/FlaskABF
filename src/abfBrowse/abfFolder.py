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
        """make lists of ABF and non-ABF files."""
        self.fileNamesAbf, self.fileNamesOther = [], []
        for fileName in sorted(self.fileNames):
            if str(fileName).lower().endswith(".abf"):
                self.fileNamesAbf.append(fileName)
            else:
                self.fileNamesOther.append(fileName)

    def _lookupFamily(self):
        """update family parent/children dictionary (parents are keys)."""
        nonAbfFileList = ",".join(self.fileNamesOther)
        self.family = {}
        parent = "orphan"
        for fileName in self.fileNamesAbf:
            abfID = os.path.splitext(fileName)[0]
            if ","+abfID in nonAbfFileList:
                parent = abfID
                if not parent in self.family:
                    self.family[parent] = [abfID]
            else:
                self.family[parent] = self.family[parent] + [abfID]

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
        self.fileNames = sorted(os.listdir(self.path))
        self._scanAnalysisFolder()
        self.abfList = AbfList(self.fileNames)

    def _scanAnalysisFolder(self):
        ANALYSIS_FOLDER_NAMES = ["autoAnalysis", "swhlab"]
        self.analysisFolder = None
        self.analysisFiles = []
        for folderName in ANALYSIS_FOLDER_NAMES:
            folderPath = os.path.join(self.path, folderName)
            if os.path.isdir(folderPath):
                self.analysisFolder = folderPath
                self.analysisFiles = sorted(os.listdir(folderPath))
                return

    def __repr__(self):
        return f"ABF folder [{self.path}] with {len(self.fileNames)} files"


if __name__ == "__main__":
    fldr = AbfFolder(R"X:\Data\CRH-Cre\oxt-tone\OXT-preincubation")
    print(fldr)
    print("analysis folder:", fldr.analysisFolder)
    print(fldr.abfList)
