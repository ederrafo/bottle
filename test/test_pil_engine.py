# -*- coding: utf-8 -*-
from unittest import TestSuite, TestCase, TextTestRunner
import Image
from util.thumbnail.pil_engine import PilEngine

__author__ = 'myth'


class PilEngineTestCase(TestCase):

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
        pe = PilEngine()
        mark = pe.rotate(mark, 45, expand=False)

        mark = mark.convert('RGB')
        image_format = 'PNG'

        # mark, mark_format = pe.rgb_to_rgba(mark)
        mark.save('/home/myth/temp/tmp/c300.png', image_format, quality=95)

    def testDrawWatermarkPicture(self):
        MARK_IMAGE = '/home/myth/temp/tmp/kuaiyin.png'
        LINE_IMAGE = '/home/myth/temp/tmp/line.png'
        new_image_s_filename = '/home/myth/temp/tmp/test1.jpg'

        mark = Image.open(MARK_IMAGE)
        line = Image.open(LINE_IMAGE)
        im = Image.open(new_image_s_filename)

        pe = PilEngine()

        im, image_format = pe.rgb_to_rgba(im)
        line, line_format = pe.rgb_to_rgba(line)
        mark, mark_format = pe.rgb_to_rgba(mark)

        w, h = pe.get_image_size(line)
        line = line.resize((w*3, h*3), resample=Image.ANTIALIAS)

        im = pe.draw_grid_line(im, line)
        # im.paste(mark, (0, 0), mark)
        im = pe.draw_watermark_picture(im, mark)
        im.save('/home/myth/temp/tmp/c301.jpg', image_format, quality=95)


def suite():
    suite = TestSuite()
    suite.addTest(PilEngineTestCase("testRotate"))
    suite.addTest(PilEngineTestCase("testDrawWatermarkPicture"))
    return suite

if __name__ == '__main__':
    TextTestRunner().run(suite())