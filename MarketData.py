from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import EWrapper

import threading
import time
import logging


class IBapi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self, self)

  def error(self, reqId, errorCode, errorString):
    print("Error: ", reqId, " ", errorCode, " ", errorString)

  def tickPrice(self, reqId, tickType, price, attrib):
      print ("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=" ")

  def tickSize(self, reqId, tickType, size):
      print ("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 0)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"
contract.primaryExchange = "NASDAQ"

app.reqMarketDataType(4)  # switch to delayed-frozen data if live is not available
app.reqMktData(1, contract, "", False, False, [])


# comment below lines if your connection is slow
time.sleep(10) #sleep to allow enough time for data to be returned
app.disconnect()
  
