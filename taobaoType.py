# Author:raobaoshi
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
url="https://www.taobao.com/"
# 使用无头模式
chrome_options=Options()
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless ')
# options=chrome_options
browser=webdriver.Chrome()
browser.get(url)
input_kw=browser.find_elements_by_xpath('//ul[@class="service-bd"]/li')
print(input_kw)
data=[]
'''
[
    {
        name:"男装"
        category:[]
    }   
]
'''
import time
print(len(input_kw))
for i in input_kw:
    print(i)
    li_a=i.find_elements_by_xpath('a')
    for li in li_a:
        print(li.get_attribute('innerHTML'))
        data.append({"name":li.get_attribute('innerHTML')})
    ActionChains(browser).move_to_element(i).perform()
    time.sleep(3)
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

print("----------")
print(data)
browser.close()
'''
Actions action = new Actions(driver);  
 action.clickAndHold();// 鼠标悬停在当前位置，既点击并且不释放  action.clickAndHold(onElement);// 鼠标悬停在 onElement 元素的位置 
action.clickAndHold(onElement) 这个方法实际上是执行了两个动作，首先是鼠标移动到元素 onElement，然后再 clickAndHold, 所以这个方法也可以写成 action.moveToElement(onElement).clickAndHold()。 
'''
# browser.implicitly_wait(2)
# # js="var q=document.documentElement.scrollTop=5000"
# # browser.execute_script(js)
# # time.sleep(5)
# # browser.implicitly_wait(2)
#
# pic_list=browser.find_elements_by_class_name('pic')
# print(pic_list)
# j=0
# window_1 = browser.current_window_handle
# for i in pic_list:
#     i.click()
#     # 获得打开的所有的窗口句柄
#     windows = browser.window_handles
#     # 切换到最新的窗口
#     for current_window in windows:
#         if current_window != window_1:
#             browser.switch_to.window(current_window)
#     # //div[@class="tb-booth"]网3
#     time.sleep(8)
#     # sufei - dialog - close
#     print("开始获取关闭按钮")
#     close_window=browser.find_element_by_id('sufei-dialog-close')
#     close_window.click()
#     time.sleep(5)
#     with open('task/nike-{}.html'.format(j),'w',encoding='utf-8') as f:
#         f.write(browser.page_source)
#         print(j)
#         f.close()
#         print(browser.page_source)
#     # /a//span[last()]/img[@alt]
#     # img=browser.find_element_by_xpath('//div[@class="tb-booth"]//span[last()]')
#     # print(img)
#     # with open('nike{}.html'.format(j),'w+',encoding='utf-8') as f:
#     #     f.write(browser.page_source)
#     j+=1
#     browser.switch_to.window(window_1)
#
#
#
# # with open('2-taobao_nike.html','w+',encoding='utf-8') as f:
# #     f.write(browser.page_source)
# browser.quit()