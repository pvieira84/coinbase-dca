import os
import http.client
import json
import sys
import time
import uuid
import math
import re
import jwt
from cryptography.hazmat.primitives import serialization
import secrets
from enum import Enum

request_host = os.environ.get("COINBASE_HOST", "api.coinbase.com")
key_name = os.environ.get("COINBASE_KEY_NAME")
key_secret = os.environ.get("COINBASE_KEY_SECRET")
if key_secret != None:
    key_secret = key_secret.replace( '\\n' , '\n' )

def build_jwt(uri):
    private_key_bytes = key_secret.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    jwt_payload = {
        'sub': key_name,
        'iss': "cdp",
        'nbf': int(time.time()),
        'exp': int(time.time()) + 120,
        'uri': uri,
    }
    jwt_token = jwt.encode(
        jwt_payload,
        private_key,
        algorithm='ES256',
        headers={'kid': key_name, 'nonce': secrets.token_hex()},
    )
    return jwt_token

class Side(Enum):
    BUY = 1
    SELL = 0

class Method(Enum):
    POST = 1
    GET = 0

def generate_client_order_id():
    return uuid.uuid4()

def coinbase_request(method, path, body):
    conn = http.client.HTTPSConnection(request_host)
    uri = f"{method} {request_host}{path}"
    jwt_token = build_jwt(uri)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }

    conn.request(method, path, body, headers)
    res = conn.getresponse()
    data = res.read()

    # Check for Unauthorized status code (401)
    if res.status == 401:
        print("Error: Unauthorized. Please check your API key and secret.")
        return None

    try:
        response_data = json.loads(data.decode("utf-8"))
        print(json.dumps(response_data, indent=2))
        return response_data
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response. Raw response data:", data)
        return None

def placeLimitOrder(side, pair, size, limit_price):
    method = Method.POST.name
    path = '/api/v3/brokerage/orders'
    payload = json.dumps({
        "client_order_id": str(generate_client_order_id()),
        "side": side,
        "product_id": pair,
        "order_configuration": {
            "limit_limit_gtc": {
                "post_only": False,
                "limit_price": limit_price,
                "base_size": size
            }
        }
    })

    coinbase_request(method, path, payload)

def placeMarketOrder(side, pair, size):
    method = Method.POST.name
    path = '/api/v3/brokerage/orders'
    payload = json.dumps({
        "client_order_id": str(generate_client_order_id()),
        "side": side,
        "product_id": pair,
        "order_configuration": {
            "market_market_ioc": {
                "quote_size": size
            }
        }
    })

    coinbase_request(method, path, payload)

def getAllProductInfo():
    method = Method.GET.name
    path = '/api/v3/brokerage/products'
    payload = ''
    response = coinbase_request(method, path, payload)
    for product in response['products']:
        print(product['product_id'])


def getProductInfo(pair):
    method = Method.GET.name
    path = f'/api/v3/brokerage/products/{pair}'
    payload = ''
    response = coinbase_request(method, path, payload)
    
    if response is None:
        return None

    return {"price": response['price'],
            "quote_increment": response['quote_increment'],
            "base_increment": response['base_increment']}

def coinbase_dca():
    my_side = Side.BUY.name
    my_trading_pair = os.environ.get("TRADING_PAIR", "BTC-EUR")
    order_size = float(os.environ.get("ORDER_SIZE", "50"))
    factor = .999 if my_side == Side.BUY.name else 1.001

    print(f'Getting product info for {my_trading_pair}')
    product_info = getProductInfo(my_trading_pair)
    
    if product_info is None:
        print("Error: Unable to fetch product information.")
        return

    quote_currency_price_increment = abs(round(math.log(float(product_info['quote_increment']), 10)))
    base_currency_price_increment = abs(round(math.log(float(product_info['base_increment']), 10)))

    my_limit_price = str(round(float(product_info['price']) * factor, quote_currency_price_increment))
    my_order_size = str(round(order_size / float(my_limit_price), base_currency_price_increment))

    print(f'Placing a limit order for {my_trading_pair} with amount {order_size}')
    placeLimitOrder(my_side, my_trading_pair, my_order_size, my_limit_price)
    #placeMarketOrder(my_side, my_trading_pair, str(order_size))

    print(f'The spot price of {my_trading_pair} is €{product_info["price"]}')

if __name__ == '__main__':
    if key_name == None or key_secret == None:
        print("Error: Missing coinbase credentials.")
    else:
        coinbase_dca()