import os
from time import sleep

if __name__=="__main__":
    p=os.getcwd()
    os.system(p+r"\Crawlers\flipkart.py")
    sleep(2)
    os.system(p+r"\Crawlers\ebay.py")
    sleep(2)
    os.system(p+r"\Crawlers\paytm.py")
    sleep(2)
    os.system(p+r"\Crawlers\amazon.py")