"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import csv
import urllib2
import simplejson as json
from flask import Flask, render_template
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def home():
    """Renders a sample page."""
    stocks = preprocess()

    return render_template("main.html",stocks=stocks)

def preprocess():
    symbols = []
    with open('symbols.csv','rb') as file:
        reader = csv.reader(file)
        for symbol in reader:
            symbols.append(symbol[0])

    limit = 10.00
    shares = 10
    results = []
         
    for s in symbols:
        response = urllib2.urlopen('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22'+s+'%22)&format=json&diagnostics=false&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=')

        result = json.loads(response.read())
        price = result['query']['results']['quote']['LastTradePriceOnly']
        if price == None:
            continue
        else:
            price = float(price)
        
        if price * shares <= limit:
            tmp = {'url': 'https://research.capitaloneinvesting.com/research/main/Stocks/Snapshot?symbol='+s,'symbol':s,'cost':price*shares}
            results.append(tmp)
             
            
            #results['symbol' == s]['cost'] = price * shares
            
        

    return results


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '31337'))
    except ValueError:
        PORT = 31337
    app.run(HOST, PORT,debug=True)
