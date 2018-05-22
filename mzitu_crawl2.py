#! /User/bin/env
# -*- codomg:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time


def getHtmlText(url):
    try:
        ua=UserAgent()
        headers={'User-Agent':ua.random,}
        res=requests.get(url,headers=headers,timeout=30)
        res.raise_for_status()
        res.encoding=res.apparent_encoding
        return res.text
    except:
        return ""

def getPageUrlList(PageL,start_url):
    try:
        html=getHtmlText(start_url)
        hrefs=re.findall(r'a href=\"http\:\/\/www\.mzitu\.com\/\d{6}\"',html)
        for i in range(len(hrefs)):
            href=eval(hrefs[i].split('=')[1])
            PageL.append(href)
    except:
        print('something wrong')

def getPageUrl(PageL,ImageL):
    for pageUrl in PageL:
        try:
            html=getHtmlText(pageUrl)
            pages=re.findall(r'\<span\>\d{1,3}\<\/span\>',html)
            t=pages[-1].split('<')[1]
            page=t.split('>')[1]
            for i in range(int(page)):
                a=str(i+1)
                url=pageUrl+'/'+a
                ImageL.append(url)
        except:
            print('something wrong')

def download(ImageL,count):
    try:
        for imgUrl in ImageL:
            html=getHtmlText(imgUrl)
            soup=BeautifulSoup(html,'html.parser')
            title=soup.select('.main-title')[0].text
            pageUrl=str(soup.select('.main-image')[0]).split('=')[-1].split('"')[1]
            ua=UserAgent()
            headers={'User-Agent':ua.random}
            res=requests.get(pageUrl,headers=headers,timeout=10)
            #filepath=os.getcwd().....
            with open('{}.jpg'.format(title),'wb') as f:
                f.write(res.content)
                time.sleep(3)
                count+=1
                print('｛｝下载完毕'.format(title))
    except:
        print('something wrong')

def main():
    count=1
    num=10
    start_url='http://www.mzitu.com/all/'
    PageL=[]
    ImageL=[]
    while count<num:
        getPageUrlList(PageL,start_url)
        getPageUrl(PageL,ImageL)
        download(ImageL,count)

main()


