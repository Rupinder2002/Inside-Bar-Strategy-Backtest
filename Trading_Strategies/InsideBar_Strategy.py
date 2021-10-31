
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style
import datetime
import performance
plt.style.use('tableau-colorblind10')
import sqlalchemy

def InsideBar(df,strt,end,ticker,strategy,param1,param2):
    #x
    param1 = int(param1)
    param2 = int(param2)
    def SMA(df, param1, param2):
        df['sma_fast'] = df['Close'].rolling(param1).mean()
        df['sma_slow'] = df['Close'].rolling(param2).mean()
        return df
    SMA(df,param1, param2)

    def ATR(df,n):
        
        df['High-Low'] = abs(df['High'] - df['Low'])
        df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
        df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
        df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis = 1, skipna = False)
        df['ATR'] = df['TR'].rolling(n).mean()
                #df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
                #df = df.drop(['diff', 'gains', 'losses', 'average_gains', 'average_losses'], axis = 1)
        return df
    ATR(df,20)


    account_size = 10000
    slippage = 2
    size = 1
    ATR_SL = 0.5


            #df['RSI'] = RSI(df, 14)['RSI']
    df['ATR'] = ATR(df, 20)['ATR']
           

    df['Inside_bar']= np.where(((df['High'] < df['High'].shift(1)) & (df['Low'] > df['Low'].shift(1))), True, False)
            #df['average_close'] = df['Close'].rolling(5).mean()
    df['spread'] = float(slippage) / float(10000)
    df['size'] = float(size) * float(10000)
            #df = df.drop(['diff', 'gains', 'losses', 'average_gains', 'average_losses','High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)

    #return df
    t={}
    t = trade(df,strt,end,ticker,strategy,param1,param2)
    return t

def trade(df,strt,end,ticker,strategy,param1,param2):
    
    
    open_trade = {}
    trade = {}
    long_take_profit = {}
    short_take_profit = {}
    long_stop_loss = {}
    short_stop_loss = {}
    long_entry_price = {}
    short_entry_price = {}
    

    open_trade = []
    trade = {}
    long_take_profit = []
    short_take_profit = []
    long_stop_loss = []
    short_stop_loss = []
    long_entry_price = []
    short_entry_price = []
    ATR_SL = 0.5
    
    for i in range(20, len(df)):
            #Buy
            if df['Inside_bar'][i-2] == True and df['Inside_bar'][i-1] == True and df['sma_fast'][i-1] >= df['sma_slow'][i-1] and df['Close'][i] > df['Open'][i] :
                print(i, 'New Long trade at price:', round(df['Close'][i], 4), ' On day:', df.index[i])
                trade[i] = {'ID': i,
                            'date_of_trade': df.index[i],
                            'entry_price': df['Close'][i],
                            'signal': 'Buy',
                            'result': 0,
                            'Take Profit': df['Close'][i] + df['ATR'][i] * ATR_SL,
                            'Stop Loss': df['Close'][i] - df['ATR'][i] * ATR_SL}
                open_trade.append(i)
                long_take_profit.append(trade[i]['Take Profit'])
                long_stop_loss.append(trade[i]['Stop Loss'])
                long_entry_price.append(trade[i]['entry_price'])


                #sell
            if df['Inside_bar'][i-2] == True and df['Inside_bar'][i-1] == True and df['sma_fast'][i-1] <= df['sma_slow'][i-1] and df['Close'][i] < df['Open'][i] :
                print(i, 'New short trade at price:', round(df['Close'][i], 4), ' On day:', df.index[i])
                trade[i] = {'ID': i,
                            'date_of_trade': df.index[i],
                            'entry_price': df['Close'][i],
                            'signal': 'sell',
                            'result': 0,
                            'Take Profit': df['Close'][i] - df['ATR'][i] * ATR_SL,
                            'Stop Loss': df['Close'][i] + df['ATR'][i] * ATR_SL}
                open_trade.append(i)
                short_take_profit.append(trade[i]['Take Profit'])
                short_stop_loss.append(trade[i]['Stop Loss'])
                short_entry_price.append(trade[i]['entry_price'])

                
                    #Exit after time
            if len(open_trade) != 0:
                for j in open_trade:
                    if (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Buy':
                        trade[j].update({'result' : (df['Close'][i] - trade[j]['entry_price'] - df['spread'][i]) * df['size'][i]})
                        print(j, 
                             'Long exited after 12 hours:', round(df['Close'][i], 4),
                             'On day:', df.index[i],
                             'With profit:', round(trade[j]['result'], 4), '\n')
                        open_trade.remove(j)
                        long_take_profit.remove(trade[j]['Take Profit'])
                        long_stop_loss.remove(trade[j]['Stop Loss'])
                    elif (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Sell':
                        trade[j].update({'result' : (trade[j]['entry_price'] - df['Close'][i] - df['spread'][i]) * df['size'][i]})
                        print(j, 
                             'Short exited after 12 hours:', round(df['Close'][i], 4),
                             'On day:', df.index[i],
                             'With profit:', round(trade[j]['result'], 4), '\n')
                        open_trade.remove(j)
                        short_take_profit.remove(trade[j]['Take Profit'])
                        short_stop_loss.remove(trade[j]['Stop Loss'])
                        
    per = performance.performance(trade,strt,end,ticker,strategy,param1,param2)
    return per
    #return trade

