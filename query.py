#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import re

# debug=True
debug = False


class Utility:
    def ToGB(str):
        if (debug): print(str)
        return str.decode('gb2312')


class StockInfo:
    """
     0: 未知
     1: 名字
     2: 代码
     3: 当前价格
     4: 涨跌
     5: 涨跌%
     6: 成交量（手）
     7: 成交额（万）
     8:
     9: 总市值"""

    def GetStockStrByNum(num):
        f = urllib.request.urlopen('http://qt.gtimg.cn/q=s_' + str(num))
        print('res=', f.read().decode('gbk'))
        res = f.readline()
        f.close()
        return res


    def ParseResultStr(resultstr):
        if (debug): print(resultstr)
        slist = resultstr[14:-3]
        if (debug): print(slist)
        slist = slist.split('~')
        if (debug): print(slist)

        # print('*******************************')
        print('股票名称:', slist[1])
        print('股票代码:', slist[2])
        print('当前价格:', slist[3])
        print('涨    跌:', slist[4])
        print('涨   跌%:', slist[5], '%')
        print('成交量(手):', slist[6])
        print('成交额(万):', slist[7])
        # print('date and time is :', dateandtime)
        print('*******************************')

    def GetStockInfo(num):
        str = StockInfo.GetStockStrByNum(num)
        strGB = Utility.ToGB(str)
        StockInfo.ParseResultStr(strGB)


if __name__ == '__main__':
    code = input("请输入股票代码:")
    no_list = re.findall(r'[0-9]', code)
    no = no_list[0]
    if int(no) == 6:
        code1 = 'sh' + code
        print(code1)
    elif (int(no) == 0) | (int(no) == 3):
        code1 = 'sz' + code
        print(code1)
    else:
        print("请输入正确的股票代码")
    stocks = [code1]
    print("stocks=", stocks)
    for stock in stocks:
        StockInfo.GetStockInfo(stock)
