#!/usr/bin/python
import logging
import requests

CARD_TYPE_ID = '3ae427a1-0f17-4524-acb1-a3f50090a8f3'

logger = logging.getLogger(__name__)

def get_status(card_number):
    payload = {'cardnum':card_number, 'cardtypeid': CARD_TYPE_ID}
    r = requests.get('http://strelkacard.ru/api/cards/status/', params=payload)
    logging.info("Get info for card %s: %d %s" % (card_number, r.status_code, r.text))
    if r.status_code == requests.codes.ok:
        return r.json()
    return None

def get_balance(card_number):
    r = get_status(card_number)
    return r['balance']/100.
