#! /usr/bin/python
# coding='utf-8'
"""
网易云音乐歌手粉丝地域分布热力图(一)：获取粉丝数据
Author: zhouzying
URL: www.zhouzying.cn
Data: 2018-10-19
"""
import requests
import codecs
import base64
import random
import math
from Crypto.Cipher import AES


# 获取粉丝页的json数据
def get_fans_json(url, data):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
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


# 获取粉丝地理位置
def get_location(uid):
    # 粉丝数据
    uri = 'https://music.163.com/weapi/user/playlist?csrf_token=cdee144903c5a32e6752f50180329fc9'
    # uid为粉丝id
    id_msg = '{uid: "' + str(uid) + '", wordwrap: "7", offset: "0", total: "true", limit: "36", csrf_token: "cdee144903c5a32e6752f50180329fc9"}'
    params, encSecKey = get_params(id_msg)
    data = {'params': params, 'encSecKey': encSecKey}
    userjson = get_fans_json(uri, data)
    if len(userjson["playlist"]) > 0:

        return userjson['playlist'][0]['creator']['city'], userjson['playlist'][0]['creator']['gender']
    else:
        print("id为{}用户没有创建歌单".format(uid))


# 构造包含昵称：地理位置的字典
def get_items(html):
    uinfos = []
    for item in html['followeds']:
        fans_items = {}
        fans_items['nickname'] = item['nickname']
        # gender=0 没有性别信息,gender=1表示男,gender=2表示女
        fans_items['location'], fans_items['gender'] = get_location(item['userId'])
        uinfos.append(fans_items)
    return uinfos


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
def get_params(id_msg):
    # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
    # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    # offset = (page-1) * 20
    # msg = '{offset":' + str(offset) + ',"limit":"20"}'
    # msg = '{"rid":"R_SO_4_1302938992","offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(id_msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)

    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey


# 歌手的粉丝页面,这里是薛之谦
# url = 'https://music.163.com/#/user/fans?id=97137413'
# 包含粉丝数据的页面的URL
# 歌手id
aid = '97137413'
url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=cdee144903c5a32e6752f50180329fc9'
page = 1

while page:
    offset = (page-1) * 20
    id_msg = '{userId: "' + aid + '", offset: ' + str(offset) + ', total: "true", limit: "20", csrf_token: "cdee144903c5a32e6752f50180329fc9"}'
    params, encSecKey = get_params(id_msg)
    data = {'params': params, 'encSecKey': encSecKey}
    html = get_fans_json(url, data)
    if html is None:

        break
    else:
        with open('fansinfo.txt', 'at', encoding='utf-8') as f:
            for item in get_items(html):
                f.write("{}\n".format(item))
        f.close()

    page += 1
