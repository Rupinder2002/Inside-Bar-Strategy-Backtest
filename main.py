from flask import Flask,render_template, request, make_response
from flask_mysqldb import MySQL
from io import BytesIO
import pandas as pd
import numpy as np
import sqlalchemy
import decimal


#commentinggg



import data_collection
import RSI_Strategy
import SMA_Strategy1
import SMA_Strategy2
import performance
import InsideBar_Strategy
import LongBar_Strategy
import testing_sql


 
app = Flask(__name__)
 


@app.route('/',methods = ['POST', 'GET'])
def form():
    
    return render_template('index.html')


@app.route('/run_strategy', methods = ['POST', 'GET'])
def run_strategy():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        ticker = request.form['ticker']
        st_date = request.form['st_date']
        ed_date = request.form['ed_date']
        strategy = request.form['strategy']
       
        param1 = request.form['param1']
        param2 = request.form['param2']
       
        
        data = data_collection.DataScraping(ticker,st_date,ed_date)
        #return f"the data :{data}"
        
        #STRATEGY 1
        
        if strategy == '1':
            try :
                w=SMA_Strategy1.SMA(data,st_date,ed_date,ticker,strategy,param1,param2)
                return f"The winning percentage ------ {w}"
            except:
                return "no trade" 
            
            

        elif strategy == '3':
            try :
                ndata=RSI_Strategy.RSI(data)
                w=RSI_Strategy.trade(ndata,st_date,ed_date,ticker,strategy,param1,param2)
                return f"The winning percentage ------ {w}"
            except:
                return "no trade" 
            
        
        elif strategy == '4':
            try :
                w = InsideBar_Strategy.InsideBar(data,st_date,ed_date,ticker,strategy,param1,param2)
                return f"The winning percentage ------ {w}"
            except:
                return "no trade"
            
           
        elif strategy == '5':
            try:
                w =LongBar_Strategy.Longbar(data,st_date,ed_date,ticker,strategy,param1,param2)
                return f"The winning percentage ------ {w}"
            except:
                return "no trade"
                
        else:
            return" No other strategy available"
  


        
if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)     
        
        
        
      