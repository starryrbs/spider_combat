# Author:raobaoshi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # 负责等待
# expected_conditions 类，负责条件出发
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
from pymongo import MongoClient

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
class taobaoSpider():
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
    #     滚动屏幕
    def roll_window(self):
        for ti in range(10):
            self.browser.execute_script("window.scrollBy(0,600)")
            time.sleep(0.5)
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

    # 打开文件开始爬虫
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


        self.browser.close()
if __name__ == '__main__':
    taobao_spider=taobaoSpider('taobao_type.json')
    taobao_spider.open_file()
'''
[
    
{
belong_to:"秋上新",
id:"da",
sales_num:""
price:"",
img_href:"",
title:"",
shop:"",
address:""
}
    ]
    
    }

]

'''
