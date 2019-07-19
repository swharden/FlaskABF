"""
Some ABF folders contain a cells.txt file which helps document cell
groups at experiment time. 
* Only parent ABFs are listed in this file.
* lines starting with # are ignored
* lines starting with --- display text but do nothing else
* ABF lines have the space-seaprated format "abfID colorCode comment"
* comments can contain spaces and commas

Methods in this file read/write cells notes files.
"""

import os
import shutil
import time

COLORCODES = {
    "": "#FFFFFF",
    "?": "#EEEEEE",
    "g": "#00FF00",
    "g1": "#00CC00",
    "g2": "#009900",
    "b": "#FF9999",
    "i": "#CCCCCC",
    "s": "#CCCCFF",
    "s1": "#9999DD",
    "s2": "#6666BB",
    "s3": "#333399",
    "w": "#FFFF00"
}


class CellNote:
    def __init__(self, abfID, colorCode="", comment=""):
        self.abfID = abfID
        self.colorCode = colorCode
        self.comment = comment
        self.color = self.colorFromCode(colorCode)

    def colorFromCode(self, colorCode):
        for code in COLORCODES:
            if colorCode == code:
                return COLORCODES[code]
        return COLORCODES[""]

    def __repr__(self):
        return f"CellNote: [{self.abfID}] [{self.color}] [{self.comment}]"


class CellsFile:
    def __init__(self, abfFolder, cellsFileName="cells.txt"):

        self.path = os.path.join(abfFolder, cellsFileName)
        self.path = os.path.abspath(self.path)

        if os.path.exists(self.path):
            self._read()
        else:
            self.cellNotes = []
            self.abfIdsNoted = []
            print(f"warning: cells file does not exist [{self.path}]")

    def _read(self):

        self.cellNotes = []
        self.abfIdsNoted = []

        with open(self.path) as f:
            raw = f.read().split("\n")
        header = "no header"
        for line in raw:
            line = line.strip()
            if line.startswith("#"):
                continue
            if len(line) < 3:
                continue

            headerDesignator = "---"
            if line.startswith(headerDesignator):
                line = line.replace(headerDesignator, "", 1).strip()
                self.cellNotes.append(line)
                continue

            if line.strip().count(" ") == 1:
                line += " ?"

            if line.count(" ") >= 2:
                abfID, color, comment = line.split(" ", 2)
                if comment == "?":
                    comment = ""
                self.abfIdsNoted.append(abfID)
                self.cellNotes.append(CellNote(abfID, color, comment))
                continue

    def getUnknownCells(self, abfIdList):
        """Return a list of ABFs unaccounted for in the cells file"""
        return [x for x in abfIdList if not x in self.abfIdsNoted]

    def getNoteForAbf(self, abfID):
        for note in self.cellNotes:
            if isinstance(note, CellNote) and note.abfID == abfID:
                return note
        return CellNote(abfID)

    def _backup(self, subFolderName):
        saveFolderPath = os.path.join(
            os.path.dirname(self.path), subFolderName)
        if not os.path.isdir(saveFolderPath):
            print("ERROR: not a folder:", saveFolderPath)
            return
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        oldName = os.path.splitext(os.path.basename(self.path))[0]
        fileName = f"{oldName}-backup-{timestamp}.txt"
        backupFilePath = os.path.join(saveFolderPath, fileName)
        if not os.path.exists(backupFilePath):
            print(">> BACKED UP:", backupFilePath)
            shutil.copy(self.path, backupFilePath)

    def modify(self, abfID, colorCode, comment, backupSubFolderName):
        self._backup(backupSubFolderName)

        if comment.strip() == "":
            comment = "?"

        print("cells file:", self.path)
        print("modifying note for:", abfID)
        print("setting color:", colorCode)
        print("setting comment:", comment)

        newCellsLine = f"{abfID} {colorCode} {comment}"

        with open(self.path) as f:
            lines = f.read().split("\n")
        for i, line in enumerate(lines):
            if line.startswith(abfID):
                print(">> REPLACING:", line)
                print(">> WITH THIS:", newCellsLine)
                lines[i] = newCellsLine
                break
        else:
            print(">> NEW LINE:", newCellsLine)
            lines.append(newCellsLine)
        
        with open(self.path, 'w') as f:
            f.write("\n".join(lines))
        print(">> SAVED:", self.path)

    def __repr__(self):
        justHeaders = [x for x in self.cellNotes if isinstance(x, str)]
        justCells = [x for x in self.cellNotes if isinstance(x, CellNote)]
        return "CellsFile with %d headers and %d ABFs" % (len(justHeaders), len(justCells))