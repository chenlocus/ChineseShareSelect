# coding:utf8
import configparser

import flask
from flask import render_template

from stock_query import stock_check, result_parse, get_stock, get_shares, get_shengangtong

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if flask.request.method == 'GET':
        result = {}
        return render_template("homepage.html", result=result)
    elif flask.request.method == 'POST'and flask.request.form.get('query', None) == "查询":
        stock_no = flask.request.form['storkcode']
        code = stock_check(stock_no)
        if code != 0:
            result = result_parse(get_stock(code))
            return render_template("homepage.html", result=result)
        else:
            return render_template("homepage.html", warning="请输入正确的股票代码")

@app.route('/getshares', methods=['GET', 'POST'])
def get_sharelist():
    if flask.request.method == 'GET':
        result = {}
        return render_template("getshares.html", result=result)
    elif flask.request.method == 'POST'and flask.request.form.get('query', None) == "查询":
        div_yield = float(flask.request.form['divyield'])/100
        price_earning = flask.request.form['pe']
        total_asset = flask.request.form['totalasset']
        if (div_yield != 0)&(price_earning !=0):
            codetable = get_shares(div_yield,price_earning,total_asset)
            return render_template('getshares.html',tables=[codetable.to_html(classes='stock')],titles = ['na','股票列表'])
        else:
            return render_template("getshares.html", warning="请输入股息率和市盈率要求")

@app.route('/getshengangtong', methods=['GET', 'POST'])
def getshengangtonglist():
    if flask.request.method == 'GET':
        result = {}
        return render_template("getshengangtong.html", result=result)
    elif flask.request.method == 'POST'and flask.request.form.get('query', None) == "查询":
        shengangtong = bool(flask.request.form['domain']=='shengangtong')
        price_earning = flask.request.form['pe']
        total_asset = flask.request.form['totalasset']
        if (total_asset != 0)&(price_earning !=0):
            codetable = get_shengangtong(shengangtong,price_earning,total_asset)
            return render_template('getshengangtong.html',tables=[codetable.to_html(classes='stock')],titles = ['na','股票列表'])
        else:
            return render_template("getshengangtong.html", warning="请输入股息率和市盈率要求")



if __name__ == '__main__':
    #app.run(debug=False, threaded=True, host='127.0.0.1', port=4501)
    app.run(debug=False, threaded=True)