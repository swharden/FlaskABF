import os
import glob

from PIL import Image
from PIL import ImageEnhance

for tifFile in glob.glob(R"C:\Users\swharden\Documents\temp\test\*.tif"):
    print("converting", os.path.basename(tifFile))
    jpgFile = tifFile+".jpg"
    im = Image.open(tifFile)
    im = ImageEnhance.Contrast(im).enhance(7)
    im.save(jpgFile)