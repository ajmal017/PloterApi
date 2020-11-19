# Ploter AI Starter Project.
# Interactive Broker API Connection.

import argparse
import datetime
import logging
import os
import time

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.common import OrderId
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.utils import iswrapper


class PloterIBWrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)


class PloterIBClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class PloterApp(PloterIBWrapper, PloterIBClient):
    def __init__(self):
        PloterIBWrapper.__init__(self)
        PloterIBClient.__init__(self, wrapper=self)

    @iswrapper
    # ! [openorder]
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. PermId: ", order.permId, "ClientId:", order.clientId, " OrderId:", orderId,
              "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQty:", order.totalQuantity, "CashQty:", order.cashQty,
              "LmtPrice:", order.lmtPrice, "AuxPrice:", order.auxPrice, "Status:", orderState.status)


def setup_logger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)


def main():
    setup_logger()
    logging.warning("now is %s", datetime.datetime.now())
    logging.getLogger().setLevel(logging.WARNING)

    cmd_line_parser = argparse.ArgumentParser("api tests")
    cmd_line_parser.add_argument("-p", "--port", action="store", type=int,
                                 dest="port", default=7496, help="The TCP port to use")
    cmd_line_parser.add_argument("-C", "--global-cancel", action="store_true",
                                 dest="global_cancel", default=False,
                                 help="whether to trigger a globalCancel req")
    args = cmd_line_parser.parse_args()
    print("Using args", args)
    logging.debug("Using args %s", args)

    # enable logging when member vars are assigned
    from ibapi import utils
    Order.__setattr__ = utils.setattr_log

    try:
        app = PloterApp()
        if args.global_cancel:
            app.globalCancelOnly = True
        # ! [connect]
        app.connect("127.0.0.1", args.port, clientId=0)
        # ! [connect]
        print("serverVersion:%s" % app.serverVersion())

        # ! [clientrun]
        app.run()
        app.reqOpenOrders()
        # ! [clientrun]
    except:
        print("Connection Error")
    finally:
        print("Connected")


if __name__ == "__main__":
    main()
