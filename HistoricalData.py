# to retrieve the last 10 hourly candlebars

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
	def historicalData(self, reqId, bar):
		print(f'HistroicalData: {reqId}, Time: {bar.date}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}, Count: {bar.barCount}, WAP: {bar.average}')
		
def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 0)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'EUR'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'USD'

#Request historical candles  
app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 1, False, [])

# comment below lines if your connection is slow
time.sleep(10) #sleep to allow enough time for data to be returned
app.disconnect()