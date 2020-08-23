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
d.get('https://www.amazon.in/')
f = open(w+"\Database\product.txt")
pn = f.read()
f.close()
d.find_element_by_id("twotabsearchtextbox").send_keys(pn)
sleep(2)
d.find_element_by_xpath("//input[@class='nav-input']").click()
sleep(2)
m=[]
while True:
    m.append({x.text:{"Price":int(y.text.replace(",","")),"Img":w.get_attribute("src"),"URL":z.get_attribute("href")} for x, y,w,z in zip(d.find_elements_by_css_selector(".a-color-base.a-text-normal"),d.find_elements_by_css_selector(".a-price-whole"),d.find_elements_by_xpath("//img[@class='s-image']"),d.find_elements_by_xpath("//a[@class='a-link-normal a-text-normal']")) if containsall(x.text.lower(),pn.lower().split())})
    try:
        d.execute_script('''window.open("{}","_blank");'''.format(d.find_element_by_xpath("//li[@class='a-last']/a").get_attribute("href")))
        sleep(3)
        d.close()
        d.switch_to.window(d.window_handles[0])
        sleep(3)
    except:
        break
d.close()
try:
    os.remove(w+r"\Database\amazon.json")
except:
    pass
with open(w+r"\Database\amazon.json","w") as p:
    json.dump({a:b for i in m for a,b in i.items() if b["Price"]==min([j[n]["Price"] for j in m for n in j])},p)
