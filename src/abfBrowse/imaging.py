import os
import glob

from PIL import Image
from PIL import ImageOps

def convertTifToJpg(tifFilePath, jpgFilePath, autoContrast = True):
    print("  converting", os.path.basename(tifFilePath), "to jpg...")
    im = Image.open(tifFilePath)
    im = im.convert('RGB')
    if autoContrast:
        im = ImageOps.autocontrast(im,.05)
    im.save(jpgFilePath)
    return