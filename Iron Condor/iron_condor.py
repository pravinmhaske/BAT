# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta, TH, TU
from app_kite_trade import *
import app_token
import constants as const
from nsepy.derivatives import get_expiry_date
from nsepython import nse_optionchain_scrapper, nse_expirydetails
import schedule
import time
import mibian
import database
import math

kite = KiteApp(enctoken=app_token.TKN)

# variable for IC starts
instrumentsList = None


# variable for IC ends


def get_cmp(symbol):
    try:
        quote = kite.quote(symbol)
        if quote:
            return quote[symbol]['last_price']
        else:
            return 0
    except Exception as e:
        print("Error while getting quote for symbol ", e)


def get_symbols(expiry, name, strike, ins_type):
    global instrumentsList
    try:
        if instrumentsList is None:
            instrumentsList = kite.instruments('NFO')

        lst_b = [num for num in instrumentsList if num['expiry'] == expiry and num['strike'] == strike
                 and num['instrument_type'] == ins_type and num['name'] == name]
        return lst_b[0]['tradingsymbol']
    except Exception as e:
        print("ERROR while getting symbol ", e)


# function to place the Buy and sell orders
def place_order(trans_type, symbol):
    # order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
    order_id = kite.place_order(variety=kite.VARIETY_AMO,
                                exchange=kite.EXCHANGE_NFO,
                                tradingsymbol=symbol,
                                transaction_type=trans_type,
                                quantity=const.LOT_SIZE * const.SELL_LOTS,
                                # product=kite.PRODUCT_MIS,
                                product=kite.PRODUCT_NRML,
                                # order_type=kite.ORDER_TYPE_MARKET,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                price=3,
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


def get_current_expiry():
    payload = nse_optionchain_scrapper(const.INSTRUMENT_NAME)
    current_expiry = nse_expirydetails(payload, 0)[0]
    return current_expiry


def print_order_info(current_expiry, atm_str_price, spot_price):
    buy, sell = [kite.TRANSACTION_TYPE_BUY, kite.TRANSACTION_TYPE_SELL]
    c_leg, p_leg = [kite.OPTION_CALL_LEG, kite.OPTION_PUT_LEG]
    sell_diff, buy_diff = [const.STRIKE_SELL_DIFF, const.STRIKE_BUY_DIFF]

    buy_pe_symbol = get_ic_symbols(current_expiry, atm_str_price, buy, p_leg)
    sell_pe_symbol = get_ic_symbols(current_expiry, atm_str_price, sell, p_leg)
    sell_ce_symbol = get_ic_symbols(current_expiry, atm_str_price, sell, c_leg)
    buy_ce_symbol = get_ic_symbols(current_expiry, atm_str_price, buy, c_leg)

    print("================================================")
    print(f" [{const.INSTRUMENT_NAME}] - ({current_expiry}) IC ORDER STRIKES  ")
    print(f" ++ B (PE) -{buy_diff} - [{atm_str_price - const.STRIKE_BUY_DIFF}] {get_premium(buy_pe_symbol)}")
    print(f" -- S (PE) -{sell_diff} - [{atm_str_price - const.STRIKE_SELL_DIFF}] {get_premium(sell_pe_symbol)}")
    print(f"---------- SPOT - [{round(spot_price, -2)}] -----")
    print(f" -- S (CE) +{sell_diff} - [{atm_str_price + const.STRIKE_SELL_DIFF}] {get_premium(sell_ce_symbol)}")
    print(f" ++ B (CE) +{buy_diff} - [{atm_str_price + const.STRIKE_BUY_DIFF}] {get_premium(buy_ce_symbol)}")
    print("================================================")


def get_premium(ic_symbol):
    return kite.ltp(f"NFO:{ic_symbol}")[f"NFO:{ic_symbol}"]["last_price"]


def store_values_database(order_list):
    # order_list = get_order_obj(atm_str_price)
    is_db_exist = database.check_db_exist()
    if is_db_exist:
        database.insert_data(order_list)
    else:
        database.create_orders()
        database.insert_data(order_list)


# def get_atm_strk_price(spot_price):
#     str_price = round(spot_price, -2)
#     return math.trunc(str_price)

def get_ic_symbols(current_expiry, atm_str_price, tran_type, leg):
    if tran_type == kite.TRANSACTION_TYPE_BUY and leg == kite.OPTION_PUT_LEG:
        strike_price = atm_str_price - const.STRIKE_BUY_DIFF
    elif tran_type == kite.TRANSACTION_TYPE_SELL and leg == kite.OPTION_PUT_LEG:
        strike_price = atm_str_price - const.STRIKE_SELL_DIFF
    elif tran_type == kite.TRANSACTION_TYPE_SELL and leg == kite.OPTION_CALL_LEG:
        strike_price = atm_str_price + const.STRIKE_SELL_DIFF
    else:
        strike_price = atm_str_price + const.STRIKE_BUY_DIFF

    return get_symbols(current_expiry, const.INSTRUMENT_NAME, strike_price, leg)


def get_order_obj(current_expiry, atm_str_price, order_id, tran_type, spot_price, leg):
    if tran_type == kite.TRANSACTION_TYPE_BUY and leg == kite.OPTION_PUT_LEG:
        strike_price = atm_str_price - const.STRIKE_BUY_DIFF
    elif tran_type == kite.TRANSACTION_TYPE_SELL and leg == kite.OPTION_PUT_LEG:
        strike_price = atm_str_price - const.STRIKE_SELL_DIFF
    elif tran_type == kite.TRANSACTION_TYPE_SELL and leg == kite.OPTION_CALL_LEG:
        strike_price = atm_str_price + const.STRIKE_SELL_DIFF
    else:
        strike_price = atm_str_price + const.STRIKE_BUY_DIFF

    ic_symbol = get_symbols(current_expiry, const.INSTRUMENT_NAME, strike_price, leg)
    return (
        order_id, ic_symbol, tran_type,
        strike_price, get_premium(ic_symbol), spot_price, datetime.now())


def trigger_iron_condor_orders():
    order_placed = False
    # global spot_price
    spot_price = math.trunc(get_cmp(const.INSTRUMENT_TYPE))
    atm_str_price = round(spot_price, -2)
    if spot_price == 0:
        print("ERROR => PLEASE RECHECK YOUR ACCESS TOKEN. SEEMS ISSUE WITH AUTHORIZATION. ")
    else:
        print(f"CURRENT PRICE => {spot_price} , ATM => ({atm_str_price})")
        cur_expiry = get_current_expiry()
        # assign_ic_strike_symbols(current_expiry, atm_str_price)
        print_order_info(cur_expiry, atm_str_price, spot_price)

        buy, sell = [kite.TRANSACTION_TYPE_BUY, kite.TRANSACTION_TYPE_SELL]
        c_leg, p_leg = [kite.OPTION_CALL_LEG, kite.OPTION_PUT_LEG]

        confirmation = input('PLEASE CONFIRM? (Y/N) :')
        if confirmation == 'Y' or confirmation == 'y':

            print(f"*************** PLACING [{const.INSTRUMENT_NAME}] IC ORDERS ********************")
            buy_pe_order = place_order(buy, get_ic_symbols(cur_expiry, atm_str_price, buy, p_leg))
            sell_pe_order = place_order(sell, get_ic_symbols(cur_expiry, atm_str_price, sell, p_leg))
            buy_ce_order = place_order(buy, get_ic_symbols(cur_expiry, atm_str_price, buy, c_leg))
            sell_ce_order = place_order(sell, get_ic_symbols(cur_expiry, atm_str_price, sell, c_leg))
            print("*************** ORDER PLACEMENT FINISHED ********************")

            if buy_pe_order and sell_pe_order and sell_ce_order and buy_ce_order:
                buy_pe_tpl = get_order_obj(cur_expiry, atm_str_price, buy_pe_order, buy, atm_str_price, p_leg)
                sell_pe_tpl = get_order_obj(cur_expiry, atm_str_price, sell_pe_order, sell, atm_str_price, p_leg)
                sell_ce_tpl = get_order_obj(cur_expiry, atm_str_price, buy_ce_order, sell, atm_str_price, c_leg)
                buy_ce_tpl = get_order_obj(cur_expiry, atm_str_price, sell_ce_order, buy, atm_str_price, c_leg)

                order_list = [buy_pe_tpl, sell_pe_tpl, sell_ce_tpl, buy_ce_tpl]
                print(order_list)
                store_values_database(order_list)
                order_placed = True

            return order_placed
        else:
            return order_placed


# def square_off():
#     # if I Condor becomes I Fly then close all trades
#     kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["buy_ce_ord_id"])
#     kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["sell_ce_ord_id"])
#     kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["buy_pe_ord_id"])
#     kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["sell_pe_ord_id"])
#     order_ids["buy_ce_ord_id"] = None
#     order_ids["sell_ce_ord_id"] = None
#     order_ids["buy_pe_ord_id"] = None
#     order_ids["sell_pe_ord_id"] = None


# def get_option_delta(strike_symbol, leg):
#     interest = 10
#     current_spot_price = get_cmp(const.INSTRUMENT_TYPE)
#     option_ltp = kite.ltp(f"NFO:{strike_symbol}")[f"NFO:{strike_symbol}"]["last_price"];
#     current_expiry = get_current_expiry()
#     days_left = current_expiry - datetime.now()
#
#     if leg == kite.OPTION_CALL_LEG:
#         strike_price = round(spot_price, -2) + const.STRIKE_SELL_DIFF
#     else:
#         strike_price = round(spot_price, -2) - const.STRIKE_SELL_DIFF
#
#     if leg == kite.OPTION_CALL_LEG:
#         obj = mibian.BS([current_spot_price, (round(spot_price, -2) + const.STRIKE_SELL_DIFF), interest, days_left],
#                         callPrice=option_ltp)
#     else:
#         obj = mibian.BS([current_spot_price, (round(spot_price, -2) - const.STRIKE_SELL_DIFF), interest, days_left],
#                         putPrice=option_ltp)
#
#     iv = obj.impliedVolatility
#     print(" iv =>", iv)
#     mib_obj = mibian.BS([current_spot_price, strike_price, interest, days_left], volatility=iv)
#     if leg == kite.OPTION_CALL_LEG:
#         return mib_obj.callDelta
#     else:
#         return mib_obj.putDelta
#
#
# # get_option_delta
#
# def adjustments():
#     print("inside adjustments", spot_price)
#
#     response = database.fetch_data()
#     print(response)
#     # print(f"NFO:{ic_strike_symbols['sell_ce']}")
#     cur_sell_ce_premium = kite.ltp(f"NFO:{ic_strike_symbols['sell_ce']}")[f"NFO:{ic_strike_symbols['sell_ce']}"][
#         "last_price"]
#     cur_sell_pe_premium = kite.ltp(f"NFO:{ic_strike_symbols['sell_pe']}")[f"NFO:{ic_strike_symbols['sell_pe']}"][
#         "last_price"]
#     has_sell_ce_decay = (cur_sell_ce_premium / selling_premium["CE"]) * 100 >= 70
#     has_sell_pe_decay = (cur_sell_pe_premium / selling_premium["PE"]) * 100 >= 70
#
#     # write condition if break even se jyada either side cut trade
#
#     if ic_strike_symbols["sell_pe"] == ic_strike_symbols["sell_ce"] or has_sell_pe_decay and has_sell_ce_decay:
#         square_off();
#     elif has_sell_ce_decay:  # if premium decay is more tan 70%
#         buy_ce_order_id = kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["buy_ce_ord_id"])
#         sell_ce_order_id = kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["sell_ce_ord_id"])
#         if buy_ce_order_id is not None and sell_ce_order_id is not None:
#             order_ids["buy_ce_ord_id"] = None
#             order_ids["sell_ce_ord_id"] = None
#             # code for
#     elif has_sell_pe_decay:
#         buy_pe_order_id = kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["buy_pe_ord_id"])
#         sell_pe_order_id = kite.cancel_order(variety=kite.VARIETY_AMO, order_id=order_ids["sell_pe_ord_id"])
#         if buy_pe_order_id is not None and sell_pe_order_id is not None:
#             order_ids["buy_pe_ord_id"] = None
#             order_ids["sell_pe_ord_id"] = None
#     else:
#         print("Adjustments not required so far.")
#
#         # kite.ltp("NFO:BANKNIFTY22D1544600CE")
#
#
# def adjustment_schedular(order_placed):
#     if order_placed:
#         # schedular for checking adjustment every 5 minutes
#         schedule.every(5).minutes.do(adjustments)
#         while order_ids["buy_pe_ord_id"] is None and order_ids["buy_ce_ord_id"] is None and \
#                 order_ids["sell_pe_ord_id"] is None and order_ids["sell_ce_ord_id"] is None:
#             schedule.run_pending()
#             time.sleep(1)
#

if __name__ == '__main__':
    has_order_placed = trigger_iron_condor_orders()
    if not has_order_placed:
        print(" ERROR - Order/s were not placed. Please check logs.")
    else:
        print(" has_order_placed ,", has_order_placed)
        # adjustment_schedular(has_order_placed)

    # adjustments()

    # delta_sell_ce = get_option_delta(ic_strike_symbols["sell_ce"], "CE")
    # print(delta_sell_ce)
