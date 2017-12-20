from tracker_utils import *

from coinbase.wallet.client import Client
import os.path

pwd = os.path.dirname(os.path.abspath(__file__))

client = Client(config['api_key'], config['api_secret'])

btc_filename = pwd + config['btc_history_file']
eth_filename = pwd + config['eth_history_file']
ltc_filename = pwd + config['ltc_history_file']

btc_buy = client.buy(config['btc_wallet'],
                     amount=1.0000,
                     currency='BTC',
                     quote='true')

eth_buy = client.buy(config['eth_wallet'],
                     amount=1.0000,
                     currency='ETH',
                     quote='true')

ltc_buy = client.buy(config['ltc_wallet'],
                     amount=1.0000,
                     currency='LTC',
                     quote='true')

btc_sell = client.sell(config['btc_wallet'],
                       amount=1.0000,
                       currency='BTC',
                       quote='true')

eth_sell = client.sell(config['eth_wallet'],
                       amount=1.0000,
                       currency='ETH',
                       quote='true')

ltc_sell = client.sell(config['eth_wallet'],
                       amount=1.0000,
                       currency='LTC',
                       quote='true')

btc_instant = Instant(btc_buy['subtotal']['amount'], btc_sell['subtotal']['amount'], btc_buy['amount']['currency'],
                      datetime.now())
eth_instant = Instant(eth_buy['subtotal']['amount'], eth_sell['subtotal']['amount'], eth_buy['amount']['currency'],
                      datetime.now())
ltc_instant = Instant(ltc_buy['subtotal']['amount'], ltc_sell['subtotal']['amount'], ltc_buy['amount']['currency'],
                      datetime.now())

instants = [btc_instant, eth_instant, ltc_instant]
filenames = [btc_filename, eth_filename, ltc_filename]

for i in range(len(instants)):

    instant = instants[i]
    filename = filenames[i]

    if os.path.exists(filename):
        new_history = False
    else:
        new_history = True

    with open(filename, 'a+', encoding='utf-8') as f:
        if not new_history:
            f.write(',\n')
        instant.write_file(f)
