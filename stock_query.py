# -*- coding:utf-8 -*-
import urllib.request

#newly added codes
import pandas as pd
import tushare as ts



def get_stock(stock_no):
    # 使用腾讯股票查询接口进行查询
    f = urllib.request.urlopen('http://qt.gtimg.cn/q=s_' + str(stock_no))
    res = f.read().decode('gbk')
    f.close()
    return res


def result_parse(result):
    res_dict = {}
    result_spl = result[14:-3].split('~')
    res_dict['stock_name'] = result_spl[1]
    res_dict['stock_no'] = result_spl[2]
    res_dict['current_price'] = result_spl[3]
    res_dict['fluctuation'] = result_spl[4]
    res_dict['fluctuation_by_percent'] = result_spl[5]
    res_dict['volume'] = result_spl[6]
    res_dict['turnover'] = result_spl[7]
    return res_dict


def stock_check(stock_no):
    if len(stock_no) != 6:
        return 0
    no_first = stock_no[0]
    if int(no_first) == 6:
        code = 'sh' + stock_no
        return code
    elif (int(no_first) == 0) | (int(no_first) == 3):
        code = 'sz' + stock_no
        return code
    else:
        return 0


def stock_query():
    # 此方法用于不进行web交互查询
    stock_no = input("请输入股票代码:")
    code = stock_check(stock_no)
    if code != 0:
        result = result_parse(get_stock(code))
        print('**************查询结果*****************')
        print('股票名称:', result['stock_name'])
        print('股票代码:', result['stock_no'])
        print('当前价格:', result['current_price'])
        print('涨    跌:', result['fluctuation'])
        print('涨   跌(%):', result['fluctuation_by_percent'], '%')
        print('成交量(手):', result['volume'])
        print('成交额(万):', result['turnover'])
        print('**************查询结果*****************')
    else:
        print('请输入正确的股票代码')

#newly added codes to get share list 

# def sharelist_parse(result):
#     res_table = result[['name','code','trade','changepercent','per','mktcap','volume']]
#     return res_table
    

def get_shares(div_yield,price_earning,total_asset):
    if total_asset !=0:
        total_asset =total_asset*10000
    else:
        total_asset =6000*10000
    div_yield = float(div_yield)
    price_earning = float(price_earning)
    total_asset = float(total_asset)
    df1 = ts.get_today_all()
    df2 = ts.profit_data(top =2000)
    df15= df1[(df1['per']<price_earning) & (df1['per']>0)]
    result = pd.merge(df15, df2, on=['code', 'name'])
    criteria1 = result[(result['low']>0) & (result['divi']/(10*result['low'])>div_yield) & (result['mktcap']<total_asset)]
    #criteria1.set_index('code', inplace=True)
    res_table = criteria1[['name','code','trade','changepercent','per','mktcap','volume']].reset_index(drop=True)
    print (res_table)
    return res_table

def get_shengangtong(shengangtong,price_earning,total_asset):
    price_earning = float(price_earning)
    total_asset = float(total_asset)

    pd = ts.get_stock_basics()
    if shengangtong:
        sgtSet=pd[pd.index.str[:3].isin(['300', '000'])]
    else:
        sgtSet =pd
    sgtSet5080 = sgtSet[(sgtSet['pe']*sgtSet['esp']*sgtSet['totals']<total_asset*10000)]
    sgt=sgtSet5080[(sgtSet5080['pe']<price_earning)&(sgtSet5080['pe']>0)]
    print (sgt)
    sgtResult = sgt[['name','industry','area','pe','totalAssets','pb']].reset_index(drop=False)
    return sgtResult
