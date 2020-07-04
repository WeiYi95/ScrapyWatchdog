# -*- coding:utf-8 -*-
# @Author: Wei Yi

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
import time
import scrapy

class SeleniumMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):

        #if request.meta.has_key('Selenium'):
        #D:\Python3.6.5\phantomjs-2.1.1-windows\bin
        if "Selenium_Jian" in request.meta:
            browser = webdriver.PhantomJS(executable_path='D:/Python3.6.5/phantomjs-2.1.1-windows/bin/phantomjs')
            browser.get(request.url)
            time.sleep(2)
            content = browser.page_source.encode("utf-8")
            browser.quit()
            return scrapy.http.HtmlResponse(request.url, body=content, request=request)

        if "Selenium_Fan" in request.meta:
            #browser = webdriver.PhantomJS(executable_path='D:/Python3.6.5/phantomjs-2.1.1-windows/bin/phantomjs')
            browser = webdriver.Firefox()
            browser.get(request.url)
            browser.find_element_by_xpath('//a[@id="textSwitch"]').click()
            content = browser.page_source.encode("utf-8")
            browser.quit()
            return scrapy.http.HtmlResponse(request.url, body=content, request=request)
