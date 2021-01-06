import websocket
import json
import time
import config
cfg = config.Config('config')


def on_open(ws):
    # Login to exchange
    payload = {"UserName": cfg.Username, "Password": cfg.Password}
    message = {"m": 0, "i": 1, "n": "AuthenticateUser", "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)
    # Start trading process
    CancelAllOrders()


def on_message(ws, message):
    global currentBid, currentAsk, usdtBal, cadBal, spread, spreadPercent

    """ SEQUENCE OF METHODS:
    1. CancelAllOrders, defined by on_open
    2. GetLevel1 (currentBid, currentAsk, spread, spreadPercent)
        if spread is too tight wait, then CancelAllOrders
        else continue to GetAccountPositions
    3. GetAccountPositions (usdtBal, cadBal)
        if cadBal has more USD equivalent value than usdtBal, SendOrderBuy
        if usdtBal has more value than cadBal equivalent, SendOrderSell
    4. sendOrderXXX, wait, restart sequence with CancelAllOrders
    """
    jmessage = json.loads(message)

    if jmessage['n'] in ['CancelAllOrders']:
        time.sleep(1)
        GetLevel1()

    if jmessage['n'] in ["GetLevel1"]:
        currentBid = float(json.loads(jmessage['o'])["BestBid"])
        currentAsk = float(json.loads(jmessage['o'])["BestOffer"])
        spread = currentAsk-currentBid
        spreadPercent = (spread/((currentAsk+currentBid)*0.5))*100

        # Check if spread allows profit making
        if (spreadPercent < 0.8):
            time.sleep(120)
            GetLevel1()
        else:
            GetAccountPositions()

    if jmessage['n'] in ['GetAccountPositions']:
        # Getting usdtBal, cadBal from JSON message
        for x in json.loads(jmessage['o']):
            if (x['ProductSymbol'] == "USDT"):
                usdtBal = float(x['Amount'])
            if (x['ProductSymbol'] == "CAD"):
                cadBal = float(x['Amount'])

        if (usdtBal < cadBal*(1/currentAsk)):
            # more cad than usdt, buy usdt
            SendOrderBuy()
        if (cadBal*(1/currentAsk) < usdtBal):
            # more usdt than cad, sell usdt
            SendOrderSell()

    if jmessage['n'] in ['SendOrder']:
        # Lifetime of order on exchange
        time.sleep(20)
        # Reset sequence
        CancelAllOrders()


def on_close(ws):
    print("exited")


def GetLevel1():

    payload = {
        "omsId": 1,
        "InstrumentId": int(cfg.USDT_CAD_ID)
    }

    message = {"m": 0,
               "i": 2,
               "n": "GetLevel1",
               "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)


def GetAccountPositions():
    payload = {
        "omsId": 1,
        "accountId": int(cfg.AccountID)
    }

    message = {"m": 0,
               "i": 2,
               "n": "GetAccountPositions",
               "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)


def GetAccountTrades():
    payload = {
        "omsId": 1,
        "accountId": int(cfg.AccountID),
        "StartIndex": 0,
        "Count": 10

    }

    message = {"m": 0,
               "i": 2,
               "n": "GetAccountTrades",
               "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)


def SendOrderBuy():
    payload = {
        "InstrumentId": int(cfg.USDT_CAD_ID),
        "OMSId": 1,
        "AccountId": int(cfg.AccountID),
        "TimeInForce": 1,
        "ClientOrderId": 0,
        "orderIdOCO": 0,
        "UseDisplayQuantity": False,
        "Side": 0,
        "quantity": round(cadBal*(1/currentAsk)*0.98, 2),
        "OrderType": 2,
        "LimitPrice": round(currentBid+0.0001, 4)}
    message = {"m": 0,
               "i": 2,
               "n": "SendOrder",
               "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)


def SendOrderSell():
    payload = {
        "InstrumentId": int(cfg.USDT_CAD_ID),
        "OMSId": 1,
        "AccountId": int(cfg.AccountID),
        "TimeInForce": 1,
        "ClientOrderId": 1,
        "orderIdOCO": 1,
        "UseDisplayQuantity": False,
        "Side": 1,
        "quantity": round(usdtBal*0.98, 2),
        "OrderType": 2,
        "LimitPrice": round(currentAsk-0.0001, 4)}
    message = {"m": 0,
               "i": 2,
               "n": "SendOrder",
               "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)


def CancelAllOrders():

    payload = {
        "AccountId": int(cfg.AccountID),
        "OMSId": 1
    }

    message = {"m": 0,
               "i": 2,
               "n": "CancelAllOrders",
               "o": json.dumps(payload)}
    message = json.dumps(message)
    ws.send(message)


ws = websocket.WebSocketApp(cfg.socketEndpoint, on_open=on_open,
                            on_message=on_message, on_close=on_close)
ws.run_forever()
