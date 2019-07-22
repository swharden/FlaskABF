import os
import glob

from PIL import Image
from PIL import ImageOps
from PIL import ImageMath

def convertTifToJpg(tifFilePath, jpgFilePath, autoContrast = True):
    print("  converting", os.path.basename(tifFilePath), "to jpg...")
    im = Image.open(tifFilePath)
    if im.mode == "F":
        im = ImageMath.eval("convert(a/8, 'L')", a=im)
    if autoContrast:
        im = ImageOps.autocontrast(im,.05)
    im = im.convert('RGB')
    im.save(jpgFilePath)
    return


# if __name__=="__main__":
#     print("TEST")
#     testIn = R"X:\Data\GLP-eYFP\round 3 - new experiment series\experiment 1 - electrical stimulation\19722000.tif"
#     testOut = r"C:\Users\swharden\Documents\temp\test.jpg"
#     convertTifToJpg(testIn, testOut)