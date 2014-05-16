# -*- coding: utf-8 -*-
from pgmagick.api import Draw, Image as pgai
from pgmagick import Geometry, CompositeOperator as co, FilterTypes, OrientationType
from util.thumbnail.base import EngineBase, RIGHT_BOTTOM, timeit

__author__ = 'myth'


class PgmagickEngine(EngineBase):

    def get_image_size(self, image):
        """
        获取图片尺寸
        :param image:
        :type image: pgmagick.api.Image
        :return:
        :rtype:
        """

        return image.width, image.height

    @timeit
    def draw_grid_line(self, image):

        """
        图片绘制网格
        """
        w, h = self.get_image_size(image)
        draw = Draw()
        default_step = 50
        step = w / 10
        step = step if step > default_step else default_step

        positives = self.dotted_line_coordinate((0, 0), (w, h), step=step)
        reverses = self.dotted_line_coordinate((0, h), (w, 0), step=step)
        #线条颜色
        draw.stroke_color((220, 220, 220))
        #线条宽度
        draw.stroke_width(2)
        #透明度
        draw.stroke_opacity(0.2)

        def _draw_lines(coordinates, draw, size, obliquity=45):
            w, h = size
            for _pos in coordinates:
                pos = self.oblique_line_coordinate(_pos, w, h, obliquity=obliquity)
                start, end = pos
                pos = self.dotted_line_coordinate(start, end, step=30)

                for i, p in enumerate(pos):
                    if i % 3 == 1:
                        start_x, start_y = start
                        end_x, end_y = p
                        draw.line(start_x, start_y, end_x, end_y)
                    if i % 3 == 0:
                        start = p

        _draw_lines(positives[1:-1], draw, (w, h), obliquity=30)
        _draw_lines(reverses[1:-1], draw, (w, h), obliquity=-30)
        image.draw(draw)
        return image

    def _set_mark_resize(self, image, mark):
        """
        设置水印图片的大小
        :param image: 原始图片
        :type image: pgmagick.api.Image
        :param mark: 水印图片
        :type mark: pgmagick.api.Image
        """
        im_width, im_height = self.get_image_size(image)
        mark_width, mark_height = self.get_image_size(mark)
        min_scale = 0.18
        max_scale = 0.3
        x_scale = float(mark_width) / float(im_width)
        y_scale = float(mark_height) / float(im_height)
        is_scale = False
        if x_scale < min_scale and y_scale < min_scale:
            mark_width = int(min_scale * im_width)
            mark_height = int(min_scale * im_height)
            is_scale = True

        if x_scale > max_scale or y_scale > max_scale:
            mark_width = int(max_scale * im_width)
            mark_height = int(max_scale * im_height)
            is_scale = True

        if is_scale:
            #设置水印图片的尺寸
            mark.img.scale(Geometry(mark_width, mark_height))
            mark.img.strokeAntiAlias(False)
        return mark

    @timeit
    def draw_watermark_picture(self, image, mark, layout=RIGHT_BOTTOM):
        """
        绘制水印
        :param image: 原始图片
        :type image: pgmagick.api.Image
        :param mark: 水印图片
        :type mark: pgmagick.api.Image
        """
        mark = self._set_mark_resize(image, mark)
        x, y = self.mark_layout(image, mark, layout=layout)
        geo = Geometry(0, 0, x, y)
        color = image.img.pixelColor(x, y)

        # print color.to_std_string()
        b = color.blueQuantum()
        r = color.redQuantum()
        g = color.greenQuantum()
        if r > 100 or g > 100 or b > 100:
            op = co.MinusCompositeOp
        else:
            op = co.OverCompositeOp
        image.composite(mark.img, geo, op)
        return image


if __name__ == '__main__':
    MARK_IMAGE = './kuaiyin.png'
    LINE_IMAGE = './line.png'
    new_image_s_filename = '/home/myth/temp/tmp/test1.jpg'

    mark = pgai(MARK_IMAGE)
    im = pgai(new_image_s_filename)

    engine = PgmagickEngine()
    im = engine.draw_grid_line(im)
    im = engine.draw_watermark_picture(im, mark)

    im.write('/home/myth/temp/tmp/b2.jpg')
