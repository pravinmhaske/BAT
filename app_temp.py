# function to place the orders
def place_order(trans_type):
    try:
        order_CE=kite.place_order(variety=kite.VARIETY_AMO,
                      exchange=kite.EXCHANGE_NFO,
                      tradingsymbol=sell_ce_symbol if trans_type ==kite.TRANSACTION_TYPE_SELL else buy_ce_symbol,
                      transaction_type=trans_type,
                      quantity=LOT_SIZE*SELL_LOTS,
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
        print("CE SELL ORDER ID =>",order_CE)
        logging.info('Order placed successfully, orderId = %s', orderId)
    except :  print("ERROR - Placing Call SELL option")
    
    try:
        order_PE=kite.place_order(variety=kite.VARIETY_AMO,
                      exchange=kite.EXCHANGE_NFO,
                      tradingsymbol=sell_pe_symbol if trans_type ==kite.TRANSACTION_TYPE_SELL else buy_pe_symbol,
                      transaction_type=trans_type,
                      quantity=LOT_SIZE*SELL_LOTS,
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
        print("PE SELL ORDER ID =>",order_PE)
        logging.info('Order placed successfully, orderId = %s', orderId)
    except :  print("ERROR - Placing Put SELL option")
    
    
    ==================
    
    # function to place the  orders
    def place_order(trans_type,buy_strike_price,sell_strike_price):
        try:
            order_CE=kite.place_order(variety=kite.VARIETY_REGULAR,
                          exchange=kite.EXCHANGE_NFO,
                          tradingsymbol=sell_ce_symbol if trans_type ==kite.TRANSACTION_TYPE_SELL else buy_ce_symbol,
                          transaction_type=trans_type,
                          quantity=LOT_SIZE*SELL_LOTS,
                          product=kite.PRODUCT_MIS,
                          order_type=kite.ORDER_TYPE_MARKET,
                          price=97,
                          validity=None,
                          disclosed_quantity=None,
                          trigger_price=None,
                          squareoff=None,
                          stoploss=None,
                          trailing_stoploss=None
                          )
            print("CE SELL ORDER ID =>",order_CE)
            logging.info('Order placed successfully, orderId = %s', orderId)
        except :  print("ERROR - Placing Call SELL option")
        
        try:
            order_PE=kite.place_order(variety=kite.VARIETY_REGULAR,
                          exchange=kite.EXCHANGE_NFO,
                          tradingsymbol=sell_pe_symbol if trans_type ==kite.TRANSACTION_TYPE_SELL else buy_pe_symbol,
                          transaction_type=trans_type,
                          quantity=LOT_SIZE*SELL_LOTS,
                          product=kite.PRODUCT_MIS,
                          order_type=kite.ORDER_TYPE_MARKET,
                          price=97,
                          validity=None,
                          disclosed_quantity=None,
                          trigger_price=None,
                          squareoff=None,
                          stoploss=None,
                          trailing_stoploss=None
                          )
            print("PE SELL ORDER ID =>",order_PE)
            logging.info('Order placed successfully, orderId = %s', orderId)
        except :  print("ERROR - Placing Put SELL option")
      ============================  
        order_ids = {
          "sell_ce_ord_id": "",
          "sell_pe_ord_id": "",
          "buy_ce_ord_id": "",
          "
          ================
          
          # function to place the Buy and sell orders
          def place_order(buy_strike_price,sell_strike_price,leg):
              try:
                  # sell_ce_symbol if trans_type ==kite.TRANSACTION_TYPE_SELL else buy_ce_symbol
                  buy_order_Id=kite.place_order(variety=kite.VARIETY_REGULAR,
                                exchange=kite.EXCHANGE_NFO,
                                tradingsymbol=buy_strike_price,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
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
                  if leg==kite.OPTION_CALL_LEG:
                      order_ids["buy_ce_ord_id"]=buy_order_Id
                  else : 
                      order_ids["buy_pe_ord_id"]=buy_order_Id
                  print(f"BUY ORDER PLCAED for LEG {leg} , strike - {buy_strike_price} , ORDER ID => {buy_order_Id}")
              except :  print(f"ERROR - Placing BUY Order for  {buy_strike_price}")
              
              try:
                  sell_order_Id=kite.place_order(variety=kite.VARIETY_REGULAR,
                                exchange=kite.EXCHANGE_NFO,
                                tradingsymbol=sell_strike_price,
                                transaction_type=kite.TRANSACTION_TYPE_SELL,
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
                  if leg==kite.OPTION_CALL_LEG:
                      order_ids["sell_ce_ord_id"]=sell_order_Id
                  else : 
                      order_ids["sell_pe_ord_id"]=sell_order_Id
                  print(f"SELL ORDER PLCAED for  LEG {leg} , strike - {sell_strike_price} , ORDER ID => {sell_order_Id}");
              except :  print(f"ERROR - Placing SELL Order for  {sell_strike_price}")
              
              ====================================
              # function to place the Buy and sell orders
              def place_order(trans_type,symbol):
               
                     order_Id=kite.place_order(variety=kite.VARIETY_REGULAR,
                                    exchange=kite.EXCHANGE_NFO,
                                    tradingsymbol=symbol,
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
                     if order_Id is None:
                         print(f"ERROR - While placing  Order for  {symbol}")
                         print("*********************** ERROR **************************")
                     else :
                         print(f"BUY ORDER PLCAED for , symbol - {symbol} , ORDER ID => {order_Id}")
                         print("*********************** SUCCESS **************************")

 =================================                    return order_Id
========================================================

# -*- coding: utf-8 -*-

import os
import logging

try:
    import requests
except ImportError:
    os.system('python -m pip install requests')
try:
    import dateutil
except ImportError:
    os.system('python -m pip install python-dateutil')

import requests
import dateutil.parser


def get_enctoken(userid, password, twofa):
    session = requests.Session()
    response = session.post('https://kite.zerodha.com/api/login', data={
        "user_id": userid,
        "password": password
    })
    response = session.post('https://kite.zerodha.com/api/twofa', data={
        "request_id": response.json()['data']['request_id'],
        "twofa_value": twofa,
        "user_id": response.json()['data']['user_id']
    })
    enctoken = response.cookies.get('enctoken')
    if enctoken:
        return enctoken
    else:
        raise Exception("Enter valid details !!!!")


class KiteApp:
    # Products
    PRODUCT_MIS = "MIS"
    PRODUCT_CNC = "CNC"
    PRODUCT_NRML = "NRML"
    PRODUCT_CO = "CO"

    # Order types
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_SLM = "SL-M"
    ORDER_TYPE_SL = "SL"

    # Varities
    VARIETY_REGULAR = "regular"
    VARIETY_CO = "co"
    VARIETY_AMO = "amo"

    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    # Validity
    VALIDITY_DAY = "DAY"
    VALIDITY_IOC = "IOC"

    # Exchanges
    EXCHANGE_NSE = "NSE"
    EXCHANGE_BSE = "BSE"
    EXCHANGE_NFO = "NFO"
    EXCHANGE_CDS = "CDS"
    EXCHANGE_BFO = "BFO"
    EXCHANGE_MCX = "MCX"

    # Legts
    OPTION_PUT_LEG = "PE"
    OPTION_CALL_LEG = "CE"

    def __init__(self, enctoken):
        print(enctoken)
        self.headers = {"Authorization": enctoken}
        self.session = requests.session()
        self.root_url = "https://api.kite.trade"
        # self.root_url = "https://kite.zerodha.com/oms"
        self.session.get(self.root_url, headers=self.headers)

    def instruments(self, exchange=None):
        data = self.session.get(self.root_url + "/instruments", headers=self.headers).text.split("\n")
        Exchange = []

        # return data
        for i in data[1:-1]:
            row = i.split(",")
            if exchange is None or exchange == row[11]:
                Exchange.append({'instrument_token': int(row[0]), 'exchange_token': row[1], 'tradingsymbol': row[2],
                                 'name': row[3][1:-1], 'last_price': float(row[4]),
                                 'expiry': dateutil.parser.parse(row[5]).date() if row[5] != "" else None,
                                 'strike': float(row[6]), 'tick_size': float(row[7]), 'lot_size': int(row[8]),
                                 'instrument_type': row[9], 'segment': row[10],
                                 'exchange': row[11]})
        return Exchange

    def quote(self, instruments):

        data = self.session.get(self.root_url + "/quote", params={"i": instruments}, headers=self.headers).json()[
            "data"]

        return data

    def ohlc(self, instruments):
        data = self.session.get(self.root_url + "/quote/ohlc", params={"i": instruments}, headers=self.headers).json()[
            "data"]
        return data

    def ltp(self, instruments):
        data = self.session.get(self.root_url + "/quote/ltp", params={"i": instruments}, headers=self.headers).json()[
            "data"]
        return data

    def historical_data(self, instrument_token, from_date, to_date, interval, continuous=False, oi=False):
        params = {"from": from_date,
                  "to": to_date,
                  "interval": interval,
                  "continuous": 1 if continuous else 0,
                  "oi": 1 if oi else 0}

        lst = self.session.get(
            f"{self.root_url}/instruments/historical/{instrument_token}/{interval}", params=params,
            headers=self.headers).json()["data"]["candles"]
        records = []
        for i in lst:
            record = {"date": dateutil.parser.parse(i[0]), "open": i[1], "high": i[2], "low": i[3],
                      "close": i[4], "volume": i[5], }
            if len(i) == 7:
                record["oi"] = i[6]
            records.append(record)
        return records

    #  done
    def margins(self):
        margins = self.session.get(self.root_url + "/user/margins", headers=self.headers).json()["data"]
        return margins

    #  done
    def orders(self):
        orders = self.session.get(self.root_url + "/orders", headers=self.headers).json()["data"]
        return orders

    #  done
    def positions(self):
        positions = self.session.get(self.root_url + "/portfolio/positions", headers=self.headers).json()["data"]
        return positions

    #  done
    def place_order(self, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type
                    , price=None,
                    validity=None, disclosed_quantity=None, trigger_price=None, squareoff=None, stoploss=None,
                    trailing_stoploss=None
                    ):
        params = locals()
        del params["self"]
        for k in list(params.keys()):
            if params[k] is None:
                del params[k]
        try:
            # print(self.session.post(self.root_url + "/orders/" +variety,data=params, headers=self.headers).json())
            response = self.session.post(self.root_url + "/orders/" + variety, data=params, headers=self.headers).json()
            if response["status"] == "success":
                order_id = response["data"]["order_id"]
                return order_id
            else:
                print("ERROR from server   ===> ", response["message"])
        except Exception as e:
            print("ERROR occurred => ", e)
            return e

    def modify_order(self, variety, order_id, parent_order_id=None, quantity=None, price=None, order_type=None,
                     trigger_price=None, validity=None, disclosed_quantity=None):
        try:
            params = locals()
            del params["self"]
            for k in list(params.keys()):
                if params[k] is None:
                    del params[k]

            order_id = self.session.put(self.root_url + "/orders/" + variety + "/" + order_id,
                                        data=params, headers=self.headers).json()["data"][
                "order_id"]
            return order_id
        except Exception as e:
            print("Error occurred => ", e)
            return e

    def cancel_order(self, variety, order_id, parent_order_id=None):
        order_id = self.session.delete(self.root_url + "/orders/" + variety + "/" + order_id,
                                       data={"parent_order_id": parent_order_id} if parent_order_id else {},
                                       headers=self.headers).json()["data"]["order_id"]
        return order_id
