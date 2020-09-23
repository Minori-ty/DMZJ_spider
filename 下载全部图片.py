import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import shutil

# 1.下面输入漫画的目录链接↓!!!网址最后不要带‘/’
url = 'http://manhua.dmzj.com/jiandiejiaoshi'
# 2.下面输入你要储存漫画的根目录↓漫画名文件夹不用写了，会自动添加一个文件夹
path = 'C:\漫画'
# 3.设置你phantomjs.exe的路径
driver_path = r'C:\Users\守夜人\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.8\phantomjs.exe'
http = 'http://manhua.dmzj.com'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4209.400',
    'Referer': url+'/'
}
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
print('正在加载浏览器，请等待5秒钟，不用管红色的警告')
name = soup.find('span',class_='anim_title_text').a.h1.text
path = 'C:\漫画\\'+name
ul = soup.find('div', class_='cartoon_online_border').find('ul')
lis = ul.find_all('li')
list = []
title=[]
for li in lis:
    title.append(li.text[0:-1])
    list.append(li.a.get('href'))
n=1
count = 0
for href in list:
    spath = path + '\\' + title[count]
    if (not os.path.exists(spath)):
        os.makedirs(spath)
    chapter_url = http+href
    driver = webdriver.PhantomJS(executable_path=driver_path)
    content = driver.get(chapter_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    select = soup.find('select', id='page_select')
    option = select.find_all('option')
    lastChapter = option[-1].text[1:-1]
    # driver.quit()
    print('正在加载' + title[count] + '的页面...')
    print(title[count]+'一共'+lastChapter+'页')
    a = 1
    for val in option:
        content = requests.get('http:' + val.get('value'), headers=headers).content
        with open(spath + '\\' + str(a) + '.jpg', 'wb') as f:
            f.write(content)
        print(title[count]+'第' + str(a) + '张图片下载完毕！')
        a += 1
    n += 1
    count += 1
print('漫画已经全部下载完毕!')
print('可以访问【'+path+'】查看漫画')

