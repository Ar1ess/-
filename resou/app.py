from flask import Flask
import pymongo as pm
from flask import render_template
from lxml import etree
import requests
import webbrowser

app = Flask(__name__)


@app.route('/')
@app.route('/index')

def index():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    url = 'https://s.weibo.com/top/summary?sudaref=www.baidu.com&display=0&retcode=6102'

    data = requests.get(url, headers).text

    html = etree.HTML(data)

    titles = html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a/text()')
    urls = html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a/@href')
    nums = html.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/span/text()')

    nums = nums[::-1]
    nums.append(None)
    nums = nums[::-1]

    posts = []

    for i in range(len(urls)):
        dict = {}
        dict['title'] = titles[i]
        dict['url'] = 'https://s.weibo.com' + urls[i]
        dict['num'] = nums[i]
        posts.append(dict)

    return render_template("index.html", posts = posts)


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/', 2, False)
    app.run()

