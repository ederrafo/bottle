# -*- coding: utf-8 -*-
import Image
from util.thumbnail.cairo_engine import CairoEngine
from util.thumbnail.pil_engine import PilEngine

__author__ = 'myth'


def rotate(image, angle=0, expand=False, is_png=True):
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
    :param is_png: 是否是cairo对象
    :type is_png: bool
    :return:
    :rtype:
    """
    ce = CairoEngine()
    if angle % 90 == 0:
        pe = PilEngine()
        image = pe.rotate(image, angle, expand=expand)
        if is_png:
            image = ce.pil2cairo(image)
    else:
        image = ce.pil2cairo(image)
        image = ce.rotate(image, angle, expand=expand)
        if not is_png:
            image = ce.cairo2pil(image)

    return image


if __name__ == '__main__':
    MARK_IMAGE = '/home/myth/temp/tmp/c1.png'
    #310x432
    mark = Image.open(MARK_IMAGE)
    if mark.mode != 'RGBA':
        mark = mark.convert('RGBA')
        image_format = 'JPEG'
    else:
        image_format = 'PNG'

    mark = rotate(mark, 45, True, False)
    print mark.mode
    mark = mark.convert('RGB')
    image_format = 'PNG'
    mark.save('/home/myth/temp/tmp/c2.png', image_format, quality=95)