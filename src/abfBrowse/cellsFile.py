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
    def __init__(self, abfID, colorCode = "", comment = ""):
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
    def __init__(self, pathCellsFile):

        self.path = os.path.abspath(pathCellsFile)

        if os.path.exists(pathCellsFile):
            self._read()
        else:
            self.cellNotes = []
            self.abfIdsNoted = []

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

            if line.count(" ") >= 2:
                abfID, color, comment = line.split(" ", 2)
                if comment == "?":
                    comment = ""
                self.abfIdsNoted.append(abfID)
                self.cellNotes.append(CellNote(abfID, color, comment))
                continue

    def getUnknownCells(self, abfIdList):
        """Return a list of ABFs unaccounted for in cells.txt"""
        return [x for x in abfIdList if not x in self.abfIdsNoted]

    def getNoteForAbf(self, abfID):
        for note in self.cellNotes:
            if isinstance(note, CellNote) and note.abfID == abfID:
                return note
        return CellNote(abfID)

    def __repr__(self):
        justHeaders = [x for x in self.cellNotes if isinstance(x, str)]
        justCells = [x for x in self.cellNotes if isinstance(x, CellNote)]
        return "CellsFile with %d headers and %d ABFs" % (len(justHeaders), len(justCells))

        return


if __name__ == "__main__":
    cells = CellsFile(R"X:\Data\CRH-Cre\oxt-tone\OXT-preincubation\cells.txt")
    print(cells)
    print("DONE")
