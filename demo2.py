#coding=utf-8
import pytesseract
from PIL import Image

#打开图片
im = Image.open('10.png')
#转为灰度图
im = im.convert('L')
#降噪 二值化
def init(threshold = 127):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
im = im.point(init(),'1')
im.show()
# 识别图片
tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/tessdata"'
# It's important to include double quotes around the dir path.
text = pytesseract.image_to_string(im, config=tessdata_dir_config)
# captcha = pytesseract.image_to_string(im)
print(text)