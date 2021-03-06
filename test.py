'''
Author: shixy
Date: 2021-12-18 15:56:02
LastEditTime: 2021-12-22 18:55:07
LastEditors: Please set LastEditors
Description: zhaoyangyongxu 
FilePath: \GL\test.py
'''
#%%
import pandas as pd
import numpy as np
from WindPy import w 
#%%
import sys
sys.path.append('D:\\实习文件\\GL\\SuntimePythonAPI\\x64\\py\\')
from SuntimePy import *
ZY.login("E000095608","355378Szw@")
#ZY.login("E00053778",'820163')

# %%查看流量
ZY.flowquery('zset')

#%% 小巨人股票代码
df=pd.read_csv('D:\实习文件\GL\东方财富专精特新小巨人20211219.csv')
df['代码']=[str(i).rjust(6,"0") for i in df['代码']]
df['代码']=[f'{i}.sh' if i[0]=='6' else f'{i}.sz' for i in df['代码']]
code=df['代码'].to_list()
#%%
ZY.zset("con_forecast_stk_wgt","",f"{code}","con_date=2021-01-01")

# %%
data=ZY.zset("con_forecast_stk_wgt","",code,"con_date=2021-01-01,con_year=2021")
data

# %%
ZY.zset("gs_rpt_goldstock","","","report_year=2020,report_period_type=19,create_date=2021-01-01")

# %%
money=pd.read_excel('D:\实习文件\GL\经济周期\金融机构人民币贷款平均利率(季).xls').iloc[2:]
date=[ pd.to_datetime(i).strftime('%Y-%m-%d')  for i in money['Wind'][-1000:]]
date=ZY.zdates('2017-01-01','2020-02-01')
#%%
w.start()
stock_list=w.wset("listedsecuritygeneralview","sectorid=a001010100000000;field=wind_code,sec_name")
stockdf=pd.DataFrame(stock_list.Data,index=stock_list.Fields,columns=stock_list.Codes).T
w.close()
# % 优秀分析师个股一致预期评级表
date_list=ZY.zdates('2017-01-01','2021-01-01')#974
code_list=[i.lower() for i in stock_list.Data[0]]
#%%
data_list=[]
for date in date_list:
    print(date)
    data=ZY.zset("con_forecast_stk_wgt","",code_list,f"con_date={date},con_year={date[:4]}")
    if type(data)==pd.core.frame.DataFrame:
        data_list.append(data)
    else:
        print(f'{date} error')
    
    

# %%
forecast=pd.concat(data_list)
forecast.to_pickle('分析师预测加权.pkl')
# %%
data=ZY.zset("con_forecast_stk_wgt","",code_list,f"con_date={date},con_year=2021")
data
# %%

ZY.zset("gs_rpt_goldstock","","",f"report_year={date[:4]},report_period_type={date[5:7]},create_date={date}")
# %%
code_list1=[i[:6] for i in code_list]
data_list=[]
for date in ZY.zdates('2017-01-01','2017-01-30'):
    data=ZY.zset("pt_der_indicator_all","",code_list,f"trade_date={date}")
    if type(data)==pd.core.frame.DataFrame:
        data_list.append(data)
        print(date)
    else:
        print(f'{date} has no data')
# %%
# %%
ZY.zset("pt_der_indicator_all","",f"{code_list1}",f"trade_date=2019-05-04")
# %%
data=ZY.zset("pt_der_indicator_fmgb","",f"{code_list1}","trade_date=2018-04-30")
data
# %%
data=ZY.zset("pt_der_qlty_indicator","",f"{code_list1}","trade_date=2020-01-01,ptype_code=1")
data
# %%
