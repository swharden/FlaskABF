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

def testExperiment(folderPath):
    print(f"testing experiment page for [{folderPath}]")
    html = abfBrowse.pages.experiment.generateHtml(folderPath)
    with open(os.path.abspath(PATH_HERE + "/testExperiment.html"), 'w') as f:
        f.write(html)

def runAllTests(launchBrowser = True):

    for testFolder in testPaths.folders:
        testMenu(testFolder)
        testProject(testFolder)

    for testAbf in testPaths.abfs:
        testParent(testAbf)

    print("ALL TESTS PASSED")

def test_makepage_parent(parentAbfPath, launchBrowser = True):
    testMenu(os.path.dirname(parentAbfPath))
    testParent(parentAbfPath)
    if launchBrowser:
        os.system(PATH_HERE+"/testFrames.html")

if __name__ == "__main__":
    test_makepage_parent(R"X:\Data\AT1-Cre\nodose Chr2 injection NTS\data\18525042.abf")

    #runAllTests()

    #testAnalysis(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P")
    #os.system(PATH_HERE+"/testAnalysis.html")

    #testExperiment(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P")
    #os.system(PATH_HERE+"/testExperiment.html")

    #fldr = abfBrowse.AbfFolder(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2018-05-30 pPIR CCh")
    #fldr.convertTifsToJpeg()