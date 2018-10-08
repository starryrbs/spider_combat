##使用selenium爬取淘宝实战
1. 确定要爬取的内容

	![](https://i.imgur.com/D6uj8wf.jpg)

	 爬取左侧的一级类型(女装/男装/内衣等等),和右侧的二级类型(秋上新/连衣裙等等)
2. 导入selenium

	1. 在这之前需要安装webdriver

		可以自行去百度安装

			from selenium import webdriver
			from selenium.webdriver.common.by import By
			from selenium.webdriver.common.keys import Keys
			from selenium.webdriver.support.wait import WebDriverWait
			from selenium.webdriver.chrome.options import Options
			from selenium.webdriver.support.ui import WebDriverWait#负责等待
			# expected_conditions 类，负责条件出发
			from selenium.webdriver.support import expected_conditions as EC
			import time
			from selenium.webdriver.common.action_chains import ActionChains
			import time

	2. 使用selenium的无头模式

			chrome_options=Options()
			chrome_options.add_argument('--enable-logging')
			chrome_options.add_argument('--disable-gpu')
			chrome_options.add_argument('--headless ')

		创建一个模拟的浏览器并设置无头模式

			browser=webdriver.Chrome()

		确定爬取的网址

			url="https://www.taobao.com/"

		发送请求

			browser.get(url)

		使用xpath抓取标签

			input_kw=browser.find_elements_by_xpath('//ul[@class="service-bd"]/li')

		这里会遇到一个问题,拿右侧的标签,如果鼠标不经过它所对应的左侧标签,页面是不会去请求后台拿取数据的,所有需要去循环触碰左侧标签,使用如下方法

			##ActionChains(browser).move_to_element(i).perform()
			
			for i in input_kw:
			    print(i)
			    li_a=i.find_elements_by_xpath('a')
			    for li in li_a:
			        print(li.get_attribute('innerHTML'))
			        data.append({"name":li.get_attribute('innerHTML')})
			    ActionChains(browser).move_to_element(i).perform()
			    time.sleep(3)

		
		拿取所有的右侧标签

			items=browser.find_elements_by_xpath('//div[@class="service-panel"]')
	
			index=0
			for item in items:
			    good=item.find_elements_by_xpath('p/a')
			    h=item.find_element_by_xpath('h5/a')
			    data[index]["href"]=h.get_attribute('href')
			    print("good",good)
			    print("good的长度",len(good))
			    item_list=[]
			    for g in good:
			        print("g",g)
			        print(g.get_attribute('innerHTML'))
			        item_list.append(g.get_attribute('innerHTML'))
			    data[index]["category"]=item_list
			    index+=1

		关闭selenium的浏览器

			browser.close()

	到这一步,我们拿到了所有商品类型,数据格式应该是这样的:

		[
		  {
		    "name": "办公",
		    "href": "https://www.taobao.com/markets/bangong/pchome",
		    "category": [
		      "WiFi放大器",
		      "无线呼叫器",
		      "格子间",
		      "电脑桌",
		      "办公椅",
		      "理线器",
		      "计算器",
		      "荧光告示贴",
		      "翻译笔",
		      "毛笔",
		      "马克笔",
		      "文件收纳",
		      "本册",
		      "书写工具",
		      "文具",
		      "画具画材",
		      "钢笔",
		      "中性笔",
		      "财会用品",
		      "碎纸机",
		      "包装设备"
		    ]
		  },
		  {
		    "name": "DIY",
		    "href": "https://www.taobao.com/markets/dingzhi/home",
		    "category": [
		      "定制T恤",
		      "文化衫",
		      "工作服",
		      "卫衣定制",
		      "LOGO设计",
		      "VI设计",
		      "海报定制",
		      "3D效果图制作",
		      "广告扇",
		      "水晶奖杯",
		      "胸牌工牌",
		      "奖杯",
		      "徽章",
		      "洗照片",
		      "照片冲印",
		      "相册/照片书",
		      "软陶人偶",
		      "手绘漫画",
		      "纸箱",
		      "搬家纸箱",
		      "胶带",
		      "标签贴纸",
		      "二维码贴纸",
		      "塑料袋",
		      "自封袋",
		      "快递袋",
		      "气泡膜",
		      "编织袋",
		      "飞机盒",
		      "泡沫箱",
		      "气柱袋",
		      "纸手提袋",
		      "打包绳带",
		      "气泡信封",
		      "缠绕膜"
		    ]
		  }]

		这只是数据的一部分


2. 爬取每个商品类型对应的所有的商品,这里只拿到5页,不贪多

	这次我们采用面向对象的思想来做:

	1. 创建一个taobaoSpider类

		将那些固定的数据写在__init__方法中,我们把数据存在mongodb里面,当然也可以存在本地

			    def __init__(self,file):
			        self.conn = MongoClient('127.0.0.1', 27017)
			        self.db = self.conn.orsp  # 连接mydb数据库，没有则自动创建
			        # 使用无头模式
			        chrome_options = Options()
			        chrome_options.add_argument('--enable-logging')
			        chrome_options.add_argument('--disable-gpu')
			        chrome_options.add_argument('--headless ')
			        # 修改头
			        # dcap = dict(DesiredCapabilities.PHANTOMJS)
			        # dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
			
			        # options=chrome_options
			        self.browser = webdriver.Chrome()
			#       类型文件
			        self.file=file

	2. 因为淘宝的商品页面也是动态刷新的,所有需要定义一个滚动屏幕的方法

		    def roll_window(self):
		        for ti in range(10):
		            self.browser.execute_script("window.scrollBy(0,600)")
		            time.sleep(0.5)

	3. 打开刚才爬取的所有类型文件,并去调用爬虫方法

		    def open_file(self):
		        with open('taobao_type.json', 'r', encoding='utf-8') as f:
		            data = json.load(f)
		            # 读取data的每一项
		            for i in data:
		                # 获得url地址
		                url = i["href"]
		                self.belong_name = i["name"]
		                for item in i["category"]:
		                    self.item=item
		                    # 获取到点击按钮
		                    try:
		                        # 使用浏览器获取url的界面
		                        self.browser.get(url)
		
		
		                        time.sleep(1)
		                        # 找到输入框
		                        input_kw = self.browser.find_element_by_xpath('//div[@class="search-combobox-input-wrap"]/input')
		                        # 每次都清空输入框
		                        input_kw.clear()
		                        # 写入要找的值
		                        input_kw.send_keys(item)
		                        # 按下回车
		                        input_kw.send_keys(Keys.ENTER)
		                    except Exception as ex:
		                        print(ex)
		                        continue
		                    # 使界面滚动条匀速下滑,使得页面全部渲染出来
		                    taobao_spider.roll_window()
		                    for num in range(5):
		                        try:
		                            # 第一次时,不需要点击下一页
		                            if num != 0:
		                                # 获取下一页按钮
		                                next_step = self.browser.find_element_by_xpath('//ul/li[@class="item next"]')
		                                next_step.click()
		                                time.sleep(1)
		                                # 滚动条匀速滚动
		                                taobao_spider.roll_window()
		                            # 获取所有商品项,其中有几个页面xpath不一样,使用 or 可以解决
		                            goods = self.browser.find_elements_by_xpath(
		                                '//div[@class="item J_MouserOnverReq  item-sku J_ItemListSKUItem"]') or self.browser.find_elements_by_xpath(
		                                '//div[@class="item J_MouserOnverReq  "]')
		                            # 遍历所有商品
		                            taobao_spider.get_all_goods(goods)
		                        except Exception as ex:
		                            print(ex)

	4. 爬虫的主体部分

		    #   获取每一个商品
		    def get_all_goods(self,goods):
		        for good in goods:
		            taobao = {}
		            good_item = good.find_element_by_xpath('.//div[@class="pic"]/a')
		            # 获取id
		            id = good_item.get_attribute('data-nid')
		            # 获取详情页的地址
		            taobao["detail_href"]=good_item.get_attribute('href')
		            # 获取价格
		            price = good_item.get_attribute('trace-price')
		            img = good.find_element_by_xpath('.//div[@class="pic"]/a/img')
		            # 获取title
		            title = img.get_attribute('alt')  # 获取alt属性
		            img_href = img.get_attribute('src')  # 获取src属性
		            shop = good.find_element_by_xpath('.//div[@class="shop"]/a/span[2]').get_attribute(
		                'innerHTML')  # 获取innerHTML,有时  元素.text  这样的形式不好用
		            address = good.find_element_by_xpath('.//div[@class="location"]').get_attribute(
		                'innerHTML')
		            sales_num = good.find_element_by_xpath('.//div[@class="deal-cnt"]').get_attribute(
		                'innerHTML')
		            taobao["belong_to"] = self.item
		            taobao["sales_num"] = sales_num
		            taobao["price"] = price
		            taobao["img_href"] = img_href
		            taobao["title"] = title
		            taobao["shop"] = shop
		            taobao["address"] = address
		            taobao["belong_name"] = self.belong_name
		            print(",", taobao)
		            # 将数据插入mongodb
		            my_set = self.db.taobao_goods.insert(taobao)


	5. 最后在main中,创建taobaoSpider类对象,开始爬虫

			if __name__ == '__main__':
			    taobao_spider=taobaoSpider('taobao_type.json')
			    taobao_spider.open_file()


	