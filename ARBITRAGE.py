'''
This strategy works by find arbitrage profit among 3 cycling trading pairs and execute
1. keep observing 3 trading paris depth
2. each time depth updates, calculate potential profit
3. As soon as it meets profit threshold, execute 3 market trades
However, it just doesn't profit
'''
from __future__ import print_function
import json
import threading
import time

from binance.client import Client
from binance.depthcache import DepthCacheManager
from binance.enums import *
from ACCOUNTS import accounts
from dudubinance.clientfactory import clientFactory

mylock = threading.Lock()
client = clientFactory(accounts)


DCs={}
DCs['BNBETH'] = DCMs['BNBETH'].get_depth_cache();
DCs['BNBBTC'] = DCMs['BNBBTC'].get_depth_cache();
DCs['ETHBTC'] = DCMs['ETHBTC'].get_depth_cache();

isTrading = False
def process_any_depth(depth_cache):

    global isTrading
    if(isTrading):
        return

    global DCs
    global client
    BNBETH_bids = DCs['BNBETH'].get_bids()
    BNBETH_asks = DCs['BNBETH'].get_asks()
    BNBBTC_bids = DCs['BNBBTC'].get_bids()
    BNBBTC_asks = DCs['BNBBTC'].get_asks()
    ETHBTC_bids = DCs['ETHBTC'].get_bids()
    ETHBTC_asks = DCs['ETHBTC'].get_asks()

    if(len(BNBETH_bids)==0 or len(BNBETH_asks)==0 or len(BNBBTC_bids)==0 or len(BNBBTC_asks)==0 or len(ETHBTC_bids)==0 or len(ETHBTC_asks)==0 ):
        return

    BNBETH_bestbid = BNBETH_bids[0]
    BNBETH_bestask = BNBETH_asks[0]
    BNBBTC_bestbid = BNBBTC_bids[0]
    BNBBTC_bestask = BNBBTC_asks[0]
    ETHBTC_bestbid = ETHBTC_bids[0]
    ETHBTC_bestask = ETHBTC_asks[0]

    
    #BNB->ETH->BTC->BNB
    BEBRatio = float(BNBETH_bestbid[0]) * float(ETHBTC_bestbid[0]) /float(BNBBTC_bestask[0]) - 1 - 0.0015
    BEBCapacity = int(min(float(BNBETH_bestbid[1]), float(ETHBTC_bestbid[1]) / float(BNBETH_bestbid[0]),float(BNBBTC_bestask[1])))

    #BNB->BTC->ETH->BNB
    BBERatio = float(BNBBTC_bestbid[0])  /float(ETHBTC_bestask[0]) /float(BNBETH_bestask[0]) - 1 - 0.0015
    BBECapacity = int(min(float(BNBETH_bestask[1]), float(ETHBTC_bestask[1]) / float(BNBETH_bestask[0]),float(BNBBTC_bestbid[1])))

    #BNB->ETH->BTC->BNB
    if(BEBRatio>0.001):
        isTrading=True
        print("{}\tBNB->ETH->BTC->BNB Ratio:{},\tQuantity:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , BEBRatio,BEBCapacity))
        
        #sell BNB to ETH###########################################################
        '''
        bnb2ethorder = client.order_market_sell(
            symbol='BNBETH',
            quantity=BEBCapacity,
            disable_validation=True,
            newOrderRespType='FULL'
            )
        print(json.dumps(bnb2ethorder, indent=4, sort_keys=True))
        ETHAmount = float(0)
        for fill in bnb2ethorder['fills']:
            ETHAmount += (float(fill['qty']) * float(fill['price']))
            if fill['commissionAsset'] == "ETH":
                ETHAmount -= float(fill['commission'])
        print("Sell {} BNB into {} ETH".format(BEBCapacity, ETHAmount))

        #sell ETH to BTC###########################################################
        eth2btcorder = client.order_market_sell(
            symbol='ETHBTC',
            quantity=format(ETHAmount,".3f"),
            disable_validation=True,
            newOrderRespType='FULL'
            )
        print(json.dumps(eth2btcorder, indent=4, sort_keys=True))
        BTCAmount = float(0)
        for fill in eth2btcorder['fills']:
            BTCAmount+=(float(fill['qty']) * float(fill['price']))
            if fill['commissionAsset'] == "BTC":
                BTCAmount -= float(fill['commission'])
        print("Sell {} ETH into {} BTC".format(ETHAmount, BTCAmount))

        #buy BTC to BNB

        #calculate proper buy amount###########################################################
        Buy_BNBAmount = 0
        Sell_BTCAmount = BTCAmount
        asks = DCs['BNBBTC'].get_asks()
        for ask in asks:
            cost = float(ask[0]) * float(ask[1])
            if Sell_BTCAmount < cost:
                Buy_BNBAmount += (Sell_BTCAmount/float(ask[0]))
                Sell_BTCAmount = 0
                break
            else:
                Sell_BTCAmount -=cost
                Buy_BNBAmount += ask[1]
                

        btc2bnborder = client.order_market_buy(
            symbol='BNBBTC',
            quantity=int(Buy_BNBAmount),
            disable_validation=True,
            newOrderRespType='FULL'
            )
        print(json.dumps(btc2bnborder, indent=4, sort_keys=True))
        BNBAmount = float(0)
        for fill in btc2bnborder['fills']:
            BNBAmount+=float(fill['qty'])
            if fill['commissionAsset'] == "BNB" :
                BNBAmount -= float(fill['commission'])
        print("Buy {} BTC into {} BNB".format(BTCAmount, BNBAmount))

        time.sleep(1)
        isTrading=False
        '''
    else:
        print("{}\tBNB->ETH->BTC->BNB Ratio:{},\tNot Good Enough".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , BEBRatio))

    #BNB->BTC->ETH->BNB
    if(BBERatio>0.001):
        isTrading=True
        print("{}\tBNB->BTC->ETH->BNB Ratio:{},\tQuantity:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , BBERatio,BBECapacity))
        
        #sell BNB to BTC###########################################################
        '''
        bnb2btcorder = client.order_market_sell(
            symbol='BNBBTC',
            quantity=BBECapacity,
            disable_validation=True,
            newOrderRespType='FULL'
            )
        print(json.dumps(bnb2btcorder, indent=4, sort_keys=True))
        BTCAmount = float(0)
        for fill in bnb2btcorder['fills']:
            BTCAmount += (float(fill['qty']) * float(fill['price']))
            if fill['commissionAsset'] == "BTC":
                BTCAmount -= float(fill['commission'])
        print("Sell {} BNB into {} BTC".format(BBECapacity, BTCAmount))
        
        #buy BTC to ETH###########################################################

        #calculate proper buy amount
        Buy_ETHAmount = 0
        Sell_BTCAmount = BTCAmount
        asks = DCs['ETHBTC'].get_asks()
        for ask in asks:
            cost = float(ask[0]) * float(ask[1])
            if Sell_BTCAmount < cost:
                Buy_ETHAmount += (Sell_BTCAmount/float(ask[0]))
                Sell_BTCAmount = 0
                break
            else:
                Sell_BTCAmount -=cost
                Buy_ETHAmount += ask[1]
                
        btc2ethorder = client.order_market_buy(
            symbol='ETHBTC',
            quantity=format(Buy_ETHAmount,".3f"),
            disable_validation=True,
            newOrderRespType='FULL'
            )
        print(json.dumps(btc2ethorder, indent=4, sort_keys=True))
        ETHAmount = float(0)
        for fill in btc2ethorder['fills']:
            ETHAmount+=float(fill['qty'])
            if fill['commissionAsset'] == "ETH" :
                ETHAmount -= float(fill['commission'])
        print("Buy {} BTC into {} ETH".format(BTCAmount, ETHAmount))


        #buy ETH to BNB###########################################################

        #calculate proper buy amount
        Buy_BNBAmount = 0
        Sell_ETHAmount = ETHAmount
        asks = DCs['BNBETH'].get_asks()
        for ask in asks:
            cost = float(ask[0]) * float(ask[1])
            if Sell_ETHAmount < cost:
                Buy_BNBAmount += (Sell_ETHAmount/float(ask[0]))
                Sell_ETHAmount = 0
                break
            else:
                Sell_ETHAmount -=cost
                Buy_BNBAmount += ask[1]
                
        eth2bnborder = client.order_market_buy(
            symbol='BNBETH',
            quantity=int(Buy_BNBAmount),
            disable_validation=True,
            newOrderRespType='FULL'
            )
        print(json.dumps(eth2bnborder, indent=4, sort_keys=True))
        BNBAmount = float(0)
        for fill in eth2bnborder['fills']:
            BNBAmount+=float(fill['qty'])
            if fill['commissionAsset'] == "BNB" :
                BNBAmount -= float(fill['commission'])
        print("Buy {} ETH into {} BNB".format(ETHAmount, BNBAmount))
        time.sleep(10)
        isTrading=False
        '''
    else:
        print("{}\tBNB->BTC->ETH->BNB Ratio:{},\tNot Good Enough".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , BBERatio))

# Set up watched depth cache
DCMs={}
DCMs['BNBBTC'] = DepthCacheManager(client,'BNBBTC',process_any_depth);
DCMs['BNBETH'] = DepthCacheManager(client,'BNBETH',process_any_depth);
DCMs['ETHBTC'] = DepthCacheManager(client,'ETHBTC',process_any_depth);






#something about user socket
'''
#handler of account update event
def process_usersocket_message(msg):
    if(msg['e'] == "outboundAccountInfo"):
        #print("message type:" + msg['e'])
        #print(msg)
        print(json.dumps(msg, indent=4, sort_keys=True))
    
    
from binance.websockets import BinanceSocketManager
bm1 = BinanceSocketManager(client)
bm1.start_user_socket()
bm1.start()
'''

