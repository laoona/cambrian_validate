下面说明的过程都需要在linux或类unix环境下操作，暂时不提供Windows版本；python版本建议使用2.7.10及以上版本
1 安装依赖的python包
> pip install -r requirements.txt

requirements.txt 中有完整的依赖包列表，如果安装报错请手动解决

2 执行jsonld数据验证工具
示例：(默认python命令可以自动找到)
> python tool.py 0 "https://www.baidu.com"

Usage: python validator.py is_mip url
is_mip:  是否为mip页面， 1 mip 0 not mip
url: url address