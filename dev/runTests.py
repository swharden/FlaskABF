import os
import sys

PATH_HERE = os.path.dirname(__file__)
import testPaths

sys.path.append(R"C:\Users\swharden\Documents\GitHub\FlaskABF\src")
import abfBrowse


def testMenu(folderPath):
    print(f"testing menu page for [{folderPath}]")
    html = abfBrowse.pages.menu.generateHtml(folderPath)
    with open(os.path.abspath(PATH_HERE + "/testMenu.html"), 'w') as f:
        f.write(html)


def testProject(folderPath):
    print(f"testing project page for [{folderPath}]")
    html = abfBrowse.pages.project.generateHtml(folderPath)
    with open(os.path.abspath(PATH_HERE + "/testProject.html"), 'w') as f:
        f.write(html)


def testParent(abfPath):
    print(f"testing parent page for [{abfPath}]")
    html = abfBrowse.pages.parent.generateHtml(abfPath)
    with open(os.path.abspath(PATH_HERE + "/testParent.html"), 'w') as f:
        f.write(html)

def testAnalysis(folderPath):
    print(f"testing analysis page for [{folderPath}]")
    html = abfBrowse.pages.analyze.generateHtml(folderPath)
    with open(os.path.abspath(PATH_HERE + "/testAnalysis.html"), 'w') as f:
        f.write(html)

def runAllTests(launchBrowser = True):

    for testFolder in testPaths.folders:
        testMenu(testFolder)
        testProject(testFolder)

    for testAbf in testPaths.abfs:
        testParent(testAbf)

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    #runAllTests()
    #testMenu(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P")
    #testParent(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P\19110032.abf")
    #os.system(PATH_HERE+"/testFrames.html")

    testAnalysis(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P")
    os.system(PATH_HERE+"/testAnalysis.html")

    
