# -*- coding:utf-8 -*-
# @Author: Wei Yi

import scrapy
import HtmlFilter
from scrapy.selector import Selector
#from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
import re
from ..items import TextItem, ImageItem, PicWordItem
import time
#from scrapy_redis.spiders import RedisSpider
import requests
import os
import collections

class SikuSpider(scrapy.Spider):
    """
    经部：
    http://skqs.guoxuedashi.com/wen_1h/
    1 - 79733
    史部：
    http://skqs.guoxuedashi.com/wen_502w/
    7665 - 79987
    子部：
    http://skqs.guoxuedashi.com/wen_1026j/
    26405 - 34155
    集部：
    http://skqs.guoxuedashi.com/wen_1819r/
    41752 - 53216
    #814879
    """
    #http://skqs.guoxuedashi.com/wen_299a/4056.html
    name = "sbook"
    filters = HtmlFilter.FilterTag()
    start_url = ["http://skqs.guoxuedashi.com/wen_1h/"]
    st = [37200]
    tot = [81489]
    url_dict = collections.defaultdict(int)

    def start_requests(self):
        try:
            with open("record.txt",'r',encoding='utf-8') as rfile:
                c = rfile.read()
                c = c.split('\n')
                for u in c:
                    self.url_dict[u] += 1
        except:
            with open("record.txt", 'w', encoding="utf-8") as tfile:
                pass
        # for u in self.start_url:
        # len(self.start_url)
        for j in range(len(self.start_url)):
            u = self.start_url[j]
            # 4056,4058
            for i in range(self.st[j], self.tot[j]):
                url = u + str(i) + ".html"
                if self.url_dict[url] == 0:
                    self.url_dict[url] = 1
                    with open("record.txt", 'a', encoding='utf-8') as afile:
                        afile.write(url + '\n')
                    try:
                        request = scrapy.Request(url=url, callback=self.parseText)
                        yield request
                    except:
                        continue

    def parseText(self, response):
        try:
            info_list = response.selector.xpath('//div[@class="info_tree"]').extract()
            book_info = ""
            if info_list != []:
                book_info = self.getInfo(info_list[0])
            page_url = response.url
            content = self.getContent(response.url)
            if content == "Time-out":
                return
            img_list = re.findall(r"imglist\[.*;", content)
            img_list, url_dict = self.getUrl(img_list)
            line_cnt = 0
            tot_text = response.selector.xpath('//span[@class="tline"]').extract()
            length = len(tot_text)
            while line_cnt < length - 1:
                line = tot_text[line_cnt]
                imageitem = ImageItem()
                myitem = TextItem()
                order = None
                flag = False
                text = ""
                exist = False
                if re.search(r"\[\d", line) != None:
                    order = self.filters.filterHtmlTag(line)
                    order = order.strip()
                    name = book_info + order
                    path, file_name = self.getDir(name)
                    file = path + '\\' + file_name + ".png"
                    if os.path.exists(file):
                        exist = True
                        break
                    i = line_cnt + 1
                    for j in range(i, length):
                        line_cnt += 1
                        line = tot_text[j]
                        if re.search(r"\[\d", line) != None:
                            line_cnt -= 1
                            break
                        while line.find("<span class='krp-note'>") != -1:
                            line = line.replace("<span class='krp-note'>", '[', 1)
                            line = line.replace("</span>", ']', 1)
                        while line.find('<span class="krp-note">') != -1:
                            line = line.replace('<span class="krp-note">', '[', 1)
                            line = line.replace("</span>", ']', 1)
                        site = []
                        first = True
                        while line.find('<img height="20" width="20" src="') != -1:
                            if first:
                                site = re.findall("http://.*?\.png", line)
                                first = False
                            line = line.replace('<img height="20" width="20" src="', '{', 1)
                            line = line.replace('.png">', '}', 1)
                            line = line.replace("http://siku.guoxuedashi.com/ziimg/images/", "", 1)
                        if site != []:
                            for u in site:
                                PWItem = PicWordItem()
                                PWItem["image_url"] = u
                                yield PWItem
                        line = self.filters.filterHtmlTag(line)
                        if flag:
                            text += '-'
                        text += line.strip()
                        flag = True
                if order != None and (not exist):
                    order = order.strip()
                    if order in url_dict.keys():
                        img_url = url_dict[order]
                        name = book_info + order
                        myitem["book_info"] = name
                        imageitem["img_info"] = name
                        imageitem["image_url"] = img_url
                        myitem["url"] = page_url
                        myitem["text"] = text
                        myitem["img_url"] = img_url
                        yield myitem
                        yield imageitem
                else:
                    line_cnt += 1
        except:
            pass

    def getUrl(self, res):
        l = []
        url_dict = {}
        for i in range(len(res)):
            pos = res[i].find("]='http:")
            if pos != -1:
                url = res[i][pos + 3:-2]
                l.append(url)
                p1 = res[i].find("['")
                p1 += 6
                name = '[' + res[i][p1:pos - 1] + ']'
                url_dict[name] = url
        return l, url_dict

    def getDir(self,s):
        pre = "g:\\SK_BOOK"
        list = s.split("~")
        path = pre
        for i in range(0,len(list)-1):
            path = path + "\\" + list[i]
        file_name = s.replace("~","_")
        return path,file_name

    def getContent(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        try:
            re = requests.get(url, headers=header, timeout=15)
        except:
            return "Time-out"
        re.encoding = "utf-8"
        text = re.text
        return text

    def getInfo(self, s):
        s = s.replace('\r\n', "")
        s = self.filters.filterHtmlTag(s)
        s = s.replace(" > ", "~")
        s = s.strip()
        s = s[3:] + "~"
        return s