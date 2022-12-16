# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta, TH

from app_kite_trade import *
import app_token


token="enctoken "+app_token.TKN
kite = KiteApp(enctoken=token)


instrument_token="738561"

# from_date=datetime.now()-relativedelta(days=7)
from_date="2022-12-11"
to_date=datetime.now()

print(from_date)
print(to_date)
interval="15minute"

def strategy(records):
    Buy=False
    SELL= False
    buyorder=0
    stoploss=0
    stiolossvalue=0
    stoplosshit=0
    record_count=0;
    white_soldier_count=0;
    last_order_placed=None;
    last_order_price=0
    deltaSL=0;
    profit=0
    
    length = len(records)
    
    for i in range(length):
        print(records[i])
        if i>=3:
            
            if records[i]["close"]-records[i-1]["close"]>0 and records[i-1]["close"]-records[i-2]["close"]>0:
                
               
                # check if buy order is placed
                # if last_order_placed is None:
                if last_order_placed is None or last_order_placed =="SELL":
                    print("Placed a BUY Order")
                    last_order_placed="BUY"
                    last_order_price=records[i]["close"]
                    stoploss=records[i]["open"]
                    deltaSL=records[i]["close"]-records[i]["open"]
                    white_soldier_count+=1;
                    print("*****************************************************************")
                    print("TOTAL BUY = ",white_soldier_count)
                    white_soldier_count
                    print("BUY condition  at closing price =>" ,records[i]["close"])
                    print("BUY =>" ,white_soldier_count)
                    print("last_order_placed =>" ,last_order_placed)
                    print("*****************************************************************")
                # Stop loss hit condition 
                if (records[i]["close"]<stoploss and last_order_placed=="BUY"):
                   last_order_placed="SELL"
                   profit=profit-deltaSL;
                   print("*****************************************************************")
                   print("STOP loss hit at =>" ,records[i]["close"])
                   print("SL =>" ,deltaSL)
                   print("Profit =>" ,profit)
                   print("CLosing the trade as SL Hit =>" ,last_order_placed)
                   print("*****************************************************************")
                    
                 #if target hit 2 times of stoploss then  
                if (records[i]["close"]>=(last_order_price+deltaSL*2) and last_order_placed=="BUY"):
                    last_order_placed="SELL"
                    profit+=(records[i]["close"]-last_order_price)
                    print("*****************************************************************")
                    print("profit target hit at =>" ,records[i]["close"])
                    print("SL =>" ,deltaSL)
                    print("Profit =>" ,profit)
                    print("CLosing the trade as target hit =>" ,last_order_placed)
                    print("*****************************************************************")
               
            
            
            
       # print("****")
       # print(records[i])
       # print(records[i+1])
       
       
    
    
    # for record in records:
    #     record_count=record_count+1;
        
    #     if record_count>3
    #     print("****")
    #     print(record)
        
    
    print("GROSS PROFIT   => ",profit)
    # should have been as per webinar => 1099
    #plaace the last order
    
    # place_order(last_order_placed)



def start():
    records=kite.historical_data(instrument_token, from_date, to_date, interval) 
    strategy(records)
    
    
start()

