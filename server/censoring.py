from PIL import Image, ImageDraw
from nudenet import NudeDetector
# from nudenet import NudeClassifier

class NsfwArea:
    def __init__(self, bounds, label, score, censorImage = True):
        if censorImage:
            self.y_min = bounds[1]
            self.x_min = bounds[0]
            self.y_max = bounds[3]
            self.x_max = bounds[2]
        else:
            self.y_min = bounds[0][1]
            self.x_min = bounds[0][0]
            self.y_max = bounds[2][1]
            self.x_max = bounds[2][0]
        self.label = label
        self.score = score

def getNsfwAreas(results, censorImage):
    nsfwAreas = []
    if censorImage:
        for nsfwArea in results:
            nsfwAreas.append(NsfwArea(nsfwArea["box"],
                                      nsfwArea["label"],
                                      nsfwArea["score"],
                                      True))
    else:
        for word in results:
            nsfwAreas.append(NsfwArea(word["vertices"],
                                      word["description"],
                                      0,
                                      False))

    return nsfwAreas

def censorImage(results, nsfwImagePath, sfwImagePath = "", censorImage = True):
    nsfwAreas = getNsfwAreas(results, censorImage)

    with Image.open(nsfwImagePath) as img:
        draw = ImageDraw.Draw(img)
        for nsfwArea in nsfwAreas:
            if (sfwImagePath == ""):
                draw.rectangle([nsfwArea.x_min, nsfwArea.y_min, nsfwArea.x_max, nsfwArea.y_max], '#0f0f0f80', '#0f0f0f80', 2)
            else:
                sfwImage = Image.open(sfwImagePath)

                size = nsfwArea.x_max - nsfwArea.x_min, nsfwArea.y_max - nsfwArea.y_min
                sfwImage = sfwImage.resize(size)

                offset = nsfwArea.x_min, nsfwArea.y_min

                img.paste(sfwImage, offset, mask=sfwImage)

    censoredImagePath = "sfw_" + nsfwImagePath

    img.save(censoredImagePath)
    return censoredImagePath