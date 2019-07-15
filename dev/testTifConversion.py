import glob
import os
import sys

sys.path.append(R"C:\Users\swharden\Documents\GitHub\FlaskABF\src")
import abfBrowse

if __name__=="__main__":
    tifFolder=R"C:\Users\swharden\Documents\temp\test"
    outFolder=R"C:\Users\swharden\Documents\temp\test\jpg"
    for tifFile in glob.glob(tifFolder+"/*.tif"):
        outFile = os.path.join(outFolder, os.path.basename(tifFile)+".jpg")
        abfBrowse.imaging.convertTifToJpg(tifFile, outFile)