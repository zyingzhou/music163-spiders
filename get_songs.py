#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: zhiying
URL: www.zhouzying.cn
Date: 2018-9-9
Update: 2019-8-5
Description: 爬取网易云音乐歌手热门歌曲（更新）
"""
import requests
import csv
from bs4 import BeautifulSoup
from requests import RequestException
import time


def parse_html_page(url):
    """
    :param url: 带有歌手id的url
    :return: 歌手的热门歌曲id以及歌曲名字
    """
    # 使用双引号会出现 Unresolve reference
    # pattern = '<span class="txt"><a href="/song?id=(\d*)"><b title="(.*?)">'
    # 这里是使用lxml解析器进行解析,lxml速度快,文档容错能力强,也能使用html5lib
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/66.0.3359.181 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200 and r.text:
            r.encoding = 'utf-8'
            html = r.text
            # 模式为：<ul class="f-hide"><li><a href="/song?id=65766">富士山下</a></li>
            soup = BeautifulSoup(html, 'html5lib')
            ul_tag = soup.find_all('ul', 'f-hide')
            ul_tag = BeautifulSoup(str(ul_tag), 'html5lib')
            items = ul_tag.find_all('li')
            # 返回内容：<li><a href="/song?id=65766">富士山下</a></li>
            return items
    except RequestException as err:
        print(err)
        pass


# 这里以获取薛之谦的热门歌曲为例
# url = "https://music.163.com/artist?id=5781"
# html = get_html_src(url)

# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(items, artist_name):

    with open("music163_songs.csv", "a", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["歌手名字", artist_name])

        for item in items:
            writer.writerow([item.a['href'].replace('/song?id=', ''), item.a.text])

            # 可视化显示
            # print('歌曲id:', item.a['href'].replace('/song?id=', ''))
            # song_name = item.b['title']
            # print('歌曲名字:', song_name)

    csvfile.close()


# 获取歌手id和歌手姓名
def read_csv():

    with open("music163_artists.csv", "r", encoding="utf-8") as csvfile:

        reader = csv.reader(csvfile)
        for row in reader:
            artist_id, artist_name = row
            if str(artist_id) is "artist_id":
                continue
            else:
                yield artist_id, artist_name
    # 当程序的控制流程离开with语句块后, 文件将自动关闭


def main():
    for readcsv in read_csv():
        artist_id, artist_name = readcsv
        print('正在获取{}的热门歌曲'.format(artist_name))
        url = 'https://music.163.com/artist?id=' + str(artist_id)
        items = parse_html_page(url)
        print('正在写入。。。')
        write_to_csv(items, artist_name)
        print('{}的热门歌曲获取成功！'.format(artist_name))
        time.sleep(3)


if __name__ == "__main__":
    main()
