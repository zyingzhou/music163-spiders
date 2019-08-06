# [网易云音乐爬虫](https://github.com/zyingzhou/music163-spiders "网易云音乐爬虫")
>
## 一,[获取全部歌手的id号](https://github.com/zyingzhou/wangyiyun_music/blob/master/get_artists.py "获取全部歌手的id号")
> [网易云音乐](https://music.163.com "网易云音乐")使用了内联框架,除网站的主框架外,其他内容都是嵌在子网页当中,如果直接使用 requests 库是无法爬取到我 
> 们想要的内容的,因此我们需要使用 selenium 的 switch_to_frame()方法来切换到子网页中,这时获取的网页源代码才包含我们需要的内容.详细的爬取思路大家可以参考我的这篇文章[网易云音乐评论爬虫(二):爬取全部热门歌曲及其对应的id号](http://www.zhouzying.cn/34.html "网易云音乐评论爬虫(二):爬取全部热门歌曲及其对应的id号") 
> 爬取入口是:[https://music.163.com/#/discover/artist](https://music.163.com/#/discover/artist "爬取入口") 
> 


## 二,[通过歌手id号爬取全部歌手的每一首热门歌曲的id号](https://github.com/zyingzhou/wangyiyun_music/blob/master/get_hot_songs.py "通过歌手id号爬取全部歌手的每一首热门歌曲的id号")
> 一种方法爬取思路同上。另一种方法是直接爬取嵌在iframe里面的子页面(控制面板--Sources--contentFrame--域名文件夹下可找到)。 
> [爬取子frame](get_songs.py "获取爬取子Frame代码") 
> 
>



## 三,[爬取全部歌手的每一首热门歌曲的全部评论](https://github.com/zyingzhou/wangyiyun_music/blob/master/get_comments.py "爬取全部歌手的每一首热门歌曲的全部评论") 
> 由于网易云音乐的歌曲评论是通过Ajax进行加载的,而且加载过程还对参数进行了js混淆加密,使得爬取歌曲全部评论变得困难.笔者对加密过程详细分析之后得出了它的
> 加密过程:两次 AES 加密得到 params 参数的值,RSA 加密得到 encSeckey 的值.然后使用 Python 进行相应的加密得到对应的参数, 利用得到的加密参数发起带
> data的post请求即可获得含有歌曲评论的json格式的数据.详细爬取思路分析请参考:[网易云音乐评论爬虫(三):爬取歌曲的全部评论](http://www.zhouzying.cn/58.html "网易云音乐评论爬虫(三):爬取歌曲的全部评论") 
> 

## 四，[网易云音乐歌手粉丝地域分布热力图](https://github.com/zyingzhou/music163-spiders/tree/master/HeatMap "网易云音乐歌手粉丝地域分布热力图")
> 制作网易云歌手粉丝地域分布热力图，我把它分为两个步骤：1.[获取歌手全部的粉丝信息](https://github.com/zyingzhou/music163-spiders/blob/master/HeatMap/get_fansinfo.py "获取歌手全部的粉丝信息") 2.[制作歌手粉丝地域分布的热力图](https://github.com/zyingzhou/music163-spiders/blob/master/HeatMap/generate_heatmap.py "制作歌手粉丝地域分布的热力图") 
> ### 1.[获取歌手全部的粉丝信息](https://github.com/zyingzhou/music163-spiders/blob/master/HeatMap/get_fansinfo.py "获取歌手全部的粉丝信息") 
> 在歌手的个人主页，我们可以找到粉丝数据(通过Ajax进行加载)，这些数据是进行了加密的，加密方式同歌曲评论的加密方式，加密方式的分析请参考：[网易云音乐评论爬虫(三):爬取歌曲的全部评论](https://www.zhouzying.cn/58.html "网易云音乐评论爬虫(三):爬取歌曲的全部评论")，只要分析出其中变量的变化规律即能获取到这些数据。 
> 再通过粉丝的id号，爬取粉丝个人主页中的地理位置信息。
> ### 2.[制作歌手粉丝地域分布的热力图](https://github.com/zyingzhou/music163-spiders/blob/master/HeatMap/generate_heatmap.py "制作歌手粉丝地域分布的热力图") 
> 由于上一步获取到的位置是城市编码，因此我们需要将城市编码转换为中文的位置信息，再通过[百度的API](http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding "百度地图开放平台web服务API")将位置转换为经纬度，使用百度API需要先[获取服务密钥(ak)](http://lbsyun.baidu.com/apiconsole/key/create "获取服务密钥（ak）")，最后把经纬度，同一个地方的粉丝 
> 数量按字典格式插入到热力图的模板HTML代码中去！热力图的H5模板文件格式: 

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=这里填写你的百度服务密钥（ak）"></script>
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

    var points =[
{"lat":39.92998577808024,"lng":116.39564503787867,"count":4000.57},
{"lat":39.143929903310074,"lng":117.21081309155257,"count":2300.01},
{"lat":38.048958314615454,"lng":114.52208184420766,"count":1015.77},
{"lat":37.89027705396754,"lng":112.5508635890553,"count":680.13},
{"lat":40.828318873081585,"lng":111.6603505200542,"count":520.52},
{"lat":41.808644783515746,"lng":123.43279092160505,"count":709.67},
{"lat":38.94870993830429,"lng":121.59347778143518,"count":535.17},
{"lat":43.89833760709784,"lng":125.31364242720072,"count":596.65},
{"lat":45.7732246332393,"lng":126.65771685544611,"count":526.13},
{"lat":31.24916171001514,"lng":121.48789948569473,"count":3709.03},
{"lat":32.05723550180587,"lng":118.77807440802562,"count":1845.6},
{"lat":30.259244461536102,"lng":120.2193754157201,"count":2606.63},
{"lat":29.885258965918055,"lng":121.57900597258933,"count":1270.33},
{"lat":31.86694226068694,"lng":117.28269909168304,"count":1352.59},
{"lat":26.04712549657293,"lng":119.33022110712668,"count":1679.44},
{"lat":24.489230612469232,"lng":118.10388604566381,"count":765.8},
{"lat":28.689578000141147,"lng":115.89352754583604,"count":674.6},
{"lat":36.68278472716141,"lng":117.02496706629023,"count":1164.14},
{"lat":36.10521490127382,"lng":120.38442818368189,"count":1369.14},
{"lat":34.756610064140254,"lng":113.64964384986449,"count":2778.95},
{"lat":30.58108412692075,"lng":114.31620010268132,"count":2517.44},
{"lat":28.21347823085322,"lng":112.9793527876505,"count":1266.63},
{"lat":23.12004910207623,"lng":113.30764967515182,"count":2540.85},
{"lat":22.546053546205247,"lng":114.0259736573215,"count":1756.52},
{"lat":22.80649293560261,"lng":108.29723355586638,"count":854},
{"lat":20.022071276952243,"lng":110.3308018483363,"count":551.29},
{"lat":29.54460610888615,"lng":106.53063501341296,"count":3725.95},
{"lat":30.679942845419564,"lng":104.06792346330406,"count":2641.14},
{"lat":26.62990674144093,"lng":106.7091770961758,"count":923.26},
{"lat":25.049153100453157,"lng":102.71460113878045,"count":1530.5},
{"lat":29.662557062056536,"lng":91.11189089598402,"count":337.69},
{"lat":42.98636494637781,"lng":125.15014857862096,"count":1949.5},
{"lat":36.06422552504259,"lng":103.8233054407292,"count":370.39},
{"lat":36.640738611957964,"lng":101.76792098980276,"count":316.5},
{"lat":38.50262101187604,"lng":106.2064786078384,"count":474.94},
{"lat":43.84038034721766,"lng":87.56498774111579,"count":344.71},
   ];

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
</script>
```
> 我们生成的字典数据({"lat":23.043023815368237,"lng":113.76343399075655,"count":204})只需要一个一个插入到point列表中去就行， 
> 字典格式为{"lat": 纬度, "lng": 经度, "count":这个地理位置的粉丝数量}。最后把这个HTML文件在浏览器中打开，再点击显示热力图，缩放地 
> 图便能看到歌手粉丝地域分布的热力图。以薛之谦为例，我们来看一下他的部分粉丝地域分布的热力图：![薛之谦粉丝地域分布热力图](https://github.com/zyingzhou/music163-spiders/blob/master/files/music163HeatMap.png)
