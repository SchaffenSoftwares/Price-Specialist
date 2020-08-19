from threading import Thread
from flask import Flask,jsonify,request
import os
import json

class Main:
    def __init__(self):
        self.m=None
        Thread(target=self.flaskapp).start()

    def flaskapp(self):
        app = Flask(__name__)
        @app.route("/cred",methods=["POST"])
        def cr():
            pn=request.form["pn"]
            f = open(os.getcwd() + "\Database\product.txt", "w")
            f.write(pn)
            f.close()
            os.system("crawlerinter.py")
            self.m = {next(iter(i)): i[next(iter(i))] for i in [json.load(open(os.getcwd() + r"\Database\{}".format(j), "r")) for j in ["ebay.json", "flipkart.json", "paytm.json", "amazon.json"]]}
            
        @app.route("/")
        def ret():
            if self.m!=None:
              return jsonify({a:b for a,b in self.m.items() if b["Price"]==min([m[n]["Price"] for n in self.m])})
            
        app.run()

if __name__=="__main__":
   u=Main()
