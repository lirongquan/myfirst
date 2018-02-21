#!/usr/bin/env python
# encoding=utf-8
import requests
import  datetime
import time
import re
import codecs
from bs4 import BeautifulSoup
from openpyxl import Workbook
wb = Workbook()
now_time =  datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  #获取当前时间，将文件名和时间相结合
dest_filename = now_time + '职位.xlsx'    #定义文件名称，此处为xlsx文件
ws1 = wb.active                    #激活默认sheet
ws1.title = "职位法务"            #将sheet名称进行更改

#DOWNLOAD_URL = 'http://movie.douban.com/top250/'
#DOWNLOAD_URL = 'http://www.45pcpc.com'
DOWNLOAD_URL = 'http://xa.58.com/job/?key=法务&final=1&jump=1'   #定义要抓取的网页地址

#获取网页源码文件

def download_page(url):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data

#######对源码文件进行分析##########################
"""
主要 分析标签结构关系，第一步找到模块信息标签， 第二步找到需要元素信息模块   第三步：获取信息值内容

"""



row = 0 #行指针为0，全局参数，因为要讲所有页面数据写入同一个文件，用于写入excel文件单元格行位置。

def getinfo(URL,row):
    
    doc = download_page(URL)  #通过调用函数获取页面内容
    soup = BeautifulSoup(doc, 'html.parser') #使用BS4对网页进行解析
    
    for link in soup.find_all('li', class_="job_item clearfix"):  #通过findall找到所有模块信息
        
        name = link.find('span', class_="name").get_text()  #找到具体元素信息
        salary = link.find('p',class_="job_salary").get_text() #找到具体元素信息
        address = link.find('span', class_="address").get_text() #找到具体元素信息
        company = link.find('a', class_="fl").get_text() #找到具体元素信息
    
        print("% s   %s  %s" %(name,salary,company))
        row = row + 1 # 行指针依次往下挪动
        col_A = 'A%s' %row
        col_B = 'B%s' %row
        col_C = 'C%s' %row
        col_D = 'D%s' %row
        ws1[col_A] = company
        ws1[col_B] = name
        ws1[col_C] = salary
        ws1[col_D] = address
    page = soup.find('a', class_="next").get('href') # 获取下一页
    
    if page: #设置递归函数出口条件，当没有下一页时候，停止递归
        return getinfo(page,row) #进行递归，解析并获取下一页数据


if __name__ == "__main__":

    
    getinfo(DOWNLOAD_URL,row) #全局调用
    
    wb.save(filename=dest_filename)  #所有数据写入exlcel文件后，保存文件并关闭。
