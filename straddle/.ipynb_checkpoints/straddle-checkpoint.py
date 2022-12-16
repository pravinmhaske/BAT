# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta, TH,TU
from app_kite_trade import *
import app_token
import constants

token="enctoken "+app_token.TKN
kite = KiteApp(enctoken=token)

# inputs start
SELL_LOTS=constants.SELL_LOTS
INSTRUMENT_TYPE=constants.INSTRUMENT_TYPE
INSTRUMENT_NAME=constants.INSTRUMENT_NAME
LOT_SIZE=constants.LOT_SIZE
# inputs ends

# variable for straddle starts
straddle_ce_symbol=""
straddle_pe_symbol=""
instrumentsList = None
# variable for straddle ends

def getCMP(symbol):
    try :
        quote=kite.quote(symbol)
        if quote:
             return quote[symbol]['last_price']
        else :
            return 0;
    except :  print("EError while getting quote for symbol")

def get_symbols(expiry, name, strike, ins_type):
    global instrumentsList
    try :
        if instrumentsList is None:
            instrumentsList = kite.instruments('NFO')
    
        lst_b = [num for num in instrumentsList if num['expiry'] == expiry and num['strike'] == strike
                 and num['instrument_type'] == ins_type and num['name'] == name]
        return lst_b[0]['tradingsymbol']
    except :  print("ERROR while getting symbol")


# # function to place the orders
# def place_order(trans_type):
#     try:
#         order_CE=kite.place_order(variety=kite.VARIETY_AMO,
#                       exchange=kite.EXCHANGE_NFO,
#                       tradingsymbol=straddle_ce_symbol,
#                       transaction_type=trans_type,
#                       quantity=LOT_SIZE*SELL_LOTS,
#                       product=kite.PRODUCT_NRML,
#                       order_type=kite.ORDER_TYPE_LIMIT,
#                       price=97,
#                       validity=None,
#                       disclosed_quantity=None,
#                       trigger_price=None,
#                       squareoff=None,
#                       stoploss=None,
#                       trailing_stoploss=None
#                       )
#         logging.info('Order placed successfully, orderId = %s', orderId)
#         print(order_CE)
#     except :  print("ERROR - Placing Call SELL option")
    
#     try:
#         order_PE=kite.place_order(variety=kite.VARIETY_REGULAR,
#                       exchange=kite.EXCHANGE_NFO,
#                       tradingsymbol=straddle_pe_symbol,
#                       transaction_type=trans_type,
#                       quantity=LOT_SIZE*SELL_LOTS,
#                       product=kite.PRODUCT_NRML,
#                       order_type=kite.ORDER_TYPE_MARKET,
#                       price=97,
#                       validity=None,
#                       disclosed_quantity=None,
#                       trigger_price=None,
#                       squareoff=None,
#                       stoploss=None,
#                       trailing_stoploss=None
#                       )
#         print(order_PE)
#         logging.info('Order placed successfully, orderId = %s', orderId)
#     except :  print("ERROR - Placing Put SELL option")
       
   

# function to place the orders
def place_order(trans_type):
    try:
        order_CE=kite.place_order(variety=kite.VARIETY_REGULAR,
                      exchange=kite.EXCHANGE_NFO,
                      tradingsymbol=straddle_ce_symbol,
                      transaction_type=trans_type,
                      quantity=LOT_SIZE*SELL_LOTS,
                      product=kite.PRODUCT_NRML,
                      order_type=kite.ORDER_TYPE_MARKET,
                      price=None,
                      validity=None,
                      disclosed_quantity=None,
                      trigger_price=None,
                      squareoff=None,
                      stoploss=None,
                      trailing_stoploss=None
                      )
        logging.info('Order placed successfully, orderId = %s', orderId)
        print(order_CE)
    except :  print("ERROR - Placing Call SELL option")
    
    try:
        order_PE=kite.place_order(variety=kite.VARIETY_REGULAR,
                     exchange=kite.EXCHANGE_NFO,
                     tradingsymbol=straddle_pe_symbol,
                     transaction_type=trans_type,
                     quantity=LOT_SIZE*SELL_LOTS,
                     product=kite.PRODUCT_NRML,
                     order_type=kite.ORDER_TYPE_MARKET,
                     price=None,
                     validity=None,
                     disclosed_quantity=None,
                     trigger_price=None,
                     squareoff=None,
                     stoploss=None,
                     trailing_stoploss=None
                     )
        print(order_PE)
        logging.info('Order placed successfully, orderId = %s', orderId)
    except :  print("ERROR - Placing Put SELL option")
       
    
        
if __name__=='__main__':
    # find the atm price for shorting
    current_price = getCMP(INSTRUMENT_TYPE);
    print("CURRENT ATM  PRICE => ",current_price)
    atm_strike_price=round(current_price,-2)
    print("CURRENT ATM STRIKE PRICE => ",atm_strike_price)
   
    # find the next expiry datetime (finnity TUESDAY else THURSDAY)
    if INSTRUMENT_NAME=="FINNIFTY" :
        next_expiry = datetime.today() + relativedelta(weekday=TU(1))
    else:
        next_expiry = datetime.today() + relativedelta(weekday=TH(1))
 
    straddle_ce_symbol = get_symbols(next_expiry.date(), INSTRUMENT_NAME, atm_strike_price, 'CE')
    straddle_pe_symbol = get_symbols(next_expiry.date(), INSTRUMENT_NAME, atm_strike_price, 'PE')
    
    print(straddle_ce_symbol)
    print(straddle_pe_symbol)  
    
    # place orders
    place_order(kite.TRANSACTION_TYPE_SELL)
   
    
    



