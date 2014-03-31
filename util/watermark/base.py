# -*- coding: utf-8 -*-
from functools import wraps
import math
import time


__author__ = 'myth'

LEFT_TOP = 'lt'
LEFT_BOTTOM = 'lb'
RIGHT_TOP = 'rt'
RIGHT_BOTTOM = 'rb'

WIDTH_GRID = 30.0
HEIGHT_GRID = 30.0


# 定义一个计时器，传入一个，并返回另一个附加了计时功能的方法
def timeit(func):

    # 定义一个内嵌的包装函数，给传入的函数加上计时功能的包装
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        _func = func(*args, **kwargs)
        end = time.time()

        print '%r: "%s" methods of running time->%r' % (func.func_code, func.func_name, end - start)
        return _func

    # 将包装后的函数返回
    return wrapper


class EngineBase(object):
    """
    图片处理引擎
    """

    def get_image_size(self, image):
        """
        返回图片尺寸
        :rtype: (int, int)
        :return: (width, height)
        """
        raise NotImplemented()

    def draw_grid_line(self, *args, **kwargs):
        """
        绘制网格线
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        raise NotImplemented()

    def draw_watermark_picture(self, image, mark, layout=RIGHT_BOTTOM):
        """
        绘制水印图片
        :param image:
        :type image:
        :param mark:
        :type mark:
        :param layout:
        :type layout:
        :return:
        :rtype:
        """
        raise NotImplemented()

    def mark_layout(self, image, mark, layout=RIGHT_BOTTOM):
        """
        设置水印位置
        :param image: 目标图片
        :type image:
        :param mark: 水印图片
        :type mark:
        :param layout: LEFT_TOP or LEFT_BOTTOM or RIGHT_TOP or RIGHT_BOTTOM
        :type layout:
        :return: (int, int)
        :rtype: (x, y)
        """
        im_width, im_height = self.get_image_size(image)
        mark_width, mark_height = self.get_image_size(mark)

        coordinates = {LEFT_TOP: (int(im_width/WIDTH_GRID),
                                  int(im_height/HEIGHT_GRID)),

                       LEFT_BOTTOM: (int(im_width/WIDTH_GRID),
                                     int(im_height - mark_height - im_height/HEIGHT_GRID)),

                       RIGHT_TOP: (int(im_width - mark_width - im_width/WIDTH_GRID),
                                   int(im_height/HEIGHT_GRID)),

                       RIGHT_BOTTOM: (int(im_width - mark_width - im_width/WIDTH_GRID),
                                      int(im_height - mark_height - im_height/HEIGHT_GRID))}

        return coordinates[layout]

    def dotted_line_coordinate(self, start, end, step=5):
        """
        虚线坐标
        :param start: 起点, (x, y)
        :type start:
        :param end: 终点, (x, y)
        :type end:
        :param step: 虚线间隔
        :type step: int
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

    def oblique_line_coordinate(self, xy, width, height, obliquity=45):
        """
        斜线坐标
        :param xy: 斜线上的一点坐标(x, y)
        :type xy:
        :param width: 坐标系的宽
        :type width:
        :param height: 坐标系的高
        :type height:
        :param obliquity: 斜度，角度
        :type obliquity:
        :return: 斜线的起点和终点坐标((x0, y0), (x1, y1))
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




