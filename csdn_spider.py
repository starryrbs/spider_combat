import time

from selenium import webdriver

telephone = "15755407860"
password = "13866015127rbs"


class SpiderCsdn:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
        option.add_argument('--enable-logging')
        option.add_argument('--disable-gpu')
        # option.add_argument('--headless ')
        self.driver = webdriver.Chrome(chrome_options=option)

    def login(self):
        print("开始登录")
        csdn_login_url = "https://passport.csdn.net/login"
        self.driver.get(csdn_login_url)
        user_login = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/div[4]/ul/li[2]/a')
        user_login.click()
        user_input = self.driver.find_element_by_xpath('//*[@id="all"]')
        password_input = self.driver.find_element_by_xpath('//*[@id="password-number"]')
        login_button = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div/div[2]/div[4]/form/div/div[6]/div/button')
        user_input.send_keys(telephone)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(3)
        my_blog_url = self.driver.find_element_by_xpath(
            '//*[@id="csdn-toolbar"]/div/div/ul/li[7]/div[2]/div[2]/div[1]/a').get_attribute('href')
        return my_blog_url

    def get_blog(self):
        my_blog_url = self.login()
        self.driver.get(my_blog_url)
        page_count = self.driver.find_element_by_xpath("//li[@data-page][last()]").get_attribute('text')
        self.view_article()
        for i in range(int(page_count)):
            self.view_article()

    def view_article(self):
        all_article = self.driver.find_elements_by_xpath(
            '//div[@class="article-item-box csdn-tracking-statistics"][position()>1]/h4/a')
        urls = []
        for article in all_article:
            print(article)

            try:
                article_url = article.get_attribute('href')
                urls.append(article_url)
                print(f"访问文章:{article_url}")
            except Exception as ex:
                print(f"出现错误{ex}")
        for url in urls:
            self.driver.get(url)
            try:
                time.sleep(1)
                article_title = self.driver.find_element_by_xpath('//h1[@class="title-article"]').text
                read_count = self.driver.find_element_by_xpath('//span[@class="read-count"]').text
                print(f"文章:{article_title},阅读数为:{read_count}")
            except Exception as ex:
                print(f"阅读文章出错{ex}")
            time.sleep(1)

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    spider = SpiderCsdn()
    spider.get_blog()
