import scrapy
from selenium.webdriver import Firefox
from scrapy.crawler import CrawlerProcess as cp
from time import sleep
import os

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'

    def __init__(self):
        super().__init__()
        w=os.getcwd()
        f = open(w+"\pricescrap\pricescrap\spiders\product.txt")
        self.pn = f.read()
        f.close()
        self.k = 0
        self.data = []
        self.driver = Firefox(executable_path=w+r"\pricescrap\pricescrap\spiders\geckodriver.exe")

    def least_price(self):
        o = [[a, b] for i in self.data for a, b in i.items() if b == min(i.values())]
        u = list(set([o[i][1] for i in range(len(o))]))
        return {o[i][0]: o[i][1] for i in range(len(o)) if o[i][1] == min(u)}

    def containsall(self,s,l):
        for c in l:
            if c not in s:
                return False
        return True


    def start_requests(self):
        self.driver.get('https://www.flipkart.com/')
        self.driver.find_element_by_xpath("//input[@title='Search for products, brands and more']").send_keys(self.pn)
        self.driver.find_element_by_xpath("//button[@class='_2AkmmA _29YdH8']").click()
        self.driver.find_element_by_xpath("//button[@class='vh79eN']").click()
        sleep(2)
        self.urls = [self.driver.current_url]
        while True:
            try:
                x = self.driver.find_element_by_xpath("//span[contains(text(),'Next')]/parent::a[@class='_3fVaIS']").get_attribute("href")
                self.driver.execute_script('''window.open("{}","_blank");'''.format(x))
                self.urls.append(x)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                sleep(7)
            except:
                break
        self.driver.close()
        for i in self.urls:
            sleep(3)
            yield scrapy.Request(url=i,callback=self.parse,
                                 headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"})

    def parse(self, response):
        it= {}
        it["pn"]=response.css("._3wU53n").css("::text").extract()
        it["pp"]=response.css("._2rQ-NK").css("::text").extract()
        d={i:int(j.replace("₹","").replace(",","")) for i,j in zip(it["pn"],it["pp"]) if self.containsall(i.lower(),self.pn.lower().split())}
        self.data.append(d)
        self.k+=1
        if self.k==len(self.urls):
            yield self.least_price()

if __name__=="__main__":
    try:
        os.remove("flipkart.json")
    except:
        pass
    p2=cp({'FEED_URI':"flipkart.json"})
    p2.crawl(FlipkartSpider)
    p2.start()