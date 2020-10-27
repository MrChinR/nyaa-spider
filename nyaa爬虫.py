# -*- coding = utf-8 -*-


from bs4 import BeautifulSoup
import xlwt
import re
import urllib.request
from io import BytesIO  #网页源代码解压缩
import gzip
import sqlite3
import sys,threading,time
import datetime
from queue import Queue

findTitle = re.compile(r'title="(.*?)"')
findUpdate = re.compile(r'data-timestamp=".*?">(.*?) .*?:')
findMagnet = re.compile(r'<a href="(.*?)"><i class="fa fa')  #1 2
findUrl = re.compile(r'<a href="(.*?)" title')  #2
findSizeUpDownCom = re.compile(r'center">(.*?)</td>',re.S)


def main():
    aa = input('请输入您要选择的爬取的网页（1.nyaa2.sukebei3.两者）：')
    a = input('请输入您要爬取的页数：')
    print('若中途报错，为服务器防爬取机制，请减少线程数量。')
    thread_num = input('请输入最大线程数量：')
    if aa == '3':
        baseurl = "https://nyaa.si/"
        baseurl1 = "https://sukebei.nyaa.si/"
        getData(baseurl,a,thread_num)
        getData(baseurl1,a,thread_num)
        savepath = ".\\nyaa.xls"
        saveData(datalist, savepath,'nyaa')
        saveData(datalist1, savepath,'sukebei_nyaa')
    elif aa == '1':
        baseurl = "https://nyaa.si/"
        getData(baseurl,a,thread_num)
        savepath = ".\\nyaa.xls"
        saveData(datalist, savepath, 'nyaa')
    else:
        baseurl1 = "https://sukebei.nyaa.si/"
        getData(baseurl1,a,thread_num)
        savepath = ".\\nyaa.xls"
        saveData(datalist1, savepath,'sukebei_nyaa')


def askURL(url):
    head = {  # 模拟浏览器头部信息
        'cookie' : '__ddg1=BsVNA0Ra1HssocYeoCUG; __ddg2=XXNH6HMqjyYjEwtg',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51",
        'sec-fetch-user': '?1',
        'accept-encoding': 'gzip',
        'referer' : '%s'%url

    }
    # 用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）


    request = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(request)
    a = response.read()
    buff = BytesIO(a)  # 解码源代码
    f = gzip.GzipFile(fileobj=buff)
    html = f.read().decode("UTF-8")
    return html



def pa(url):
    end = datetime.date.today()
    try:
        html = askURL(url)
    except Exception as e:
        print(e)
        return
    soup = BeautifulSoup(html, "lxml")
    for ii in ["success", "danger", "default"]:
        for item in soup.find_all("tr", class_=ii):
            data = []
            item = str(item)
            size = re.findall(findSizeUpDownCom, item)[1]
            if g == 'Y' or 'y':
                if size[len(size) - 3:] != 'GiB':
                    continue
            title1 = re.findall(findTitle, item)[0]
            try:
                title2 = re.findall(findTitle, item)[1]
            except:
                tiltle2 = 'None'
            update = re.findall(findUpdate, item)[0]
            year = int(update[:4])
            month = int(update[5:7])
            day = int(update[8:])
            start = datetime.date(year, month, day)
            DE = (end - start).days
            URL = url + re.findall(findUrl, item)[1][1:]
            torrent = url + re.findall(findMagnet, item)[0][1:]
            magnet = re.findall(findMagnet, item)[1]
            upload = re.findall(findSizeUpDownCom, item)[2]
            download = re.findall(findSizeUpDownCom, item)[3]
            complete = re.findall(findSizeUpDownCom, item)[4]
            data.append(title1)
            data.append(title2)
            data.append(upload)
            data.append(download)
            data.append(complete)
            data.append(torrent)
            data.append(magnet)
            data.append(size)
            data.append(update)
            data.append(URL)
            U = int(upload)
            D = int(download)
            F = int(complete)
            if int(upload) == 0:
                rate = '上传为0'
            elif DE == 0:
                DU = D / U
                rate = '当天新种，下载/上传=%d' % DU
            else:
                DU = D / U
                rate = (F - U - D) / DE * DU
            data.append(rate)
            if url[:10] == 'https://ny':
                datalist.append(data)
            else:
                datalist1.append(data)

def getData(url,page,thread_num):
    page = int(page) + 1
    queue_url = Queue()
    thread_num = int(thread_num)
    for item in range(1, page):
        url1 = url + "?p=%d"%item
        queue_url.put(url1)
        print(url1)
    while 1:
            if queue_url.empty() == True:
                break
            if threading.active_count() > thread_num:
                time.sleep(1)
                continue
            url = queue_url.get()
            t = threading.Thread(target=pa, name='th-' + str(item),kwargs={'url': url})
            t.start()
    t.join()


def saveData(datalist,savepath,sheetname):
    print("save....")
    data = []
    sheet = book.add_sheet(sheetname,cell_overwrite_ok=True)    #创建工作表
    col = ("所属","标题","上传量","下载量","完成数","种子","磁力链接","大小","上传日期","链接",'黑？')
    for i in range(0,11):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,len(datalist)):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,11):
            sheet.write(i+1,j,data[j])      #数据
    book.save(savepath)       #保存



if __name__ == '__main__':
    book = xlwt.Workbook(encoding="utf-8", style_compression=0) #创建workbook对象
    datalist = []
    datalist1 = []
    g = input('是否要略过1G以下的小文件（Y/N）:')
    main()
    print("程序执行完毕！")