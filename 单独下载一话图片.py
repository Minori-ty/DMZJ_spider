import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import shutil

# 1.下面输入漫画第几话的链接↓!!!网址最后不要带斜杠‘/’
url = 'http://manhua.dmzj.com/fufuyishanglianrenweiman/74214.shtml#@page=1'
# 2.下面输入你要储存漫画的目录↓第几话文件夹不用写了，会自动添加一个第几话的文件夹
path = 'C:\漫画\夫妇以上，恋人未满'
# 3.设置你phantomjs.exe的路径
driver_path = r'C:\Users\守夜人\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.8\phantomjs.exe'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4209.400',
    'Referer': url+'/'
}
print('正在加载浏览器，请等待5秒钟，不用管红色的警告')
driver = webdriver.PhantomJS(executable_path=driver_path)
content = driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

select = soup.find('select', id='page_select')
option = select.find_all('option')
title = soup.find('span', class_='redhotl').text
print('正在下载'+title)
path = path+'\\'+title
lastChapter = option[-1].text[1:-1]
print('一共'+lastChapter+'页')
a = 1
if (not os.path.exists(path)):
    os.makedirs(path)
for val in option:
    content = requests.get('http:' + val.get('value'), headers=headers).content
    with open(path + '\\' + str(a) + '.jpg', 'wb') as f:
        f.write(content)
    print('第' + str(a) + '张图片下载完毕！')
    a += 1
print('漫画已经全部下载完毕!')