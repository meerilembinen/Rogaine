from PIL import Image

from src.findByLines.CircleByLines import find_circle

if __name__ == "__main__":
    im = Image.open('resources/very_thin_red_circle.png')
    pix = im.load()

    circle = find_circle(im, pix)
    print(circle)
    im.show()
