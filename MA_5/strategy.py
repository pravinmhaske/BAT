# -*- coding: utf-8 -*-


# this is tbc as sl is hitting once the candle close and candle 
# can relayy close down of our trade open price so we need to constantly check the price for every m/s to close the trade
# NOTE- write the candle closing logic and finish this assignment

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta, TH

from app_kite_trade import *
import app_token


token="enctoken "+app_token.TKN
kite = KiteApp(enctoken=token)


instrument_token="738561"

# from_date=datetime.now()-relativedelta(days=60)
# to_date=datetime.now()

from_date="2016-10-01"
to_date="2016-10-17"
print(from_date)
print(to_date)
interval="5minute"

 



def strategy(records):
    total_closing_price=0
    record_count=0
    order_placed=False
    last_order_placed=None
    last_order_price=0
    profit=0
    moving_average=0;
    
    for record in records:
        record_count+=1
        total_closing_price+=record["close"]
        
        # moving average is calculated for every 5 ticks (records)
        if record_count>=5:
            moving_average=total_closing_price/5
            
            # if moving average is greater than 5 tick place buy order
            if record["close"]>moving_average:
                if last_order_placed=="SELL" or last_order_placed is None:
                    
                    # if last order is placed then exit from it first
                    if last_order_placed=="SELL":
                        print("Exit SELL Order")
                        
                        # calculate profitd
                        profit +=last_order_price-record["close"]
                        last_order_price=record["close"]
                        
                    # Fresh buy order
                    print("place new BUY order")
                    last_order_placed="BUY"
            # if mv is less than closing price  place a sell order
            elif record["close"]<moving_average:
                # check if last order placed is but then exit else place new order
                if last_order_placed=="BUY":
                    print("exit BUY Order")
                    
                #calculate profit
                profit+=record["close"]-last_order_price
                last_order_price=record["close"]
                
                # place new sell order
                print("Place new SELL order")
                last_order_placed="SELL"
            
            total_closing_price-=records[record_count-5]["close"]
    
    print("GROSS PROFIT   => ",profit)
    # should have been as per webinar => 1099
    #plaace the last order
    
    
    
def start():
    records=kite.historical_data(instrument_token, from_date, to_date, interval) 
    strategy(records)
    
start()
            
                
        