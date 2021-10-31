import pandas_datareader.data as web



#2021-05-3


def DataScraping(ticker,st_date,ed_date):
    ticker=ticker
    st_date = st_date
    ed_date = ed_date
    df1=web.DataReader(ticker, data_source='yahoo', start=st_date, end=ed_date)
    #print(df1)
    return df1
    