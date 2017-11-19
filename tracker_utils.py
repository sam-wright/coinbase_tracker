import re
from datetime import datetime
from datetime import timedelta
from math import exp

import os.path
import smtplib
import json

from config import config
from coinbase.wallet.client import Client


def read_config(config):
    """
    :param config:
    :return:
    """
    for c in config:
        print('{' + c + '\t' + config[c] + '}')
    print('\n')


class Instant:
    """
    Class Instant

    Manages marketplace snapshot

    BTC_MARKET = [BTC_INSTANT_1, BTC_INSTANT_2, ...

    """
    buy_price = 0
    sell_price = 0
    market = ''
    date = datetime.now()

    def __init__(self, buy_price, sell_price, currency, date):
        self.market = currency
        self.buy_price = float(buy_price)
        self.sell_price = float(sell_price)
        self.date = date

    def write_file(self, filename):
        """
        :param filename:
        :return:
        """
        self.date = str(self.date)
        return json.dump(self, filename, default=lambda o: o.__dict__, sort_keys=True, indent=0)

class Message:
    """

    """
    def __init__(self):
        self.standard = str()
        self.verbose = str()



    def __str__(self, val):
        msg = Message()
        msg.verbose = val
        msg.standard = val

        return(msg)

    def __add__(self, val):
        self.standard += val
        self.verbose += val

        return(self)

    def __eq__(self, val):
        self.standard = val
        self.verbose = val

class Market:
    """
    class Market

    Creates list of market instants

    """
    market_JSON_file = ''

    def __init__(self):
        pass


class Portfolio:
    """
    Class Portfolio

    Manages currency
    """
    btc_avg_price = 0.0
    eth_avg_price = 0.0
    ltc_avg_price = 0.0
    last_btc_transaction = datetime.now()
    last_eth_transaction = datetime.now()
    last_ltc_transaction = datetime.now()

    def __init__(self):
        self.btc_avg_price = 0.0
        self.eth_avg_price = 0.0
        self.ltc_avg_price = 0.0
        self.last_btc_transaction = datetime.now()
        self.last_eth_transaction = datetime.now()
        self.last_ltc_transaction = datetime.now()

    def write_file(self, filename):
        """
        :param filename:
        :return:
        """

        self.last_btc_transaction = str(self.last_btc_transaction)
        self.last_eth_transaction = str(self.last_eth_transaction)
        self.last_ltc_transaction = str(self.last_ltc_transaction)

        pwd = os.path.dirname(os.path.abspath(__file__))

        with open(pwd + filename, 'w', encoding='utf-8') as f:
            return json.dump(self, f, default=lambda o: o.__dict__, sort_keys=True, indent=0)

    def read_file(self, filename):
        """
        :param filename:
        :return:
        """

        pwd = os.path.dirname(os.path.abspath(__file__))

        try:
            with open(pwd + filename, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

                self.btc_avg_price = float(raw_data['btc_avg_price'])
                self.eth_avg_price = float(raw_data['eth_avg_price'])
                self.ltc_avg_price = float(raw_data['ltc_avg_price'])
                self.last_btc_transaction = datetime.strptime(raw_data['last_btc_transaction'], '%Y-%m-%d %H:%M:%S.%f')
                self.last_eth_transaction = datetime.strptime(raw_data['last_eth_transaction'], '%Y-%m-%d %H:%M:%S.%f')
                self.last_ltc_transaction = datetime.strptime(raw_data['last_ltc_transaction'], '%Y-%m-%d %H:%M:%S.%f')
        except:
            print("Error reading in Portfolio.json file!")


def read_history(filename):
    """
    :param filename:
    :return:
    """

    instants = []
    pwd = os.path.dirname(os.path.abspath(__file__))
    with open(pwd + filename, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    raw_data = '[' + raw_data + ']'

    decoded_data = json.loads(raw_data, encoding='utf-8')

    for d in decoded_data:
        instants.append(
            Instant(d['buy_price'],
                    d['sell_price'],
                    d['market'],
                    datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S.%f')))

    return instants


def get_currency_amount(currency):
    """
    :param currency:
    :return:
    """

    client = Client(config['api_key'], config['api_secret'])

    if currency == "BTC":
        account = client.get_account(config["btc_wallet"])
    elif currency == "ETH":
        account = client.get_account(config["eth_wallet"])
    elif currency == "LTC":
        account = client.get_account(config["ltc_wallet"])
    elif currency == "USD":
        account = client.get_account(config["usd_wallet"])


    money = re.search(r'\d+.\d+', str(account["native_balance"]))
    return float(money.group(0))


def sell_currency(instant, _amount):

    client = Client(config['api_key'], config['api_secret'])

    if instant.market == "BTC":
        client.sell(config['btc_wallet'],
                    amount=_amount,
                    currency="USD",
                    payment_method=config['usd_fiat'])

    elif instant.market == "ETH":
        client.sell(config['eth_wallet'],
                    amount=_amount,
                    currency="USD",
                    payment_method=config['usd_fiat'])

    elif instant.market == "LTC":
        client.sell(config['ltc_wallet'],
                    amount=_amount,
                    currency="USD",
                    payment_method=config['usd_fiat'])


def buy_currency(instant, _amount):
    client = Client(config['api_key'], config['api_secret'])

    portfolio = Portfolio()
    portfolio.read_file(config['portfolio_file'])

    old_val = get_currency_amount(instant.market)

    if instant.market == "BTC":
        portfolio.btc_avg_price = (portfolio.btc_avg_price*old_val + instant.buy_price*_amount)/(old_val+_amount)
        portfolio.last_btc_transaction = datetime.now()

        client.buy(config['btc_wallet'],
                   amount=_amount,
                   currency="USD",
                   payment_method=config['usd_fiat'])

    elif instant.market == "ETH":
        portfolio.eth_avg_price = (portfolio.eth_avg_price*old_val + instant.buy_price*_amount)/(old_val+_amount)
        portfolio.last_eth_transaction = datetime.now()

        client.buy(config['eth_wallet'],
                   amount=_amount,
                   currency="USD",
                   payment_method=config['usd_fiat'])

    elif instant.market == "LTC":
        portfolio.ltc_avg_price = (portfolio.ltc_avg_price*old_val + instant.buy_price*_amount)/(old_val+_amount)
        portfolio.last_ltc_transaction = datetime.now()

        client.buy(config['ltc_wallet'],
                   amount=_amount,
                   currency="USD",
                   payment_method=config['usd_fiat'])

    portfolio.write_file(config['portfolio_file'])



def limit_date_range(instants, delta):
    """
    :param instants:
    :param delta:
    :return:
    """

    valid_instants = []

    for i in instants:
        if (datetime.now()-i.date) < delta:
            valid_instants.append(i)

    return valid_instants


def evaluate_date_range(instants, delta):
    """
    :param instants:
    :param delta:
    :return:
    """

    valid_instants = limit_date_range(instants, delta)

    dc_buy = list(range(len(valid_instants)))
    dc_buy_ = list(range(len(valid_instants)))
    dc_buy_[0] = 0
    alpha = 0.7
    for i in range(1, len(valid_instants)):
        dt = (valid_instants[i].date - valid_instants[i-1].date).total_seconds()
        dc_buy[i] = float(valid_instants[i].buy_price) - float(valid_instants[i-1].buy_price)
        dc_buy_[i] = alpha * dc_buy[i] + (1-alpha) * dc_buy_[i-1]

        print('[%s]\t%s\t%s\t%s\t%s' %
              (i, valid_instants[i].date, valid_instants[i].buy_price, dc_buy[i]/dt, dc_buy_[i] / dt))


def buy_proposition(instants, n, msg):
    """

    :param instants:
    :param n:
    :return:
    """

    valid_instants = limit_date_range(instants, timedelta(weeks=1))

    price_average = 0.0
    for inst in valid_instants:
        price_average += float(inst.buy_price)
    price_average /= len(valid_instants)
    price_current = float(valid_instants[-1].buy_price)

    stdev = 0
    for i in range(len(valid_instants)):
        stdev += (float(valid_instants[i].buy_price) - price_average)**2
    stdev /= len(valid_instants)
    stdev = stdev**0.5

    msg.verbose += '[' + instants[-1].market + ']\t' + str(valid_instants[-1].buy_price) + '\t Buy threshold: ' + str(price_average - n * stdev) + '\t'
    msg += str(price_current < price_average - n * stdev) + '\n'

    return price_current < price_average - n * stdev


def sell_proposition(instants, msg):
    """
    Coinbase sell fees:
        U.S. Bank Account           1.49%, with a $0.15 minimum
        Coinbase USD Wallet     1.49%
        Credit/Debit Card           3.99%

    :param instants:
    :return:
    """

    portfolio = Portfolio()
    portfolio.read_file(config['portfolio_file'])

    '''
    Update sell threshold
    '''
    sell_point = 0
    if instants[-1].market == 'BTC':
        dt = (datetime.now() - portfolio.last_btc_transaction).total_seconds() / 60 / 60
        avg_price = portfolio.btc_avg_price

    elif instants[-1].market == 'ETH':
        dt = (datetime.now() - portfolio.last_eth_transaction).total_seconds() / 60 / 60
        avg_price = portfolio.eth_avg_price

    elif instants[-1].market == 'LTC':
        dt = (datetime.now() - portfolio.last_ltc_transaction).total_seconds() / 60 / 60
        avg_price = portfolio.ltc_avg_price

    sell_point = avg_price * 1.2 + 0.8 * exp(-dt / 10) * avg_price
    msg.verbose += '[' + instants[-1].market + ']\t' + str(instants[-1].buy_price) + '\t Sell threshold: ' + str(sell_point) + '\t'
    msg += str(sell_point < instants[-1].sell_price) + '\n'

    '''
    Save portfolio
    '''
    # portfolio.write_file(config['portfolio_file'])


    if instants[-1].market == 'BTC' and get_currency_amount('BTC') > 1.50:
        return sell_point < instants[-1].sell_price

    elif instants[-1].market == 'ETH' and get_currency_amount('ETH') > 1.50:
        return sell_point < instants[-1].sell_price

    elif instants[-1].market == 'LTC' and get_currency_amount('LTC') > 1.50:
        return sell_point < instants[-1].sell_price

    return False


def notify(message):
    """
    :param message:
    :return:
    """

    server = smtplib.SMTP(config['email_server'])
    server.starttls()
    server.login(config['email_username'], config['email_password'])
    server.sendmail(config['email_from'], config['email_to'], message)


def log(message):
    """
    :param message:
    :return:
    """

    pwd = os.path.dirname(os.path.abspath(__file__))
    with open(pwd + config['log_file'], 'w')as f:
        f.write(message.verbose)
