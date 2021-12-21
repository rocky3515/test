'''
Author: your name
Date: 2021-12-18 15:56:02
LastEditTime: 2021-12-19 00:03:13
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \GL\test.py
'''

#%%
from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
import time
import datetime
import pandas as pd

import os
import pymssql
from bs4 import BeautifulSoup
import numpy as np
import logging


import warnings
warnings.filterwarnings('ignore')
# %%
opt=webdriver.ChromeOptions() # 创建浏览
#opt.add_argument('--headless') #无窗口模式

chromedriverpath ='D:\实习文件\爬虫\chromedriver_win32\chromedriver.exe'
browser = webdriver.Chrome(chromedriverpath,options=opt)

# 打开网页链接
web='http://quote.eastmoney.com/center/boardlist.html#boards-BK10051'
browser.get(web)
time.sleep(10)
# %% 获取内容
def get_web_content(browser):
    cont=browser.find_element_by_xpath('//table[@class="table_wrapper-table"]').text
    cont_list=cont.split('\n')
    df=pd.DataFrame([i.split(' ') for i in cont_list])
    df.columns=df.iloc[0,:]
    df=df.iloc[1:]
    return df
# %% 获取总页数
page=browser.find_element_by_xpath('//span[@class="paginate_page"]').text
click_num=int(page[-2:])-1
num=0
df_list=[]
while num<click_num:
    df=get_web_content(browser)
    df_list.append(df)
    browser.find_element_by_xpath('//a[@class="next paginate_button"]').click()
    time.sleep(1)
    num+=1
    print(f'第{num}页内容已获取')
    

# %% 数据存储
total=pd.concat(df_list).reset_index(drop=True)
name_list=[i for i in total.columns if i not in ['相关链接','加自选',None,]]
total.drop(['相关链接','最新价','涨跌幅'],axis=1,inplace=True)
total.columns=name_list
day=datetime.datetime.today().strftime('%Y%m%d')
total['date']=day
total.to_csv(f'东方财富专精特新小巨人{day}.csv')


# %%
