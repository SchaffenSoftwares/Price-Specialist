import scrapy
from selenium.webdriver import Firefox
from scrapy.crawler import CrawlerProcess as cp
from time import sleep
import os

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def __init__(self):
        super().__init__()
        w=os.getcwd()
        f = open(w+"\pricescrap\pricescrap\spiders\product.txt")
        self.pn=f.read()
        f.close()
        self.k=0
        self.data=[]
        self.driver=Firefox(executable_path=w+r"\pricescrap\pricescrap\spiders\geckodriver.exe")

    def containsall(self,s, l):
        for c in l:
            if c not in s:
                return False
        return True

    def least_price(self):
        o = [[a, b] for i in self.data for a, b in i.items() if b == min(i.values())]
        u = list(set([o[i][1] for i in range(len(o))]))
        return {o[i][0]: o[i][1] for i in range(len(o)) if o[i][1] == min(u)}


    def start_requests(self):
        self.driver.get('https://www.amazon.in/')
        self.driver.find_element_by_id("twotabsearchtextbox").send_keys(self.pn)
        self.driver.find_element_by_xpath("//input[@class='nav-input']").click()
        sleep(2)
        self.urls = [self.driver.current_url]
        while True:
            try:
                self.driver.execute_script('''window.open("{}","_blank");'''.format(self.driver.find_element_by_xpath("//li[@class='a-last']/a").get_attribute("href")))
                self.urls.append(self.driver.find_element_by_xpath("//li[@class='a-last']/a").get_attribute("href"))
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                sleep(3)
            except:
                break
        self.driver.close()
        for i in self.urls:
            sleep(3)
            yield scrapy.Request(url=i,callback=self.parse,
                                 headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"})

    def parse(self, response):
        it={}
        it["pn"]=response.css(".a-color-base.a-text-normal").css("::text").extract()
        it["pp"]=response.css(".a-price-whole").css("::text").extract()
        d={i:int(j.replace(",","")) for i,j in zip(it["pn"],it["pp"]) if self.containsall(i.lower(),self.pn.lower().split())}
        self.data.append(d)
        self.k+=1
        if self.k==len(self.urls):
            yield self.least_price()

if __name__=="__main__":
    try:
        os.remove("amazon.json")
    except:
        pass
    p1=cp({'FEED_URI':"amazon.json"})
    p1.crawl(AmazonSpider)
    p1.start()