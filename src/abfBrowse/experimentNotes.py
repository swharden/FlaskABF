import os
import shutil
import time
import datetime

class ExperimentNotes:
    def __init__(self, abfFolderPath):
        assert isinstance(abfFolderPath, str)
        self.abfFolderPath = os.path.abspath(abfFolderPath)
        assert os.path.exists(self.abfFolderPath)
        self.path = os.path.join(self.abfFolderPath, "experiment.txt")
        self.backupFolder = os.path.join(self.abfFolderPath, "swhlab")
    
    def getEditDateString(self):
        if os.path.exists(self.path):
            modEpoch = os.path.getmtime(self.path)
            modDT = datetime.datetime.fromtimestamp(int(modEpoch))
            secondsAgo = time.time() - modEpoch
            secondsInADay = 60 * 60 * 24
            daysAgo = secondsAgo / secondsInADay
            s = f"Lasted edited on {modDT.date()} at {modDT.time()} ({round(daysAgo, 2)} days ago)"
            return s
        else:
            return "file does not exist"

    def getText(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                raw = f.read()
            return raw
        else:
            return None

    def _backup(self):
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        oldName = os.path.splitext(os.path.basename(self.path))[0]
        backupFileName = f"{oldName}-backup-{timestamp}.txt"
        backupFilePath = os.path.join(self.backupFolder, backupFileName)
        if os.path.exists(self.backupFolder):
            if os.path.exists(backupFilePath):
                print("backup file already exists")
            else:
                shutil.copy(self.path, backupFilePath)
                print("created new backup:", backupFilePath)
        else:
            print("folder does not exist:", self.backupFolder)

    def write(self, text):
        self._backup()
        assert isinstance(text, str)
        text = text.replace("\r", "")
        with open(self.path, 'w') as f:
            f.write(text)
        print("wrote", self.path)
