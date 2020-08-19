from selenium.webdriver import Firefox
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
d.get('https://www.flipkart.com/')
f = open(w+"\Database\product.txt")
pn = f.read()
f.close()
d.find_element_by_xpath("//input[@title='Search for products, brands and more']").send_keys(pn)
d.find_element_by_xpath("//button[@class='_2AkmmA _29YdH8']").click()
d.find_element_by_xpath("//button[@class='vh79eN']").click()
sleep(2)
m=[]
while True:
    m.append({x.text:{"Price":int(y.text.replace("₹","").replace(",","")),"Img":w.get_attribute("src"),"URL":z.get_attribute("href")} for x, y,w,z in zip(d.find_elements_by_css_selector("._3wU53n"),d.find_elements_by_css_selector("._2rQ-NK"),d.find_elements_by_xpath("//div[@class='_3BTv9X']/img"),d.find_elements_by_xpath("//a[@class='_31qSD5']")) if containsall(x.text.lower(),pn.lower().split())})
    try:
        d.execute_script('''window.open("{}","_blank");'''.format(d.find_element_by_xpath("//span[contains(text(),'Next')]/parent::a[@class='_3fVaIS']").get_attribute("href")))
        sleep(3)
        d.close()
        d.switch_to.window(d.window_handles[0])
        sleep(3)
    except:
        break
d.close()
try:
    os.remove(w+r"\Database\flipkart.json")
except:
    pass
with open(w+r"\Database\flipkart.json","w") as p:
    json.dump({a:b for i in m for a,b in i.items() if b["Price"]==min([j[n]["Price"] for j in m for n in j])},p)
