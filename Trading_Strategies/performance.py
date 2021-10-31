import pandas as pd
import sqlalchemy
import csv
from datetime import datetime

def performance(trade,strt,end,ticker,strategy,param1,param2):
    profits = []
    losses = []
    be = []
    account_size = 10000
    trade=trade
    p =[]
    
    start_d = strt
    end_d = end
    ticker = ticker
    strategy = strategy
    param1 = param1
    param2 = param2
    
    results = {}
    results = pd.DataFrame(trade)
    results = results.drop(['signal', 'ID', 'Take Profit', 'Stop Loss'], axis = 0)
    results = results.T
    results.set_index('date_of_trade', inplace = True)
    results['cum_res'] = results['result'].cumsum() + account_size

    for t in trade:
        profits.append(trade[t]['result']) if trade[t]['result'] > 0.1 else '' 
        losses.append(trade[t]['result']) if trade[t]['result'] < -0.1 else ''
        be.append(trade[t]['result']) if -0.1 <= trade[t]['result'] <= 0.1 else ''
    
    roi = round(results['cum_res'][-1]) - account_size
    len_profit = len(profits)
    len_loss =len(losses)
    len_b = len(be)
    len_trade = len_profit + len_loss + len_b
    w_percentage = ((round(len(profits) / (len(profits) + len(losses) + len(be)) * 100, 2))if len(profits) > 0 else 0)
    
    
    currentdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #t['createdAt'] = currentdate
    
    p.append(ticker)
    p.append(strategy)
    p.append(param1)
    p.append(param2)
    p.append(start_d)
    p.append(end_d)
    p.append(len_trade)
    p.append(len_profit)
    p.append(len_loss)
    p.append(len_b)
    p.append(w_percentage)
    p.append(roi)
    p.append(currentdate)
   
    p = pd.DataFrame(p)
    p = p.T
    
    p = p.reset_index()
    
    p.columns = ['id','ticker', 'strategy_id','param_1','param_2','start_date','end_date', 'no_of_trade', 'no_of_profits', 'no_of_losses', 'no_of_breakevens', 'winning_percentage', 'roi' ,'created_at']
   
    
    engine = sqlalchemy.create_engine('mysql+pymysql://finuser:Stablehacks123@35.193.164.234:3306/finance')
    p.to_sql(
            name= "performance",
            con=engine,
            index=False,
            if_exists='append')
          
          
          

    
    
  
   #len(trade),len(profits),len(losses),len(be),
    
    
    #return p  
    return ((round(len(profits) / (len(profits) + len(losses) + len(be)) * 100, 2))if len(profits) > 0 else 0)
    