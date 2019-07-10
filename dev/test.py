import os
import sys

PATH_HERE = os.path.dirname(__file__)

sys.path.append(R"C:\Users\swharden\Documents\GitHub\FlaskABF\src")
import abfBrowse


def testMenu(abfFolderPath):
    fldr = abfBrowse.AbfFolder(abfFolderPath)
    pathFileOut = os.path.abspath(PATH_HERE + "/testMenu.html")
    with open(pathFileOut, 'w') as f:
        f.write(abfBrowse.pageMenu(fldr))
        print("wrote", pathFileOut)

def testParent(abfIdPath):
    fldr = abfBrowse.AbfFolder(os.path.dirname(abfIdPath))
    parentID = os.path.basename(abfIdPath)
    pathFileOut = os.path.abspath(PATH_HERE + "/testParent.html")
    with open(pathFileOut, 'w') as f:
        f.write(abfBrowse.pageParent(fldr, parentID))
        print("wrote", pathFileOut)

if __name__ == "__main__":
    testMenu(R"X:\Data\CRH-Cre\oxt-tone\OXT-preincubation")
    testParent(R"X:\Data\CRH-Cre\oxt-tone\OXT-preincubation\19709_sh_0015")
    print("DONE")
