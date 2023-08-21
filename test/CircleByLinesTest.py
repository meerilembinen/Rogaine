import unittest
from PIL import Image

from src.findByLines.CircleByLines import find_circle


class MyTestCase(unittest.TestCase):
    def test_one_very_thin_red_circle(self):
        im = Image.open('resources/very_thin_red_circle.png')
        pix = im.load()
        circle = find_circle(im, pix)
        print(circle)
        print(im.size[0])
        print(im.size[1])
        self.assertGreater(circle.x, im.size[0] / 2 - im.size[0] * 0.05)
        self.assertLess(circle.x, im.size[0] / 2 + im.size[0] * 0.05)
        self.assertGreater(circle.y, im.size[1] / 2 - im.size[1] * 0.05)
        self.assertLess(circle.y, im.size[1] / 2 + im.size[1] * 0.05)

        im.show()
    def test_one_thin_red_circle(self):
        im = Image.open('resources/thin_red_circle.png')
        pix = im.load()
        circle = find_circle(im, pix)
        print(circle)
        print(im.size[0])
        print(im.size[1])
        self.assertGreater(circle.x, im.size[0] / 2 - im.size[0] * 0.05)
        self.assertLess(circle.x, im.size[0] / 2 + im.size[0] * 0.05)
        self.assertGreater(circle.y, im.size[1] / 2 - im.size[1] * 0.05)
        self.assertLess(circle.y, im.size[1] / 2 + im.size[1] * 0.05)

        im.show()


if __name__ == '__main__':
    unittest.main()
