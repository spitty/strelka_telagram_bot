#!/usr/bin/python
import logging
import requests

# suppress warnings about insecure request (https://stackoverflow.com/a/28002687/954275)
import requests.packages.urllib3 as urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CARD_TYPE_ID = '3ae427a1-0f17-4524-acb1-a3f50090a8f3'

logger = logging.getLogger(__name__)

def get_status(card_number):
    payload = {'cardnum':card_number, 'cardtypeid': CARD_TYPE_ID}
    # We don't care about request security here
    r = requests.get('http://strelkacard.ru/api/cards/status/', params=payload, verify=False)
    logger.info("Get info for card %s: %d %s" % (card_number, r.status_code, r.text))
    if r.status_code == requests.codes.ok:
        return r.json()
    raise ValueError("Can't get info about card with number %s" % card_number)

def get_balance(card_number):
    r = get_status(card_number)
    return r['balance']/100.
