# -*- coding:utf-8 -*-
# @Author: Wei Yi
# Reference: https://blog.csdn.net/yangyang_1009/article/details/19168055

import re

class FilterTag():
    def __init__(self):
        pass

    def filterHtmlTag(self, htmlStr):
        '''
        过滤html中的标签
        :param htmlStr:html字符串 或是网页源码
        '''
        self.htmlStr = htmlStr
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_n = re.compile('\\n') #除去\n
        re_t = re.compile('\\t') #除去\t
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlStr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        blank_line = re.compile('\n+')  # 去掉多余的空行
        s = blank_line.sub('\n', s)
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_n.sub('', s) #替换\n
        s = re_t.sub('', s) #替换\t
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        filterTag = FilterTag()
        s = filterTag.replaceCharEntity(s)  # 替换实体
        return  s

    def replaceCharEntity(self, htmlStr):
        '''
        替换html中常用的字符实体
        使用正常的字符替换html中特殊的字符实体
        可以添加新的字符实体到CHAR_ENTITIES 中
    CHAR_ENTITIES是一个字典前面是特殊字符实体  后面是其对应的正常字符
        :param htmlStr:
        '''
        self.htmlStr = htmlStr
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlStr)
        while sz:
            entity = sz.group()  # entity全称，如>
            key = sz.group('name')  # 去除&;后的字符如（" "--->key = "nbsp"）    去除&;后entity,如>为gt
            try:
                htmlStr = re_charEntity.sub(CHAR_ENTITIES[key], htmlStr, 1)
                sz = re_charEntity.search(htmlStr)
            except KeyError:
                # 以空串代替
                htmlStr = re_charEntity.sub('', htmlStr, 1)
                sz = re_charEntity.search(htmlStr)
        return htmlStr

    def replace(self, s, re_exp, repl_string):
        return re_exp.sub(repl_string)

    def strip_tags(self, htmlStr):
        '''
        使用HTMLParser进行html标签过滤
        :param htmlStr:
        '''

        self.htmlStr = htmlStr
        htmlStr = htmlStr.strip()
        htmlStr = htmlStr.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(htmlStr)
        parser.close()
        return ''.join(result)

    def stripTagSimple(self, htmlStr):
        '''
        最简单的过滤html <>标签的方法    注意必须是<任意字符>  而不能单纯是<>
        :param htmlStr:
        '''
        self.htmlStr = htmlStr
        #         dr =re.compile(r'<[^>]+>',re.S)
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        htmlStr = re.sub(dr, '', htmlStr)
        return htmlStr


#if __name__ == '__main__':
    #     s = file('Google.html').read()
#    filters = FilterTag()
#    print(filters.filterHtmlTag("n. 跳跃,上涨,惊跳 <br /><br />vt. 跳跃,跃过,突升,使跳跃 <br /><br />vi. \n \t跳跃,暴涨<br>"))