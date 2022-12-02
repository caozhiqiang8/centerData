from PIL import Image
import os


# 获取文件大小:KB
def get_size(file):
    size = os.path.getsize(file)
    return size / 1024


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile


def compress_image(infile, outfile='', mb=100, step=10, quality=85):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    infile_size = get_size(infile)
    # 如果文件小于等于指定大小，直接返回原文件
    if infile_size <= mb:
        return infile

    outfile = get_outfile(infile, outfile)

    # 如果文件大于指定大小，循环处理图片质量
    while infile_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
    print(infile, '------->', '原文件:', get_size(infile), '------->压缩后文件：', get_size(outfile), '------->','{:.2%}'.format(1 - get_size(outfile) / get_size(infile)))
    return outfile, get_size(outfile)



if __name__ == '__main__':
    compress_image(r'C:\Users\caozhiqiang\Desktop\原图\111.jpg')
