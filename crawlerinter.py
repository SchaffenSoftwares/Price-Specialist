import os

if __name__=="__main__":
    p=os.getcwd()
    os.system(p+r"\pricescrap\pricescrap\spiders\amazon.py")
    os.system(p+r"\pricescrap\pricescrap\spiders\flipkart.py")
    os.system(p+r"\pricescrap\pricescrap\spiders\ebay.py")
    os.system(p+r"\pricescrap\pricescrap\spiders\paytm.py")