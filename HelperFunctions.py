import pygame as pg

def loadImage(filename):
    image = pg.image.load(filename)
    if (image is None):
        raise FileNotFoundError("Image file not found: " + filename)
        
    return image

def loadSound(filename):
    sound = pg.mixer.Sound(filename)
    if (sound is None):
        raise FileNotFoundError("Sound file not found: " + filename)
        
    return sound

def loadFont(filename, size):
    font = pg.font.Font(filename, size)
    if (font is None):
        raise FileNotFoundError("Font file not found: " + filename)
        
    return font