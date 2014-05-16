# -*- coding: utf-8 -*-
import array
from math import radians, cos, sin, ceil, floor
import cairocffi
import sys
from PIL import Image

cairocffi.install_as_pycairo()
import cairo
from util.thumbnail.base import EngineBase, timeit, RIGHT_BOTTOM


__author__ = 'myth'


class CairoEngine(EngineBase):

    def get_image_size(self, image):
        """
        获取图片尺寸
        :param image:
        :type image: cairo.ImageSurface
        :return:
        :rtype:
        """
        w = image.get_width()
        h = image.get_height()
        return w, h

    @timeit
    def pil2cairo(self, image):
        """
        Transform a PIL Image into a Cairo ImageSurface.
        image图片尺寸6000x6000
        :param image:
        :type image: PIL.Image
        """

        #检查机器是否支持小端，（大端(Big Endian)与小端(Little Endian)）
        assert sys.byteorder == 'little', 'We don\'t support big endian'
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        s = image.tostring('raw', 'BGRA')#ARBG  (Big Endian)
        a = array.array('B', s)
        w, h = image.size
        dest = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(dest)
        non_premult_src_wo_alpha = cairo.ImageSurface.create_for_data(
            a, cairo.FORMAT_RGB24, w, h)
        non_premult_src_alpha = cairo.ImageSurface.create_for_data(
            a, cairo.FORMAT_ARGB32, w, h)
        ctx.set_source_surface(non_premult_src_wo_alpha)
        ctx.mask_surface(non_premult_src_alpha)

        return dest

    @timeit
    def cairo2pil(self, image):
        """
        Transform a Cairo ImageSurface into a PIL Image .
        :param image:
        :type image: cairo.ImageSurface
        :return:
        :rtype:
        """

        #检查机器是否支持小端，（大端(Big Endian)与小端(Little Endian)）
        assert sys.byteorder == 'little', 'We don\'t support big endian'
        data = image.get_data()
        im = Image.fromstring('RGBA', self.get_image_size(image), data)
        #ARBG  (Big Endian)
        #BGRA  (Little Endian)
        #分割rgba通道，分割后根据mode返回值
        r_im, g_im, b_im, a_im = im.split()
        if sys.byteorder == 'little':
            r_im, g_im, b_im, a_im = b_im, g_im, r_im, a_im

        im = Image.merge(im.mode, (r_im, g_im, b_im, a_im))
        return im

    @timeit
    def draw_watermark_picture(self, image, mark, layout=RIGHT_BOTTOM):
        """
        绘制水印
        :param image: 原始图片
        :type image: cairo.ImageSurface
        :param mark: 水印图片
        :type mark: cairo.ImageSurface
        """

        context = cairo.Context(image)
        mark = self._set_mark_resize(image, mark)
        x, y = self.mark_layout(image, mark, layout=layout)
        context.mask_surface(mark, surface_x=x, surface_y=y)
        context.fill()
        context.stroke()
        return image

    @timeit
    def _set_mark_resize(self, image, mark):
        """
        设置水印图片的大小
        :param image: 原始图片
        :type image: cairo.ImageSurface
        :param mark: 水印图片
        :type mark: cairo.ImageSurface
        """
        im_width, im_height = self.get_image_size(image)
        mark_width, mark_height = self.get_image_size(mark)
        min_scale = 0.18
        max_scale = 0.3
        x_scale = float(mark_width) / float(im_width)
        y_scale = float(mark_height) / float(im_height)
        scale = 1/x_scale
        is_scale = False
        if x_scale < min_scale and y_scale < min_scale:

            scale = 1/min_scale
            is_scale = True

        if x_scale > max_scale or y_scale > max_scale:
            scale = 1/max_scale
            is_scale = True

        if is_scale:
            #设置水印图片的尺寸
            mark = self.scale(mark, scale)

        return mark

    @timeit
    def scale(self, image, sx, sy=None):
        """
        图片缩放
        :param image:
        :type image: cairo.ImageSurface
        :param sx:
        :type sx: float
        :param sy:
        :type sy: float
        :return:
        :rtype:
        """

        width = image.get_width()
        height = image.get_height()
        if sy is None:
            sy = sx
        w = int(width * sx)
        h = int(height * sy)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)
        ctx.scale(sx, sy)
        # ctx.translate(0, 0)
        ctx.set_source_surface(image)
        ctx.paint()
        # ctx.restore()
        return surface

    @timeit
    def rotate(self, image, angle=0, expand=False):
        """
        图片水平旋转
        :param image:
        :type image: cairo.ImageSurface
        :param angle: 旋转角度
        :type angle:
        :param expand:可选的扩展标志。如果为true，
                      扩大了输出图像，使其大到足以容纳整个旋转后的图像。
                      如果虚假或省略，使输出的图像的大小相同的输入图像。
        :type expand: bool
        :return:
        :rtype:
        """
        # calculate output size
        w, h = self.get_image_size(image)
        angle = -radians(angle)

        matrix = [
            cos(angle), -sin(angle), 0.0,
            sin(angle), cos(angle), 0.0
        ]

        def transform(x, y, (a, b, c, d, e, f)=matrix):
            return a*x + b*y + c, d*x + e*y + f

        if expand:

            xx = []
            yy = []
            for x, y in ((0, 0), (w, 0), (w, h), (0, h)):
                x, y = transform(x, y)
                xx.append(x)
                yy.append(y)
            w = int(ceil(max(xx)) - floor(min(xx)))
            h = int(ceil(max(yy)) - floor(min(yy)))

            # adjust center
            x, y = transform(w / 2.0, h / 2.0)
            move_x = 0-min(xx)
            move_y = 0-min(yy)
        else:
            x, y = transform(w / 2.0, h / 2.0)
            move_x = w/2.0 - x
            move_y = h/2.0 - y
            # move_x, move_y = (0, 0)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)

        ctx.translate(move_x, move_y)
        ctx.rotate(angle)

        ctx.set_source_surface(image)
        ctx.paint()

        return surface

if __name__ == '__main__':
    MARK_IMAGE = '/home/myth/temp/tmp/kuaiyin.png'
    # MARK_IMAGE = '/home/myth/temp/tmp/3.png'
    # MARK_IMAGE = '/home/myth/temp/tmp/water.jpg'
    new_image_s_filename = '/home/myth/temp/tmp/test1.jpg'
    save_file_path = '/home/myth/temp/tmp/c1.jpg'
    #
    # mark = Image.open(MARK_IMAGE)
    #
    # im = Image.open(new_image_s_filename)
    # engine = CairoEngine()
    #
    # image = engine.pil2cairo(im)
    #
    # mark = cairo.ImageSurface.create_from_png(MARK_IMAGE)
    #
    # image = engine.draw_watermark_picture(image, mark)
    # im = engine.cairo2pil(image)
    #
    # # im = Image.open(so)
    # im.save(save_file_path, format='JPEG')


    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

    surface = ce.rotate(mark, 0, True)
    surface.write_to_png('/home/myth/temp/tmp/c1.png')

