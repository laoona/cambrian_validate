# /usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
"""
tool.py

Authors: work (work@baidu.com)
Date:    2017/06/07 22:44
"""
import requests as requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import SNIMissingWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
import logging as log
from lxml import etree
import traceback
import sys
from validator import mipValidator
from validator import canonicalValidator
from validator import jsonldValidator
from validator import h5Validator

log.basicConfig(
    format=
    '%(asctime)s\t%(name)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s',
    level=log.INFO,
)


def pageEncode(func):
    """

    :param content: page content
    :return:
    """

    def wrapper(url):
        """

        :param url: page url
        :return:
        """
        content = func(url)
        try:
            if content == False:
                return False
            html = etree.HTML(content)
            meta = html.xpath('//head/meta[@charset]')
            if len(meta) == 0:
                meta = html.xpath('//head/meta[@http-equiv]')
                if len(meta) > 0:
                    for tag in meta:
                        if tag.get('http-equiv').lower() == 'content-type':
                            c = tag.get('content').lower()
                            c = c.split('charset=')
                            encoding = c[1]
                            break
                else:
                    # 自己检测编码，并进行转换
                    import chardet
                    ret = chardet.detect(content)
                    encoding = ret['encoding']
            else:
                meta = meta.pop()
                encoding = meta.get('charset')

            encoding = str(encoding).upper()
            if encoding == 'UTF-8':
                return content
            if encoding.startswith("GB"):
                return content.decode("").encode('UTF-8')
        except Exception as e:
            # traceback.print_exc(file=sys.stdout)
            # log.warning("解析页面编码失败")
            return content.encode('UTF-8')

    return wrapper


@pageEncode
def request(url):
    """
    get page content
    :param: url 请求网页url
    """
    try:
        if url.find("http") == -1:
            print "url lost http protocol header"
            url = "http://" + url
        response = requests.get(url, verify=False)
        return response.text
    except Exception as e:
        # traceback.print_exc(file=sys.stdout)
        log.warning("请求 url %s 失败 %s" % (url, e.args))
    return False


def validator(is_mip, url):
    """
    validate
    :param: is_mip 是否mip页面，True/False,非mip会当做h5页面对待
    :param: url 请求的url地址
    """
    try:
        sContent = request(url)
        if not sContent:
            sys.exit(0)

        if is_mip:
            mipErr = mipValidator(sContent)
            if mipErr[0]:
                print "mip链接校验通过"
            else:
                print "如果不使用顶bar功能请忽略"
                print "mip链接校验不通过，错误原因:"
                for (k, v) in mipErr[1].iteritems():
                    print v
        else:
            h5Err = h5Validator(sContent)
            if h5Err[0]:
                print "h5链接校验通过"
            else:
                print "如果不使用顶bar功能请忽略"
                print "h5链接校验不通过，错误原因:"
                for (k, v) in h5Err[1].iteritems():
                    print v

        canErr = canonicalValidator(sContent)
        if canErr[0]:
            print "canonical标签校验通过"
        else:
            print "canonical标签校验不通过，错误原因："
            for (k, v) in canErr[1].iteritems():
                print v

        jsonldErr = jsonldValidator(sContent, url)
        if jsonldErr[0]:
            print "jsonld数据校验通过"
        else:
            print "jsonld校验不通过，错误原因:"
            for (k, v) in jsonldErr[1].iteritems():
                print v

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        log.warning("%s", e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python validator.py is_mip url"
        print "is_mip: 1 mip 0 not mip"
        print "url: url address"
        sys.exit(0)

    del sys.argv[0]
    is_mip, url = sys.argv

    validator(bool(int(is_mip)), url)
