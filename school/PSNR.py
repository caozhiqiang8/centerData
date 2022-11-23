from PIL import Image
import os
from skimage.metrics import mean_squared_error
from skimage.metrics import peak_signal_noise_ratio
import numpy as np

# 获取文件信息

path1 = r'C:\Users\caozhiqiang\Desktop\原图\1005029885_1663213969628767853_1.jpeg'
path2 = r'C:\Users\caozhiqiang\Desktop\原图\1005029885_1663214594177018226_2.jpeg'

img1 = Image.open(path1)
img2 = Image.open(path2)
print('图片格式：{}-----{}'.format(img1.format,img2.format))
print('图片尺寸：{}-----{}'.format(img1.size,img2.size))
print('图片路径：{}-----{}'.format(img1.filename,img2.filename))
print('图片格式：{}-----{}'.format(img1.mode,img2.mode))

im_memory = os.path.getsize(path1)
im_memory /= 1024
print('图片内存：{}-----{}'.format((os.path.getsize(path1))/1024 ,(os.path.getsize(path2))/1024 ))

img1 = np.array(Image.open(path1))
img2 = np.array(Image.open(path2))
MSE = mean_squared_error(img2, img1)
PSNR = peak_signal_noise_ratio(img1, img2)

'''
MSE：值越小越相似

PSNR接近 50dB ，代表压缩后的图像仅有些许非常小的误差。
PSNR大于 30dB ，人眼很难察觉压缩后和原始影像的差异。
PSNR介于 20dB 到 30dB 之间，人眼就可以察觉出图像的差异。
PSNR介于 10dB 到 20dB 之间，人眼还是可以用肉眼看出这个图像原始的结构，且直观上会判断两张图像不存在很大的差异。
PSNR低于 10dB，人类很难用肉眼去判断两个图像是否为相同，一个图像是否为另一个图像的压缩结果。
'''

print('MSE: ', MSE)
# print('SSIM: ', SSIM)
print('PSNR: ', PSNR)

