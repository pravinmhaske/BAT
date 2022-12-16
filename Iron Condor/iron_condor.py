# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta, TH, TU
from app_kite_trade import *
import app_token
import constants
from nsepy.derivatives import get_expiry_date
from nsepython import nse_optionchain_scrapper, nse_expirydetails

kite = KiteApp(enctoken=app_token.TKN)

# variable for straddle starts

# sell_ce_symbol = ""
# sell_pe_symbol = ""
# buy_ce_symbol = ""
# buy_pe_symbol = ""
instrumentsList = None

total_premium = 0
sell_ce_premium = 0
sell_pe_premium = 0

order_ids = {
    "sell_ce_ord_id": "",
    "sell_pe_ord_id": "",
    "buy_ce_ord_id": "",
    "buy_pe_ord_id": "",
}


# variable for straddle ends

def get_cmp(symbol):
    try:
        quote = kite.quote(symbol)
        if quote:
            return quote[symbol]['last_price']
        else:
            return 0
    except:
        print("Error while getting quote for symbol")


def get_symbols(expiry, name, strike, ins_type):
    global instrumentsList
    try:
        if instrumentsList is None:
            instrumentsList = kite.instruments('NFO')

        lst_b = [num for num in instrumentsList if num['expiry'] == expiry and num['strike'] == strike
                 and num['instrument_type'] == ins_type and num['name'] == name]
        return lst_b[0]['tradingsymbol']
    except:
        print("ERROR while getting symbol")


# function to place the Buy and sell orders
def place_order(trans_type, symbol):
    order_id = kite.place_order(variety=kite.VARIETY_AMO,
                                exchange=kite.EXCHANGE_NFO,
                                tradingsymbol=symbol,
                                transaction_type=trans_type,
                                quantity=constants.LOT_SIZE * constants.SELL_LOTS,
                                product=kite.PRODUCT_MIS,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                price=97,
                                validity=None,
                                disclosed_quantity=None,
                                trigger_price=None,
                                squareoff=None,
                                stoploss=None,
                                trailing_stoploss=None
                                )
    if order_id is None:
        print(f"ERROR - While placing  Order for  {symbol}")
    else:
        print(f"( {trans_type}) ORDER PLACED for , SYMBOL - {symbol} , ORDER ID => {order_id}")
    return order_id


def trigger_iron_condor_orders():
    current_price = get_cmp(constants.INSTRUMENT_TYPE)
    atm_strike_price = round(current_price, -2)
    print(f"CURRENT PRICE => {current_price} , ATM => ({atm_strike_price})")

    if current_price == 0:
        print("ERROR => PLEASE RECHECK YOUR ACCESS TOKEN. SEEMS ISSUE WITH AUTHORIZATION. ")
    else:
        payload = nse_optionchain_scrapper(constants.INSTRUMENT_NAME)
        current_expiry = nse_expirydetails(payload, 0)[0]

        sell_ce_symbol = get_symbols(current_expiry, constants.INSTRUMENT_NAME,
                                     atm_strike_price + constants.STRIKE_SELL_DIFF, 'CE')
        sell_pe_symbol = get_symbols(current_expiry, constants.INSTRUMENT_NAME,
                                     atm_strike_price - constants.STRIKE_SELL_DIFF, 'PE')
        buy_ce_symbol = get_symbols(current_expiry, constants.INSTRUMENT_NAME,
                                    atm_strike_price + constants.STRIKE_BUY_DIFF, 'CE')
        buy_pe_symbol = get_symbols(current_expiry, constants.INSTRUMENT_NAME,
                                    atm_strike_price - constants.STRIKE_BUY_DIFF, 'PE')

        # sell_ce_primium = kite.ltp(f"NFO:{sell_ce_symbol}")[f"NFO:{sell_ce_symbol}"]["last_price"]
        # sell_ce_primium = kite.ltp(f"NFO:{sell_pe_symbol}")[f"NFO:{sell_pe_symbol}"]["last_price"]

        print("*************** PLACING IC ORDERS ********************")
        place_order(kite.TRANSACTION_TYPE_BUY, buy_ce_symbol)
        # place_order(kite.TRANSACTION_TYPE_SELL, sell_ce_symbol)
        # place_order(kite.TRANSACTION_TYPE_BUY, buy_pe_symbol)
        place_order(kite.TRANSACTION_TYPE_SELL, sell_pe_symbol)
        print("*************** ORDER PLACEMENT FINISHED ********************")


# def adjustments():
#     print("inside adjustments")
#     print(f"NFO:{sell_ce_symbol}")

#     kite.ltp("NFO:BANKNIFTY22D1544600CE")
#     cur_sell_ce_primium=kite.ltp(f"NFO:{sell_ce_symbol}")[f"NFO:{sell_ce_symbol}"]["last_price"]
#     if (cur_sell_ce_primium/sell_ce_primium)*100 >=70 :#if premium decay is more tan 70%
#         # modify previous call order 
#         kite.ltp("NFO:BANKNIFTY22D1544600CE")

if __name__ == '__main__':
    # logging.info('Order placed dasdsadas')
    trigger_iron_condor_orders()
    # adjustments()
