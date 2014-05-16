# -*- coding: utf-8 -*-
from unittest import TestCase, TestSuite, TextTestRunner
import Image
from util.thumbnail.engine import rotate

__author__ = 'myth'


class EngineTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPilRotate(self):
        MARK_IMAGE = '/home/myth/temp/tmp/tt.png'
        #310x432
        mark = Image.open(MARK_IMAGE)
        if mark.mode != 'RGBA':
            mark = mark.convert('RGBA')
            image_format = 'JPEG'
        else:
            image_format = 'PNG'

        mark = rotate(mark, 45, True, False)
        mark = mark.convert('RGB')
        image_format = 'PNG'
        mark.save('/home/myth/temp/tmp/c201.png', image_format, quality=95)

    def testCairoRotate(self):
        MARK_IMAGE = '/home/myth/temp/tmp/tt.png'
        #310x432
        mark = Image.open(MARK_IMAGE)
        if mark.mode != 'RGBA':
            mark = mark.convert('RGBA')
            image_format = 'JPEG'
        else:
            image_format = 'PNG'

        mark = rotate(mark, 45, True, True)

        mark.write_to_png('/home/myth/temp/tmp/c202.png')


def suite():
    suite = TestSuite()
    suite.addTest(EngineTestCase("testPilRotate"))
    suite.addTest(EngineTestCase("testCairoRotate"))
    return suite

if __name__ == '__main__':
    TextTestRunner().run(suite())