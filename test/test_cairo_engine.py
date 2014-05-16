# -*- coding: utf-8 -*-
from unittest import TestCase, TestSuite, TextTestRunner
import Image
from util.thumbnail.cairo_engine import CairoEngine

__author__ = 'myth'


class CairoEngineTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRotate(self):

        MARK_IMAGE = '/home/myth/temp/tmp/tt.jpg'
        #310x432
        mark = Image.open(MARK_IMAGE)
        if mark.mode != 'RGBA':
            mark = mark.convert('RGBA')
            image_format = 'JPEG'
        else:
            image_format = 'PNG'
        ce = CairoEngine()
        mark = ce.pil2cairo(mark)

        surface = ce.rotate(mark, 45, True)
        surface.write_to_png('/home/myth/temp/tmp/c100.png')

    def testRotate2(self):

        MARK_IMAGE = '/home/myth/temp/tmp/tt.jpg'
        #310x432
        mark = Image.open(MARK_IMAGE)
        if mark.mode != 'RGBA':
            mark = mark.convert('RGBA')
            image_format = 'JPEG'
        else:
            image_format = 'PNG'
        ce = CairoEngine()
        mark = ce.pil2cairo(mark)

        surface = ce.rotate(mark, 45, False)
        surface.write_to_png('/home/myth/temp/tmp/c101.png')

    def testDrawWatermarkPicture(self):
        MARK_IMAGE = '/home/myth/temp/tmp/kuaiyin.png'
        new_image_s_filename = '/home/myth/temp/tmp/test1.jpg'
        save_file_path = '/home/myth/temp/tmp/c102.jpg'

        mark = Image.open(MARK_IMAGE)

        im = Image.open(new_image_s_filename)
        engine = CairoEngine()

        image = engine.pil2cairo(im)
        mark = engine.pil2cairo(mark)
        # mark = cairo.ImageSurface.create_from_png(MARK_IMAGE)

        image = engine.draw_watermark_picture(image, mark)
        im = engine.cairo2pil(image)

        im.save(save_file_path, format='JPEG')


def suite():
    suite = TestSuite()
    suite.addTest(CairoEngineTestCase("testRotate"))
    suite.addTest(CairoEngineTestCase("testRotate2"))
    suite.addTest(CairoEngineTestCase("testDrawWatermarkPicture"))
    return suite

if __name__ == '__main__':
    TextTestRunner().run(suite())