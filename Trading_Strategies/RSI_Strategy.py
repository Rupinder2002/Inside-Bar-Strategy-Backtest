


import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style
import datetime
plt.style.use('tableau-colorblind10')
import sqlalchemy
import performance








def RSI(df):
      
    def RSI(df, n):
           

        df['diff'] = df['Close'].diff(1).dropna()
        df['gains'] = np.where(df['diff'] > 0, df['diff'], np.nan)
        df['losses'] = np.where(df['diff'] <= 0, df['diff'], np.nan)
        df['average_gains'] = df['gains'].rolling(n, min_periods = 1).mean()
        df['average_losses'] = df['losses'].rolling(n, min_periods = 1).mean()
        rs = abs(df['average_gains'] / df['average_losses'])
        df['RSI'] = 100 - (100 / (1 + rs))
        #df = df.drop(['diff', 'gains', 'losses', 'average_gains', 'average_losses'], axis = 1)
        return df
    RSI(df,14)
    def ATR(df, n):
        #df = df.copy()
        df['High-Low'] = abs(df['High'] - df['Low'])
        df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
        df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
        df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis = 1, skipna = False)
        df['ATR'] = df['TR'].rolling(n).mean()
        df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
        df = df.drop(['diff', 'gains', 'losses', 'average_gains', 'average_losses'], axis = 1)
        return df
    ATR(df,20)
    

    
        
    account_size = 10000
    slippage = 2
    size = 1
    ATR_SL = 0.5


    df['RSI'] = RSI(df, 14)['RSI']
    df['ATR'] = ATR(df, 20)['ATR']
    
    df['average_close'] = df['Close'].rolling(5).mean()
    df['spread'] = float(slippage) / float(10000)
    df['size'] = float(size) * float(10000)
    df = df.drop(['diff', 'gains', 'losses', 'average_gains', 'average_losses','High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
    
    
    return df

def trade(df2,strt,end,ticker,strategy,param1,param2):
    
    param1 = int(param1)
    param2 = int(param2)
    
    
    open_trade = {}
    trade = {}
    long_take_profit = {}
    short_take_profit = {}
    long_stop_loss = {}
    short_stop_loss = {}
    long_entry_price = {}
    short_entry_price = {}
    ATR_SL = 0.5

    open_trade = []
    trade = {}
    long_take_profit = []
    short_take_profit = []
    long_stop_loss = []
    short_stop_loss = []
    long_entry_price = []
    short_entry_price = []

    for i in range(50, len(df2)):

                #Buy
        if df2['RSI'][i-1] < param1 and df2['Close'][i - 1] < df2['average_close'][i - 1] and df2['Close'][i] >= df2['average_close'][i]:
            print(i, 'New Long trade at price:', round(df2['Close'][i], 4), ' On day:', df2.index[i])
            trade[i] = {'ID': i,
                        'date_of_trade': df2.index[i],
                        'entry_price': df2['Close'][i],
                        'signal': 'Buy',
                        'result': 0,
                        'Take Profit': df2['Close'][i] + df2['ATR'][i] * ATR_SL,
                        'Stop Loss': df2['Close'][i] - df2['ATR'][i] * ATR_SL}
            open_trade.append(i)
            long_take_profit.append(trade[i]['Take Profit'])
            long_stop_loss.append(trade[i]['Stop Loss'])
            long_entry_price.append(trade[i]['entry_price'])

                 #Sell
        if df2['RSI'][i-1] > param2 and df2['Close'][i - 1] > df2['average_close'][i - 1] and df2['Close'][i] <= df2['average_close'][i]:
            print(i, 'New Short trade at price:', round(df2['Close'][i], 4), ' On day:', df2.index[i])
            trade[i] = {'ID': i,
                        'date_of_trade': df2.index[i],
                        'entry_price': df2['Close'][i],
                        'signal': 'Sell',
                        'result': 0,
                        'Take Profit': df2['Close'][i] - df2['ATR'][i] * ATR_SL,
                        'Stop Loss': df2['Close'][i] + df2['ATR'][i] * ATR_SL}
            open_trade.append(i)
            short_take_profit.append(trade[i]['Take Profit'])
            short_stop_loss.append(trade[i]['Stop Loss'])
            short_entry_price.append(trade[i]['entry_price'])
            
        if len(open_trade) != 0:
            for j in open_trade:
                if (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Buy':
                    trade[j].update({'result' : (df2['Close'][i] - trade[j]['entry_price'] - df2['spread'][i]) * df2['size'][i]})
                    print(j, 
                          'Long exited after 12 hours:', round(df2['Close'][i], 4),
                          'On day:', df2.index[i],
                          'With profit:', round(trade[j]['result'], 4), '\n')
                    open_trade.remove(j)
                    #long_take_profit.remove(trade[j]['Take Profit'])
                    #long_stop_loss.remove(trade[j]['Stop Loss'])
                elif (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Sell':
                    trade[j].update({'result' : (trade[j]['entry_price'] - df2['Close'][i] - df2['spread'][i]) * df2['size'][i]})
                    print(j, 
                          'Short exited after 12 hours:', round(df2['Close'][i], 4),
                          'On day:', df2.index[i],
                          'With profit:', round(trade[j]['result'], 4), '\n')
                    open_trade.remove(j)
                    #short_take_profit.remove(trade[j]['Take Profit'])
                    #short_stop_loss.remove(trade[j]['Stop Loss'])
                    
    #trade=pd.DataFrame(trade)
    #trade=trade.T               
    per=performance.performance(trade,strt,end,ticker,strategy,param1,param2) 
    return per               
    #return trade
    
           
    





