from threading import Thread
from flask import Flask
import os

class Main:
    def __init__(self):
        Thread(target=self.flaskapp).start()

    def flaskapp(self):
        app = Flask(__name__)
        @app.route("/")
        def price():
             m=input("Enter product name:")
             f=open(os.getcwd()+"\pricescrap\pricescrap\spiders\product.txt","w")
             f.write(m)
             f.close()
             os.system("crawlerinter.py")
             return m
        app.run()

if __name__=="__main__":
   u=Main()