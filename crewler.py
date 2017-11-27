#coding=utf-8
# 模拟浏览器登陆
import requests
from bs4 import BeautifulSoup as BS
import time
from subprocess import Popen # 打开图片
import http.cookiejar
import re
from PIL import Image
import pytesseract

# header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
header = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
url = "https://www.zhihu.com"
login_url = "http://www.zhihu.com/login/"

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='ZhiHuCookies')

try:
    #加载cookie文件
    session.cookies.load(ignore_discard=True)
except:
    print("cookies未保存或cookie已过期")
    #第一步 获取_xsrf
    _xsrf = BS(session.get(url,headers=header).text,"lxml").find("input",{"name":"_xsrf"})["value"]

    #第二步 根据账号判断登录方式
    account = input("please input your account:")
    password = input("please input your password:")

    #第三步 获取验证码图片
    gifUrl = "http://www.zhihu.com/captcha.gif?r="+str(int(time.time()*1000))+"&type=login"
    gif = session.get(gifUrl,headers=header)

    #保存图片
    with open('code.gif','wb') as f:
        f.write(gif.content)
    #打开图片
    #Popen('code.gif',shell=True)
    #输入验证码
    #captcha = input('captcha: ')

    #打开图片
    im = Image.open('code.gif')
    # 识别图片
    captcha = pytesseract.image_to_string(im)

    data = {
        "captcha":captcha,
        "password":password,
        "_xsrf":_xsrf
    }

    # 第四步 判断account类型是手机号还是邮箱
    if re.match("^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$",account):
        #邮箱
        data['email'] = account
        login_url = login_url + "email"
    else:
        #手机号
        data["phone_num"] = account
        login_url = login_url + "phone_num"
    print(data)

    #第五步 登录
    response = session.post(login_url,data=data,headers=header)
    print(response.content.decode("utf-8"))

    #第六步 保存cookies
    session.cookies.save()

resp = session.get(url,headers=header,allow_redirects=False)
print(resp.content.decode("utf-8"))