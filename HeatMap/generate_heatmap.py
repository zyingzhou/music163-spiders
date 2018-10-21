#! /usr/bin/python
# coding='utf-8'
"""
制作网易云音乐歌手粉丝地域分布热力图(二)：统计相同地域的粉丝个数,再对地域进行经纬度转换,最后制作热力图的网页文件
Author: zhouzying
URL: www.zhouzying.cn
Data: 2018-10-21
"""

import json
import requests
from bs4 import BeautifulSoup
from urllib.request import quote, urlopen


# 获取城市编码,返回一个键是城市编码,值为中文地理位置的字典
def get_loccodes():
    # 中华人民共和国行政区划代码
    url = 'http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/20180810101641.html'
    locs = {}
    try:
        r = requests.get(url)
        if r.status_code == 200:
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, 'html5lib')
            items = soup.find_all('tr', attrs={"height": "19"})
            # 城市编码的个数
            print(print(len(items)))
            for item in items:
                # 提取数据
                # print(item.find_all('td')[1].text, item.find_all('td')[2].text)
                locs[item.find_all('td')[1].text] = item.find_all('td')[2].text
    except:
        print("获取失败！")

    # 可视化输出
    # print(locs)
    return locs


# 返回格式为{"中文地理位置": "该地理位置的粉丝个数"}的字典
def convert_code_loc(locs):
    counts = {}
    ls = []
    i = 1
    for line in open('fansinfo.txt', encoding='utf-8').readlines():
        ls.append(eval(line)['location'])
        i += 1
    # 用于计算粉丝个数
    # print("有{}行".format(i))
    for word in ls:
        counts[word] = counts.get(word, 0) + 1
    loc_counts = {}
    # 统计没有对应中文地理位置的城市编码个数
    j = 1
    for key in counts.keys():
        if str(key) in locs:
            loc_counts[locs[str(key)]] = counts[key]
        else:
            print("城市编码为{}没有对应的中文地理位置".format(key))
            j += 1
            pass
    # 统计没有对应中文地址的编码个数
    # print("总共有{}个城市编码没有对应的中文地理位置".format(j))
    # print(loc_counts)
    return loc_counts


# 获取地理位置的经纬度
def getlnglat(address):
    url = "http://api.map.baidu.com/geocoder/v2/"
    output = 'json'
    # 密钥需要到百度开发者平台申请
    ak = '这里填写自己的密钥'
    addr = quote(address)
    uri = url + '?' + 'address=' + addr + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    return temp


# 生成热力图
def generate_map(loc_counts):

    # html文件的头
    header = """<!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
        <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=这里填写你的密钥"></script>
        <script type="text/javascript" src="http://api.map.baidu.com/library/Heatmap/2.0/src/Heatmap_min.js"></script>
        <title>热力图功能示例</title>
        <style type="text/css">
            ul,li{list-style: none;margin:0;padding:0;float:left;}
            html{height:100%}
            body{height:100%;margin:0px;padding:0px;font-family:"微软雅黑";}
            #container{height:500px;width:100%;}
            #r-result{width:100%;}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <div id="r-result">
            <input type="button"  onclick="openHeatmap();" value="显示热力图"/><input type="button"  onclick="closeHeatmap();" value="关闭热力图"/>
        </div>
    </body>
    </html>
    <script type="text/javascript">
        var map = new BMap.Map("container");          // 创建地图实例
    
        var point = new BMap.Point(113.418261, 39.921984);
        map.centerAndZoom(point, 5);             // 初始化地图，设置中心点坐标和地图级别
        map.enableScrollWheelZoom(); // 允许滚轮缩放
    
        var points =["""

    # html文件的脚部
    footer = """];
    
        if(!isSupportCanvas()){
            alert('热力图目前只支持有canvas支持的浏览器,您所使用的浏览器不能使用热力图功能~')
        }
        //详细的参数,可以查看heatmap.js的文档 https://github.com/pa7/heatmap.js/blob/master/README.md
        //参数说明如下:
        /* visible 热力图是否显示,默认为true
         * opacity 热力的透明度,1-100
         * radius 势力图的每个点的半径大小
         * gradient  {JSON} 热力图的渐变区间 . gradient如下所示
         *	{
                .2:'rgb(0, 255, 255)',
                .5:'rgb(0, 110, 255)',
                .8:'rgb(100, 0, 255)'
            }
            其中 key 表示插值的位置, 0~1.
                value 为颜色值.
         */
        heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":20});
        map.addOverlay(heatmapOverlay);
        heatmapOverlay.setDataSet({data:points,max:100});
        //是否显示热力图
        function openHeatmap(){
            heatmapOverlay.show();
        }
        function closeHeatmap(){
            heatmapOverlay.hide();
        }
        closeHeatmap();
        function setGradient(){
            /*格式如下所示:
            {
                0:'rgb(102, 255, 0)',
                .5:'rgb(255, 170, 0)',
                1:'rgb(255, 0, 0)'
            }*/
            var gradient = {};
            var colors = document.querySelectorAll("input[type='color']");
            colors = [].slice.call(colors,0);
            colors.forEach(function(ele){
                gradient[ele.getAttribute("data-key")] = ele.value;
            });
            heatmapOverlay.setOptions({"gradient":gradient});
        }
        //判断浏览区是否支持canvas
        function isSupportCanvas(){
            var elem = document.createElement('canvas');
            return !!(elem.getContext && elem.getContext('2d'));
        }
    </script>"""
    # 将经纬度和粉丝个数信息写入points列表中
    with open("music163.html", 'a') as f:
        f.write(header)
        for key in loc_counts.keys():
            # 采用构造的函数来获取经度
            lng = getlnglat(key)['result']['location']['lng']
            # 获取纬度
            lat = getlnglat(key)['result']['location']['lat']
            str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + ',"count":' + str(loc_counts[key]) + '},'
            f.write(str_temp)
        f.write(footer)
        f.close()


def main():
    locs = get_loccodes()
    loc_counts = convert_code_loc(locs)
    generate_map(loc_counts)
    print("热力图生成完成！")


if __name__ == "__main__":
    main()
