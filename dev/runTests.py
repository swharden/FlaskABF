import os
import sys

PATH_HERE = os.path.dirname(os.path.abspath(__file__))
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

def testOrigin(folderPath):
    print(f"testing origin page for [{folderPath}]")
    html = abfBrowse.pages.origin.generateHtml(folderPath)
    with open(os.path.abspath(PATH_HERE + "/testOrigin.html"), 'w') as f:
        f.write(html)

def runAllTests(launchBrowser = True):

    for testFolder in testPaths.folders:
        testMenu(testFolder)
        testProject(testFolder)

    for testAbf in testPaths.abfs:
        testParent(testAbf)

    print("ALL TESTS PASSED")

def test_makepage_parent(parentAbfPath, launchBrowser = False):
    testMenu(os.path.dirname(parentAbfPath))
    testParent(parentAbfPath)
    if launchBrowser:
        os.system(PATH_HERE+"/testFrames.html")

def test_makepage_experiment(parentAbfPath, launchBrowser = False):
    testExperiment(os.path.dirname(parentAbfPath))
    os.system(PATH_HERE+"/testExperiment.html")

def test_makepage_origin(parentAbfPath, launchBrowser = False):
    testOrigin(parentAbfPath)
    if launchBrowser:
        os.system(PATH_HERE+"/testOrigin.html")

def test_json_abfFolder(folderPath):
    print(f"creating JSON for abf folder: {folderPath}")
    abfFolder = abfBrowse.AbfFolder(folderPath)
    print()
    print(abfFolder.toJSON())
    #filePathOut = os.path.abspath(PATH_HERE + "/testProject.json")
    #with open(os.path.abspath(filePathOut), 'w') as f:
        #f.write(html)
    #print(f"wrote: {filePathOut}")

if __name__ == "__main__":

    test_json_abfFolder(R"X:\Data\F344\Aging BLA\basal excitability round2\abfs")

    #test_makepage_origin(R"X:\Data\F344\Aging BLA\basal excitability round2\abfs", False)
    #test_makepage_origin(R"X:\Data\F344\Aging BLA\basal excitability round3\abfs-intrinsics", False)

    #test_makepage_parent(R"X:\Data\GLP-eYFP\round 2 - ChR2 in nodose\abfs\19517000.abf")
    
    #test_makepage_experiment(R"X:\Data\GLP-eYFP\round 2 - ChR2 in nodose\abfs")

    #runAllTests()

    #testAnalysis(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P")
    #os.system(PATH_HERE+"/testAnalysis.html")

    #testExperiment(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2019-01-08 stim TR L3P")
    #os.system(PATH_HERE+"/testExperiment.html")

    #fldr = abfBrowse.AbfFolder(R"X:\Data\SD\Piriform Oxytocin\00 pilot experiments\2018-05-30 pPIR CCh")
    #fldr.convertTifsToJpeg()