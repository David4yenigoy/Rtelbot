import pyupbit 
import pandas 
import datetime 
import time
import telegram

bot = telegram.Bot(token='**')
chat_id = **

def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")


# 이용할 코인 리스트 
coinlist = pyupbit.get_tickers(fiat="KRW")

while(True):
    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute60")
        now_rsi = rsi(data, 14).iloc[-1]
        past_rsi = rsi(data, 14).iloc[-2]
        if now_rsi < 28 and now_rsi < past_rsi :
            sendMsg = str(coinlist[i]) + "< RSI > :" + str(now_rsi)
            print(coinlist[i], "현재시간: ", datetime.datetime.now(), "< RSI 60분 > :", now_rsi)
            bot.sendMessage(chat_id=chat_id, text=sendMsg)
        else :
            pass
        # print()        

       
    time.sleep(1)
