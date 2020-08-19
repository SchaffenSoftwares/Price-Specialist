from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import os

def containsall(s, l):
    for c in l:
        if c not in s:
            return False
    return True

w=os.getcwd()
d=Firefox(executable_path=w+r"\geckodriver.exe")
d.get("https://paytmmall.com/")
f = open(w+"\Database\product.txt")
pn = f.read()
f.close()
d.find_element_by_xpath("//input[@id='searchInput']").send_keys(pn)
sleep(5)
d.find_element_by_xpath("//input[@id='searchInput']").send_keys(Keys.RETURN)
sleep(10)
m=[]
while True:
    m.append({x.text:{"Price":int(y.text.replace(",","")),"Img":w.get_attribute("src"),"URL":z.get_attribute("href")} for x, y,w,z in zip(d.find_elements_by_xpath("//div[@class='UGUy']"),d.find_elements_by_xpath("//div[@class='_1kMS']/span"),d.find_elements_by_xpath("//div[@class='_3nWP']/img"),d.find_elements_by_xpath("//a[@class='_8vVO']")) if containsall(x.text.lower(),pn.lower().split())})
    try:
        d.execute_script('''window.open("{}","_blank");'''.format(d.find_element_by_xpath("//li[@class='_2TzX']/a").get_attribute("href")))
        sleep(10)
        d.close()
        d.switch_to.window(d.window_handles[0])
        sleep(5)
    except:
        break
d.close()
try:
    os.remove(w+"\Database\paytm.json")
except:
    pass
with open(w+"\Database\paytm.json","w") as p:
    json.dump({a:b for i in m for a,b in i.items() if b["Price"]==min([j[n]["Price"] for j in m for n in j])},p)
