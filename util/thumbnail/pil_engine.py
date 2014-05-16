# -*- coding: utf-8 -*-
from PIL import Image
from math import hypot, radians, pi
from util.thumbnail.base import EngineBase, RIGHT_BOTTOM, timeit


__author__ = 'myth'


class PilEngine(EngineBase):

    def rgb_to_rgba(self, image):
        """
        图片模式转换
        :param image:
        :type image:
        :return:
        :rtype:
        """
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
            image_format = 'JPEG'
        else:
            image_format = 'PNG'

        return image, image_format

    @timeit
    def draw_grid_line(self, image, line):

        """
        图片绘制网格
        """
        w, h = self.get_image_size(image)

        default_step = 50
        step = w / 10
        step = step if step > default_step else default_step

        positives = self.dotted_line_coordinate((0, 0), (w, h), step=step)
        reverses = self.dotted_line_coordinate((0, h), (w, 0), step=step)

        def _draw_lines(coordinates, image, line, size, obliquity=45):
            w, h = size

            mark = line.rotate(obliquity, expand=True)
            mw, mh = self.get_image_size(mark)
            step = hypot(mw, mh)
            for _pos in coordinates:
                pos = self.oblique_line_coordinate(_pos, w, h, obliquity=obliquity)
                start, end = pos
                pos = self.dotted_line_coordinate(start, end, step=step)

                for i, p in enumerate(pos):
                    if i % 2 == 1:
                        start_x, start_y = start
                        end_x, end_y = p
                        image.paste(mark, (int(start_x), int(start_y)), mark)

                    if i % 2 == 0:
                        start = p

        _draw_lines(positives[1:-1], image, line, (w, h), obliquity=30)
        _draw_lines(reverses[1:-1], image, line, (w, h), obliquity=-30)

        return image

    @timeit
    def draw_watermark_picture(self, image, mark, layout=RIGHT_BOTTOM):
        """
        绘制水印
        :param image:
        :type image:
        :param mark:
        :type mark:
        :param layout:
        :type layout:
        :return:
        :rtype:
        """

        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        mark = self._set_mark_resize(image, mark)
        #分割rgba通道，分割后根据mode返回值
        r_im, g_im, b_im, a_im = mark.split()
        x, y = self.mark_layout(image, mark, layout)
        #获取像素值，根据mode返回值
        r, g, b, a = image.getpixel((x, y))
        if r > 100 or g > 100 or b > 100:
            mark = a_im

        image.paste(mark, (x, y), mark)

        # return Image.composite(layer, image, layer)
        return image

    def get_image_size(self, image):
        """
        获取图片尺寸
        :param image:
        :type image:
        :return:
        :rtype:
        """

        return image.size

    def _set_mark_resize(self, image, mark):
        """
        设置水印图片的尺寸
        :param image:
        :type image:
        :param mark:
        :type mark: PIL.Image
        :return:
        :rtype:
        """
        im_width, im_height = self.get_image_size(image)
        mark_width, mark_height = self.get_image_size(mark)
        min_scale = 0.18
        max_scale = 0.3
        x_scale = float(mark_width) / float(im_width)
        y_scale = float(mark_height) / float(im_height)
        is_scale = False
        scale = max(x_scale, y_scale)
        if scale < min_scale:
            mark_width = int(mark_width/min_scale)
            mark_height = int(mark_height/min_scale)
            is_scale = True

        if scale > max_scale:
            mark_width = int(mark_width/max_scale)
            mark_height = int(mark_height/max_scale)
            is_scale = True

        if is_scale:
            #设置水印图片的尺寸
            return mark.resize((mark_width, mark_height), resample=Image.ANTIALIAS)
        else:
            return mark

    @timeit
    def rotate(self, image, angle=0, expand=False):
        """
        图片水平旋转
        :param image:
        :type image: PIL.Image
        :param angle: 旋转角度
        :type angle:
        :param expand:可选的扩展标志。如果为true，
                      扩大了输出图像，使其大到足以容纳整个旋转后的图像。
                      如果虚假或省略，使输出的图像的大小相同的输入图像。
        :type expand: bool
        :return:
        :rtype:
        """
        if angle % 90 == 0:
            cycles = int(angle) / 360
            _angle = angle - cycles * 360
            # if _angle == 0:
            #     return image
            if _angle == 90:
                return image.transpose(Image.ROTATE_90)
            if _angle == 180:
                return image.transpose(Image.ROTATE_180)
            if _angle == 270:
                return image.transpose(Image.ROTATE_270)
            return image
        else:
            return image.rotate(angle, expand=expand)


if __name__ == '__main__':
    # MARK_IMAGE = './kuaiyin.png'
    # LINE_IMAGE = './line.png'
    # new_image_s_filename = '/home/myth/temp/tmp/test1.jpg'
    #
    # mark = Image.open(MARK_IMAGE)
    # line = Image.open(LINE_IMAGE)
    # im = Image.open(new_image_s_filename)
    #
    # pe = PilEngine()
    #
    # im, image_format = pe.rgb_to_rgba(im)
    # line, line_format = pe.rgb_to_rgba(line)
    # mark, mark_format = pe.rgb_to_rgba(mark)
    #
    # w, h = pe.get_image_size(line)
    # line = line.resize((w*3, h*3), resample=Image.ANTIALIAS)
    #
    # im = pe.draw_grid_line(im, line)
    # # im.paste(mark, (0, 0), mark)
    # im = pe.draw_watermark_picture(im, mark)
    # im.save('/home/myth/temp/tmp/b4.jpg', image_format, quality=95)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    MARK_IMAGE = '/home/myth/temp/tmp/tt.jpg'
    #310x432
    mark = Image.open(MARK_IMAGE)
    if mark.mode != 'RGBA':
        mark = mark.convert('RGBA')
        image_format = 'JPEG'
    else:
        image_format = 'PNG'
    pe = PilEngine()
    mark = pe.rotate(mark, 90, expand=False)

    mark = mark.convert('RGB')
    image_format = 'PNG'
    # mark, mark_format = pe.rgb_to_rgba(mark)
    mark.save('/home/myth/temp/tmp/c1.jpg', image_format, quality=95)