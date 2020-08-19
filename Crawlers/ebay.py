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
d.get("https://in.ebay.com/")
f = open(w+"\Database\product.txt")
pn = f.read()
f.close()
d.find_element_by_xpath("//input[@class='gh-tb ui-autocomplete-input']").send_keys(pn)
d.find_element_by_id("gh-btn").click()
sleep(2)
m=[]
while True:
    m.append({x.text:{"Price":float(y.text.replace("INR ","").replace(",","")),"Img":w.get_attribute("src"),"URL":z.get_attribute("href")} for x, y,w,z in zip(d.find_elements_by_css_selector(".s-item__title"),d.find_elements_by_css_selector(".s-item__price"),d.find_elements_by_xpath("//img[@class='s-item__image-img']"),d.find_elements_by_xpath("//a[@class='s-item__link']")) if containsall(x.text.lower(),pn.lower().split()) and "to" not in y.text})
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
    os.remove(w+"\Database\ebay.json")
except:
    pass
with open(w+"\Database\ebay.json","w") as p:
    json.dump({a:b for i in m for a,b in i.items() if b["Price"]==min([j[n]["Price"] for j in m for n in j])},p)
