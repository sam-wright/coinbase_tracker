# from config import config
from tracker_utils import *


# read_config(config)
# portfolio = Portfolio()

# portfolio.storeJSON(config['portfolio_file'])
# portfolio.loadJSON(config['portfolio_file'])
msg = Message()


'''
Buy proposition?
'''

std_devs = 1.25
transaction_fee = 0.0149

msg += str(datetime.now()) + '\n'
msg += 'Actions evaluated using std_dev = ' + str(std_devs) + '\n'
msg += '\n' + '~'*60 + '\n\n'

btc_instants = read_history(config['btc_history_file'])
eth_instants = read_history(config['eth_history_file'])
ltc_instants = read_history(config['ltc_history_file'])

btc_buy_proposition = buy_proposition(btc_instants, std_devs, msg)
eth_buy_proposition = buy_proposition(eth_instants, std_devs, msg)
ltc_buy_proposition = buy_proposition(ltc_instants, std_devs, msg)

msg += '\n' + '~'*60 + '\n\n'

btc_sell_proposition = sell_proposition(btc_instants, msg)
eth_sell_proposition = sell_proposition(eth_instants, msg)
ltc_sell_proposition = sell_proposition(ltc_instants, msg)

msg += '\n' + '~'*60 + '\n\n'

total_value = 0
total_value += get_currency_amount('BTC')
total_value += get_currency_amount('LTC')
total_value += get_currency_amount('ETH')
total_value += get_currency_amount('USD')

# Tabulate current net worth
total_sell_price = btc_instants[-1].sell_price+ eth_instants[-1].sell_price + ltc_instants[-1].sell_price

send_notification = False
# Buy when current_price  is below avg - X*std_dev
# As long as the recent slope is favorable (negative)
# Also ensure that your not over exposed on any one currency
if (btc_buy_proposition and
        get_currency_amount('USD') > 15.00 and
        (get_currency_amount('BTC') > total_value) < 0.50):

    msg += 'Purchase Bitcoin @ ' + str(btc_instants[-1].buy_price) + '\n'
    buy_currency(btc_instants[-1], 15.00*(1+transaction_fee))
    send_notification = True

if (eth_buy_proposition and
        get_currency_amount('USD') > 15.00 and
        (get_currency_amount('ETH') > total_value) < 0.50):

    msg += 'Purchase Etherium @ ' + str(eth_instants[-1].buy_price) + '\n'
    buy_currency(eth_instants[-1], 15.00*(1+transaction_fee))
    send_notification = True

if (ltc_buy_proposition and
    get_currency_amount('USD') > 15.00 and
    (get_currency_amount('LTC') > total_value) < 0.50):

    msg += 'Purchase Litecoin @ ' + str(ltc_instants[-1].buy_price) + '\n'
    buy_currency(ltc_instants[-1], 15.00*(1+transaction_fee))
    send_notification = True


'''
Sell Proposition?
'''
if btc_sell_proposition:
    msg += 'Sell  BTC @ (' + str(btc_instants[-1].sell_price) + ')\n'
    sell_currency(btc_instants[-1], get_currency_amount('BTC')*(1-transaction_fee))
    send_notification = True

if eth_sell_proposition:
    msg += 'Sell  ETH @ (' + str(eth_instants[-1].sell_price) + ')\n'
    sell_currency(eth_instants[-1], get_currency_amount('ETH')*(1-transaction_fee))
    send_notification = True

if ltc_sell_proposition:
    msg += 'Sell LTC @ (' + str(ltc_instants[-1].sell_price) + ')\n'
    sell_currency(ltc_instants[-1], get_currency_amount('LTC')*(1-transaction_fee))
    send_notification = True


if send_notification:
    msg.verbose += 'Notification = True\n'
else:
    msg.verbose += 'Notification = False\n'

'''
notify
'''
log(msg)

print(msg.verbose)
if send_notification:
    notify(msg.verbose)
