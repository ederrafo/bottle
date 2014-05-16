# -*- coding: utf-8 -*-
import math
from pgmagick import CompositeOperator as co, Geometry
from pgmagick.api import Image as pgai, Draw


__author__ = 'myth'

LEFT_TOP = 'lt'
LEFT_BOTTOM = 'lb'
RIGHT_TOP = 'rt'
RIGHT_BOTTOM = 'rb'

WIDTH_GRID = 30.0
HEIGHT_GRID = 30.0


def dotted_line(start, end, step=5):
    """
    虚线坐标
    :param start:
    :type start:
    :param end:
    :type end:
    :param step:
    :type step:
    :return:
    :rtype:
    """
    xl, yl = start
    xr, yr = end
    w = abs(xl - xr)
    # h = abs(yl - yr)
    #将坐标转换到第三象限
    yl, yr = -yl, -yr
    #斜率
    k = float((yr - yl)) / (xr - xl)
    #偏移
    b = yl - k * xl
    pos = [start]
    pos_y = lambda x: k * x + b
    # pos_x = lambda y: (y - b)/k

    if step > 0:
        step = math.ceil(step)
        _steps = w / step
        _steps = _steps-1 if _steps == math.floor(_steps) else math.floor(_steps)
        steps = int(_steps)
        for s in xrange(steps):
            _s = s + 1
            x = xl + _s * step
            y = pos_y(x)
            _pos = (x, -y)
            pos.append(_pos)

    pos.append(end)
    return pos


def oblique_line(xy, width, height, obliquity=45):
    """
    斜线坐标
    :param xy:
    :type xy:
    :param width:
    :type width:
    :param height:
    :type height:
    :param obliquity:
    :type obliquity:
    :return:
    :rtype:
    """

    x, y = xy
    #将坐标转换到第三象限
    y = -y
    w, h = width, -height
    #角度转弧度
    # p = obliquity/180. * math.pi
    p = math.radians(obliquity)
    #斜率
    k = math.tan(p)
    #偏移
    b = y - k*x

    pos_y = lambda x: k * x + b
    pos_x = lambda y: (y - b)/k
    if k > 0:
        #左边x坐标
        xl = 0
        #左边y坐标
        yl = pos_y(xl)
        if yl < h:
            yl = h
            xl = pos_x(yl)
        #右边y坐标
        yr = 0
        #右边x坐标
        xr = pos_x(yr)
        if xr > w:
            xr = w
            yr = pos_y(xr)
    else:
        #左边y坐标
        yl = 0
        #左边x坐标
        xl = pos_x(yl)
        if xl < 0:
            xl = 0
            yl = pos_y(xl)

        #右边x坐标
        xr = w
        #右边y坐标
        yr = pos_y(xr)
        if yr < h:
            yr = h
            xr = pos_x(yr)

    pos = ((round(xl), round(-yl)), (round(xr), round(-yr)))
    return pos


def draw_grid(im):

    """
    图片绘制网格
    """
    w, h = im.width, im.height
    draw = Draw()
    default_step = 50
    step = w / 10
    step = step if step > default_step else default_step

    positives = dotted_line((0, 0), (w, h), step=step)
    reverses = dotted_line((0, h), (w, 0), step=step)
    #线条颜色
    draw.stroke_color((220, 220, 220))
    #线条宽度
    draw.stroke_width(2)
    #透明度
    draw.stroke_opacity(0.2)

    def _draw_lines(coordinates, draw, size, obliquity=45):
        w, h = size
        for _pos in coordinates:
            pos = oblique_line(_pos, w, h, obliquity=obliquity)
            start, end = pos
            pos = dotted_line(start, end, step=30)

            for i, p in enumerate(pos):
                if i % 3 == 1:
                    start_x, start_y = start
                    end_x, end_y = p
                    draw.line(start_x, start_y, end_x, end_y)
                if i % 3 == 0:
                    start = p

    _draw_lines(positives[1:-1], draw, (w, h), obliquity=30)
    _draw_lines(reverses[1:-1], draw, (w, h), obliquity=-30)
    im.draw(draw)


def mark_layout(im, mark, layout=RIGHT_BOTTOM):
    """
    设置水印位置
    :param im:
    :type im: pgmagick.api.Image
    :param mark:
    :type mark: pgmagick.api.Image
    :param layout:
    :type layout:
    :return:
    :rtype:
    """
    im_width, im_height = im.width, im.height
    mark_width, mark_height = mark.width, mark.height

    coordinates = {LEFT_TOP: (int(im_width/WIDTH_GRID), int(im_height/HEIGHT_GRID)),
                   LEFT_BOTTOM: (int(im_width/WIDTH_GRID), int(im_height - mark_height - im_height/HEIGHT_GRID)),
                   RIGHT_TOP: (int(im_width - mark_width - im_width/WIDTH_GRID), int(im_height/HEIGHT_GRID)),
                   RIGHT_BOTTOM: (int(im_width - mark_width - im_width/WIDTH_GRID),
                                  int(im_height - mark_height - im_height/HEIGHT_GRID))}

    return coordinates[layout]


def set_mark_picture(im, mark):
    """
    设置水印图片的大小
    :param im: 原始图片
    :type im: pgmagick.api.Image
    :param mark: 水印图片
    :type mark: pgmagick.api.Image
    """
    im_width, im_height = im.width, im.height
    mark_width, mark_height = mark.width, mark.height
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


def draw_watermark(im, mark, layout=RIGHT_BOTTOM):
    """
    绘制水印
    :param im: 原始图片
    :type im: pgmagick.api.Image
    :param mark: 水印图片
    :type mark: pgmagick.api.Image
    """
    set_mark_picture(im, mark)
    x, y = mark_layout(im, mark, layout=layout)
    geo = Geometry(0, 0, x, y)
    color = im.img.pixelColor(x, y)

    # print color.to_std_string()
    b = color.blueQuantum()
    r = color.redQuantum()
    g = color.greenQuantum()
    if r > 100 or g > 100 or b > 100:
        op = co.MinusCompositeOp
    else:
        op = co.OverCompositeOp
    im.composite(mark.img, geo, op)


if __name__ == '__main__':
    MARK_IMAGE = './kuaiyin.png'
    new_image_s_filename = '/home/myth/temp/tmp/test.jpg'

    mark = pgai(MARK_IMAGE)
    im = pgai(new_image_s_filename)
    draw_grid(im)
    draw_watermark(im, mark)
    im.write('/home/myth/temp/tmp/b2.jpg')
