"""
Test file
used model:  requests,Thread
"""

import requests
from threading import Thread

url = 'http://127.0.0.1:5000/'


def get_product(product_id):
    """
    A query about a product returns the correct product attributes
    """
    url_ = url + 'query'
    resp = requests.get(url_, params={'id': product_id})
    print(resp.json())


def buy_success(product_id):
    """
    Buying a product with sufficient stock in the server succeeds and the quantity in stock is updated
    :return:
    """
    url_ = url + 'buy'
    resp = requests.get(url_, params={'id': product_id, "count": 10, 'credit_card': '5142514458415635'})
    print(resp.json())


def buy_failed(product_id):
    """
    Buying a product with insufficient stock in the server fails and the quantity in stock remains unchanged
    :return:
    """
    url_ = url + 'buy'
    resp = requests.get(url_, params={'id': product_id, "count": 10000, 'credit_card': '5142514458415635'})
    print(resp.json())


def replenish(product_id):
    """
    Replenishing a product updates the server’s quantity in stock
    :return:
    """
    url_ = url + 'replenish'
    resp = requests.get(url_, params={'id': product_id, "count": 10000, 'credit_card': '5142514458415635'})
    print(resp.json())


def query_failed(product_id):
    """
    When the product ID does not exist, the server returns the 404 status code
    :return:
    """
    url_ = url + 'query'
    resp = requests.get(url_, params={'id': product_id})
    print(resp.json())


def params_missed(product_id):
    """
    When some required input data are missing or invalid, the server returns the 400 status code
    :return:
    """
    url_ = url + 'buy'
    resp = requests.get(url_, params={'id': product_id})
    print(resp.json())


def query(product_id):
    """
    If two requests for buying the same product arrive almost simultaneously and
    the quantity in stock is insufficient for the second request, the server must not
    mistakenly fulfill the second request.
    :param product_id:
    :return:
    """
    url_ = url + 'buy'

    def get_data(count):
        resp = requests.get(url_,  params={'id': product_id, "count": count, 'credit_card': '5142514458415635'})
        print(resp.json())

    for i in range(1, 3):
        Thread(target=get_data, args=(22*i,)).start()


if __name__ == '__main__':
    query(1)
