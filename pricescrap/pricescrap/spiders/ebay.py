import scrapy
from selenium.webdriver import Firefox
from scrapy.crawler import CrawlerProcess as cp
from time import sleep
import os

class EBaySpider(scrapy.Spider):
    name = "ebay"

    def __init__(self):
        super().__init__()
        w=os.getcwd()
        f = open(w+"\pricescrap\pricescrap\spiders\product.txt")
        self.pn = f.read()
        f.close()
        self.k = 0
        self.data = []
        self.driver = Firefox(executable_path=w+r"\pricescrap\pricescrap\spiders\geckodriver.exe")

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
        self.driver.get("https://in.ebay.com/")
        self.driver.find_element_by_xpath("//input[@class='gh-tb ui-autocomplete-input']").send_keys(self.pn)
        self.driver.find_element_by_id("gh-btn").click()
        sleep(2)
        self.urls=[self.driver.current_url]
        while True:
           try:
             x=self.driver.find_element_by_xpath("//a[@class='pagination__next']").get_attribute("href")
             self.driver.execute_script('''window.open("{}","_blank");'''.format(x))
             self.urls.append(x)
             self.driver.close()
             self.driver.switch_to.window(self.driver.window_handles[0])
           except:
               break
        self.driver.close()
        for i in self.urls:
            sleep(3)
            yield scrapy.Request(url=i, callback=self.parse,
                                 headers={
                                     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"})

    def parse(self, response):
        it= {}
        it["pn"]=response.css(".s-item__title").css("::text").extract()
        it["pp"]=response.css(".s-item__price").css("::text").extract()
        d={i:float(j.replace("INR ","").replace(",","")) for i,j in zip(it["pn"],it["pp"]) if self.containsall(i.lower(),self.pn.lower().split()) and "to" not in j}
        self.data.append(d)
        self.k+=1
        if self.k==len(self.urls):
            yield self.least_price()

if __name__=="__main__":
    try:
        os.remove("ebay.json")
    except:
        pass
    p3=cp({'FEED_URI':"ebay.json"})
    p3.crawl(EBaySpider)
    p3.start()
