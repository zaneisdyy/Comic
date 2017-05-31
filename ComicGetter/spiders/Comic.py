# -*- coding: utf-8 -*-
import scrapy
import os
import re
import requests
from bs4 import BeautifulSoup


class ComicSpider(scrapy.Spider):
    name = 'Comic'
    
    start_urls = ['http://manhua.fzdm.com/131/']

    def parse(self, response):
        content = response.body;
        soup = BeautifulSoup(content, "html.parser")
        Comiclist = soup.find_all('li', attrs={'class':'pure-u-1-2 pure-u-lg-1-4'})
        '''for href in Comiclist:
        	try:
	        	url = 'http://manhua.fzdm.com/131/' + href.a['href'][:-1]
	        	self.title = href.a['href'][:-1]
	        	print(url)'''
        url = 'http://manhua.fzdm.com/131/01'
        self.title = '01' 
        yield scrapy.Request(url, callback=self.comic_parse)
            #except:
        	#continue'''

    def comic_parse(self, response):
        content = response.body;
        soup = BeautifulSoup(content, "html.parser")
        #单个页面上获取图片地址
        jpg_key = 'mhpic'
        jpg_tag = soup.find('img', attrs={'id':jpg_key})
        jpg_url = jpg_tag['src'] 
        
        #图片保存到本地
        self.jpg_save(jpg_url)

        #下一页漫画地址
        page_tag = soup.find_all('div', attrs={'class':'navigation'})[0]
        page_url_tag = page_tag.find_all('a')[-1]
        page_url = page_url_tag['href']

        #最后一页
        if page_url_tag.next_sibling == '最后一页了':
           pass
        else:
            url = 'http://manhua.fzdm.com/131/' + self.title +'/'+ page_url
            yield scrapy.Request(url, callback=self.comic_parse)

    def jpg_save(self, jpg_url):
        path = "D://Dyy//Study//python//PythonProjects//scrapy//ComicGetter//" + jpg_url.split('/')[-1]
        jpg_url = 'http:' + jpg_url
        r = requests.get(jpg_url)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            #

