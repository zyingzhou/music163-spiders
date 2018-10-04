#! /usr/bin/env python
# coding='utf-8'

'''

获取网易云音乐歌曲全部评论
Author: zhouzying
URL: https://www.zhouzying.cn
Date: 2018-09-14
Update: 2018-09-27         Add data argument.
Update: 2018-10-04         Get replied comments and add users name who shared comments.

'''


import requests
import math
import random
# pycrypto
from Crypto.Cipher import AES
import codecs
import base64


# 构造函数获取歌手信息
def get_comments_json(url, data):
    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Connection': 'keep-alive',
             'Cookie': 'WM_TID=36fj4OhQ7NdU9DhsEbdKFbVmy9tNk1KM; _iuqxldmzr_=32; _ntes_nnid=26fc3120577a92f179a3743269d8d0d9,1536048184013; _ntes_nuid=26fc3120577a92f179a3743269d8d0d9; __utmc=94650624; __utmz=94650624.1536199016.26.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_NI=2Uy%2FbtqzhAuF6WR544z5u96yPa%2BfNHlrtTBCGhkg7oAHeZje7SJiXAoA5YNCbyP6gcJ5NYTs5IAJHQBjiFt561sfsS5Xg%2BvZx1OW9mPzJ49pU7Voono9gXq9H0RpP5HTclE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5cb8085b2ab83ee7b87ac8c87cb60f78da2dac5439b9ca4b1d621f3e900b4b82af0fea7c3b92af28bb7d0e180b3a6a8a2f84ef6899ed6b740baebbbdab57394bfe587cd44b0aebcb5c14985b8a588b6658398abbbe96ff58d868adb4bad9ffbbacd49a2a7a0d7e6698aeb82bad779f7978fabcb5b82b6a7a7f73ff6efbd87f259f788a9ccf552bcef81b8bc6794a686d5bc7c97e99a90ee66ade7a9b9f4338cf09e91d33f8c8cad8dc837e2a3; JSESSIONID-WYYY=G%5CSvabx1X1F0JTg8HK5Z%2BIATVQdgwh77oo%2BDOXuG2CpwvoKPnNTKOGH91AkCHVdm0t6XKQEEnAFP%2BQ35cF49Y%2BAviwQKVN04%2B6ZbeKc2tNOeeC5vfTZ4Cme%2BwZVk7zGkwHJbfjgp1J9Y30o1fMKHOE5rxyhwQw%2B%5CDH6Md%5CpJZAAh2xkZ%3A1536204296617; __utma=94650624.1052021654.1536048185.1536199016.1536203113.27; __utmb=94650624.12.10.1536203113',
             'Host': 'music.163.com',
             'Referer': 'http://music.163.com/',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/66.0.3359.181 Safari/537.36'}

    try:
        r = requests.post(url, headers=headers, data=data)
        r.encoding = "utf-8"
        if r.status_code == 200:

            # 返回json格式的数据
            return r.json()

    except:
        print("爬取失败!")


# 生成16个随机字符
def generate_random_strs(length):
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 控制次数参数i
    i = 0
    # 初始化随机字符串
    random_strs  = ""
    while i < length:
        e = random.random() * len(string)
        # 向下取整
        e = math.floor(e)
        random_strs = random_strs + list(string)[e]
        i = i + 1
    return random_strs


# AES加密
def AESencrypt(msg, key):
    # 如果不是16的倍数则进行填充(paddiing)
    padding = 16 - len(msg) % 16
    # 这里使用padding对应的单字符进行填充
    msg = msg + padding * chr(padding)
    # 用来加密或者解密的初始向量(必须是16位)
    iv = '0102030405060708'

    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 加密后得到的是bytes类型的数据
    encryptedbytes = cipher.encrypt(msg)
    # 使用Base64进行编码,返回byte字符串
    encodestrs = base64.b64encode(encryptedbytes)
    # 对byte字符串按utf-8进行解码
    enctext = encodestrs.decode('utf-8')

    return enctext


# RSA加密
def RSAencrypt(randomstrs, key, f):
    # 随机字符串逆序排列
    string = randomstrs[::-1]
    # 将随机字符串转换成byte类型数据
    text = bytes(string, 'utf-8')
    seckey = int(codecs.encode(text, encoding='hex'), 16)**int(key, 16) % int(f, 16)
    return format(seckey, 'x').zfill(256)


# 获取参数
def get_params(page):
    # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
    # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    # 偏移量
    offset = (page-1) * 20
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
    msg = '{"offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)

    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey


def hotcomments(html, songname, i, pages, total, filepath):
    # 写入文件
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write("正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    print("正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))

    # 精彩评论
    m = 1
    # 键在字典中则返回True, 否则返回False
    if 'hotComments' in html:
        for item in html['hotComments']:
            # 提取发表热门评论的用户名
            user = item['user']
            # 写入文件
            print("热门评论{}: {} : {}    点赞次数: {}".format(m, user['nickname'], item['content'], item['likedCount']))
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write("热门评论{}: {} : {}   点赞次数: {}\n".format(m, user['nickname'], item['content'], item['likedCount']))
                # 回复评论
                if len(item['beReplied']) != 0:
                    for reply in item['beReplied']:
                        # 提取发表回复评论的用户名
                        replyuser = reply['user']
                        print("回复：{} : {}".format(replyuser['nickname'], reply['content']))
                        f.write("回复：{} : {}\n".format(replyuser['nickname'], reply['content']))
            m += 1


def comments(html, songname, i, pages, total, filepath):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write("\n正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    print("\n正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    # 全部评论
    j = 1
    for item in html['comments']:
        # 提取发表评论的用户名
        user = item['user']
        print("全部评论{}: {} : {}    点赞次数: {}".format(j, user['nickname'], item['content'], item['likedCount']))
        with open(filepath, 'a', encoding='utf-8') as f:

            f.write("全部评论{}: {} : {}   点赞次数: {}\n".format(j, user['nickname'], item['content'], item['likedCount']))
            # 回复评论
            if len(item['beReplied']) != 0:
                for reply in item['beReplied']:
                    # 提取发表回复评论的用户名
                    replyuser = reply['user']
                    print("回复：{} : {}".format(replyuser['nickname'], reply['content']))
                    f.write("回复：{} : {}\n".format(replyuser['nickname'], reply['content']))

        j += 1


def main():

    # 歌曲id号
    songid = 38592976

    # 歌曲名字
    songname = "Dream it possible"
    # 文件存储路径
    filepath = songname + ".txt"
    page = 1
    params, encSecKey = get_params(page)

    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(songid) + '?csrf_token='
    data = {'params': params, 'encSecKey': encSecKey}
    # url = 'https://music.163.com/#/song?id=19292984'
    # 获取第一页评论
    html = get_comments_json(url, data)
    # 评论总数
    total = html['total']
    # 总页数
    pages = math.ceil(total / 20)
    hotcomments(html, songname, page, pages, total, filepath)
    comments(html, songname, page, pages, total, filepath)

    # 开始获取歌曲的全部评论
    page = 2
    while page <= pages:

        params, encSecKey = get_params(page)
        data = {'params': params, 'encSecKey': encSecKey}
        html = get_comments_json(url, data)
        # 从第二页开始获取评论
        comments(html, songname, page, pages, total, filepath)
        page += 1


if __name__ == "__main__":
    main()

