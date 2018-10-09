# [网易云音乐爬虫](https://github.com/zyingzhou/music163-spiders "网易云音乐爬虫")
>
## 一,[获取全部歌手的id号](https://github.com/zyingzhou/wangyiyun_music/blob/master/get_artists.py "获取全部歌手的id号")
> [网易云音乐](https://music.163.com "网易云音乐")使用了内联框架,除网站的主框架外,其他内容都是嵌在子网页当中,如果直接使用 requests 库是无法爬取到我 
> 们想要的内容的,因此我们需要使用 selenium 的 switch_to_frame()方法来切换到子网页中,这时获取的网页源代码才包含我们需要的内容.详细的爬取思路大家可以参考我的这篇文章[网易云音乐评论爬虫(二):爬取全部热门歌曲及其对应的id号](http://www.zhouzying.cn/34.html "网易云音乐评论爬虫(二):爬取全部热门歌曲及其对应的id号") 
> 爬取入口是:[https://music.163.com/#/discover/artist](https://music.163.com/#/discover/artist "爬取入口") 
> 


## 二,[通过歌手id号爬取全部歌手的每一首热门歌曲的id号](https://github.com/zyingzhou/wangyiyun_music/blob/master/get_hot_songs.py "通过歌手id号爬取全部歌手的每一首热门歌曲的id号")
> 爬取思路同上,这里就不在赘述! 
>



## 三,[爬取全部歌手的每一首热门歌曲的全部评论](https://github.com/zyingzhou/wangyiyun_music/blob/master/get_comments.py "爬取全部歌手的每一首热门歌曲的全部评论") 
> 由于网易云音乐的歌曲评论是通过Ajax进行加载的,而且加载过程还对参数进行了js混淆加密,使得爬取歌曲全部评论变得困难.笔者对加密过程详细分析之后得出了它的
> 加密过程:两次 AES 加密得到 params 参数的值,RSA 加密得到 encSeckey 的值.然后使用 Python 进行相应的加密得到对应的参数, 利用得到的加密参数发起带
> data的post请求即可获得含有歌曲评论的json格式的数据.详细爬取思路分析请参考:[网易云音乐评论爬虫(三):爬取歌曲的全部评论](http://www.zhouzying.cn/58.html "网易云音乐评论爬虫(三):爬取歌曲的全部评论") 
> 
