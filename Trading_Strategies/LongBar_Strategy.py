import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style
import performance



def Longbar(df,strt,end,ticker,strategy,param1,param2):
    
    param1 = int(param1)
    param2 = int(param2)
        
    def ATR(df, n):
        #df = df.copy()
        df['High-Low'] = abs(df['High'] - df['Low'])
        df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
        df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
        df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis = 1, skipna = False)
        df['ATR'] = df['TR'].rolling(n).mean()
        #df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
        #df = df.drop(['diff', 'gains', 'losses', 'average_gains', 'average_losses'], axis = 1)
        return df
    ATR(df,20)
    
    def average_bar_size(df):
              
        df['candle_size'] = df['High'] - df['Low']
        df['average_bar'] = df['candle_size'].rolling(20).mean()
        return df
    average_bar_size(df)
    
    def small_wick(df, wick_size):
        df = df.copy()
        df['small_wick'] = np.where((df['Close'] > df['Open'])& ((df['High'] - df['Close']) <= ((df['High'] - df['Low']) * wick_size))                                 & ((df['Open'] - df['Low']) <= ((df['High'] - df['Low']) * wick_size))                                 | (df['Close'] < df['Open'])  & ((df['High'] - df['Open']) <= ((df['High'] - df['Low']) * wick_size))                                  & ((df['Close'] - df['Low']) <= ((df['High'] - df['Low']) * wick_size)), True, False)
        return df
    
    #small_wick(df,param1)
    #wicksize 0.2
    
        
    account_size = 10000
    slippage = 2
    size = 1
    ATR_SL = 0.5
    
    df['ATR'] = ATR(df, 20)['ATR']
    df['average_bar'] = average_bar_size(df)['average_bar']
    df['small_wick'] = small_wick(df,param1)['small_wick']
    df['spread'] = float(slippage) / float(10000)
    df['size'] = float(size) * float(10000)
    df['wick_size']=param1
    df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
    
    t={}
    t = trade(df,strt,end,ticker,strategy,param1,param2)
    
    return t

#param2 average bar size

def trade(df,strt,end,ticker,strategy,param1,param2):
    #trade = {}
    param2 = int(param2)
    open_trade = {}
    trade = {}
   

    open_trade = []
    trade= {}
    
    ATR_SL = 0.5
    for i in range(len(df)):
        if (df['High'][i - 1] - df['Low'][i - 1]) >= param2 * df['average_bar'][i - 1] and df['small_wick'][i - 1] == True and df['Close'][i - 1] > df['Open'][i - 1]:
            print(i, 'New Long trade at price:', round(df['Close'][i], 4), ' On day:', df.index[i])
            trade[i] = {'ID': i,
                             'date_of_trade': df.index[i],
                             'entry_price': df['Close'][i],
                             'signal': 'Buy',
                             'result': 0,
                             'Take Profit': df['Close'][i] + df['ATR'][i] * 4 * ATR_SL,
                             'Stop Loss': df['Close'][i] - df['ATR'][i] * ATR_SL}
            open_trade.append(i)
            
        #Sell
        if (df['High'][i - 1] - df['Low'][i - 1]) >= param2 * df['average_bar'][i - 1] and df['small_wick'][i - 1] == True          and df['Close'][i - 1] < df['Open'][i - 1]:
            print(i, 'New Short trade at price:', round(df['Close'][i], 4), ' On day:', df.index[i])
            trade[i] = {'ID': i,
                             'date_of_trade': df.index[i],
                             'entry_price': df['Close'][i],
                             'signal': 'Sell',
                             'result': 0,
                             'Take Profit': df['Close'][i] + df['ATR'][i] * 4 * ATR_SL,
                             'Stop Loss': df['Close'][i] - df['ATR'][i] * ATR_SL}
            open_trade.append(i)
            
        #results
        if len(open_trade) != 0:
            for j in open_trade:
                if (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Buy':
                    trade[j].update({'result' : (df['Close'][i] - trade[j]['entry_price'] - df['spread'][i]) * df['size'][i]})
                    print(j,
                         'Long exited after 12 hours:', round(df['Close'][i], 4),
                         'On day:', df.index[i],
                         'With profit:', round(trade[j]['result'], 4), '\n')
                    open_trade.remove(j)
                    #long_take_profit.remove(trade[j]['Take Profit'])
                    #long_stop_loss.remove(trade[j]['Stop Loss'])
                elif (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Sell':
                    trade[j].update({'result' : (trade[j]['entry_price'] - df['Close'][i] - df['spread'][i]) * df['size'][i]})
                    print(j,
                         'Short exited after 12 hours:', round(df['Close'][i], 4),
                         'On day:', df.index[i],
                         'With profit:', round(trade[j]['result'], 4), '\n')
                    open_trade.remove(j)
                    #short_take_profit.remove(trade[j]['Take Profit'])
                    #short_stop_loss.remove(trade[j]['Stop Loss'])
    
    #test = testing_sql.try_sql(t,ticker,strategy)
    
    per = performance.performance(trade,strt,end,ticker,strategy,param1,param2)
    return per
    

