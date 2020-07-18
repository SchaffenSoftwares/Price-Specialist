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
d=Firefox(executable_path=w+r"\pricescrap\pricescrap\spiders\geckodriver.exe")
d.get("https://paytmmall.com/")
f = open(w+"\pricescrap\pricescrap\spiders\product.txt")
pn = f.read()
f.close()
d.find_element_by_xpath("//input[@id='searchInput']").send_keys(pn)
sleep(5)
d.find_element_by_xpath("//input[@id='searchInput']").send_keys(Keys.RETURN)
sleep(10)
m=[]
while True:
    m.append({x.text: int(y.text.replace(",","")) for x, y in zip(d.find_elements_by_xpath("//div[@class='UGUy']"),d.find_elements_by_xpath("//div[@class='_1kMS']/span")) if containsall(x.text.lower(),pn.lower().split())})
    try:
        d.execute_script('''window.open("{}","_blank");'''.format(d.find_element_by_xpath("//li[@class='_2TzX']/a").get_attribute("href")))
        sleep(10)
        d.close()
        d.switch_to.window(d.window_handles[0])
        sleep(5)
    except:
        break
d.close()
o=[[a,b] for i in m for a,b in i.items() if b==min(i.values())]
u=list(set([o[i][1] for i in range(len(o))]))
p={o[i][0]:o[i][1] for i in range(len(o)) if o[i][1]==min(u)}
try:
    os.remove("paytm.json")
except:
    pass
with open("paytm.json","w") as a:
    json.dump(p,a)