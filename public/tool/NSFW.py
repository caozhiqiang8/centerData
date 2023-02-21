from PIL import Image



t_img = Image.open(r'C:\Users\caozhiqiang\Downloads\001_pre (4).jpg').convert("YCbCr")  # 参数传入图片，引入转换成YUV模式图片
w, h = t_img.size  # 像素
sx = t_img.getdata()  # 像素数据
count = 0
for i, ycbcr in enumerate(sx):
    y, cb, cr = ycbcr
    if 86 <= cb <= 117 and 140 <= cr <= 168:
        count += 1
# print count,w * h
print(" 这%s一个色图." % ("是" if count > w * h * 0.3 else "不是"))

