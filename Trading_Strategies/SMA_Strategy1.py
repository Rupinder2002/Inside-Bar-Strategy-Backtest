
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style
import datetime
plt.style.use('tableau-colorblind10')
import sqlalchemy
import performance


def SMA(df,strt,end,ticker,strategy,param1,param2):
    
    param1 = int(param1)
    param2 = int(param2)
    SMA_lower = df['Adj Close'].rolling(window = param1).mean()
    SMA_upper = df['Adj Close'].rolling(window = param2).mean()
    df['SMA_Lower'] = df['Adj Close'].rolling(window = param1).mean()
    df['SMA_Upper'] = df['Adj Close'].rolling(window = param2).mean()
    crossover = ((SMA_lower <= SMA_upper) & (SMA_lower.shift(1) > SMA_upper.shift(1)) |
                 (SMA_lower >= SMA_upper) & (SMA_lower.shift(1) < SMA_upper.shift(1)))
    crossover_value = df.loc[crossover, 'SMA_Lower']
    
    
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
    account_size = 10000
    slippage = 2
    size = 1
    ATR_SL = 0.5
    df['ATR'] = ATR(df, 20)['ATR']
    df['spread'] = float(slippage) / float(10000)
    df['size'] = float(size) * float(10000)
    df = df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis = 1)
    
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
    trade= {}
    long_take_profit = []
    short_take_profit = []
    long_stop_loss = []
    short_stop_loss = []
    long_entry_price = []
    short_entry_price = []
    ATR_SL = 0.5
    
    for i in range(20, len(df)):
            #Buy
            if df['SMA_Lower'][i-1] < df['SMA_Upper'][i-1] and df['SMA_Lower'][i] >= df['SMA_Upper'][i] :
                print(i, 'New Long trade at price:', round(df['Adj Close'][i], 4), ' On day:', df.index[i])
                trade[i] = {'ID': i,
                            'date_of_trade': df.index[i],
                            'entry_price': df['Adj Close'][i],
                            'signal': 'Buy',
                            'result': 0,
                            'Take Profit': df['Adj Close'][i] + df['ATR'][i] * ATR_SL,
                            'Stop Loss': df['Adj Close'][i] - df['ATR'][i] * ATR_SL}
                open_trade.append(i)
                long_take_profit.append(trade[i]['Take Profit'])
                long_stop_loss.append(trade[i]['Stop Loss'])
                long_entry_price.append(trade[i]['entry_price'])

    for i in range(20, len(df)):
            #sell
            if df['SMA_Lower'][i-1] > df['SMA_Upper'][i-1] and df['SMA_Lower'][i] <= df['SMA_Upper'][i] :
                print(i, 'New short trade at price:', round(df['Adj Close'][i], 4), ' On day:', df.index[i])
                trade[i] = {'ID': i,
                            'date_of_trade': df.index[i],
                            'entry_price': df['Adj Close'][i],
                            'signal': 'sell',
                            'result': 0,
                            'Take Profit': df['Adj Close'][i] - df['ATR'][i] * ATR_SL,
                            'Stop Loss': df['Adj Close'][i] + df['ATR'][i] * ATR_SL}
                open_trade.append(i)
                short_take_profit.append(trade[i]['Take Profit'])
                short_stop_loss.append(trade[i]['Stop Loss'])
                short_entry_price.append(trade[i]['entry_price'])
    if len(open_trade) != 0:
                for j in open_trade:
                    if (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Buy':
                        trade[j].update({'result' : (df['Close'][i] - trade[j]['entry_price'] - df['spread'][i]) * df['size'][i]})
                        print(j,
                             'Long exited after 12 hours:', round(df['Close'][i], 4),
                             'On day:', df.index[i],
                             'With profit:', round(trade[j]['result'], 4), '\n')
                        open_trade.remove(j)
                        #long_take_profit.remove(trade[j]['TP'])
                        #long_stop_loss[pair].remove(trade[pair][j]['SL'])
                    elif (i - trade[j]['ID']) >= 12 and trade[j].get('result', {}) == 0 and trade[j].get('signal', {}) == 'Sell':
                        trade[j].update({'result' : (trade[j]['entry_price'] - df['Close'][i] - df['spread'][i]) * df['size'][i]})
                        print(j,
                             'Short exited after 12 hours:', round(df['Close'][i], 4),
                             'On day:', df.index[i],
                             'With profit:', round(trade[j]['result'], 4), '\n')
                        open_trade.remove(j)
                        
    per = performance.performance(trade,strt,end,ticker,strategy,param1,param2)
    return per