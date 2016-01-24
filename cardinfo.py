#!/usr/bin/python

import checker
import logging

logger = logging.getLogger(__name__)

class CardInfo:
    def __init__(self, card_number):
        self.card_number = card_number
        self.threshold = None
        self.json = checker.get_status(self.card_number)
        self._int_update_by_json(self.json)

    def __str__(self):
        return "Card(%s, balance: %s, threshold: %s" % (self.card_number, self.balance, self.threshold)

    def _int_update_by_json(self, json):
        self.last_updated = time()
        self.balance = json['balance']/100.
        self.cardblocked = json['cardblocked']

    def update(self):
        if time() < self.last_updated + UPDATE_TIMEOUT:
            logger.info("Can't update card %s now. Next update not earlier than at %s"
                        % (self.card_number, ctime(self.last_updated + UPDATE_TIMEOUT)))
            return False
        self.json = checker.get_status(self.card_number)
        self._int_update_by_json(self.json)

    def check_threshold_valid(self):
        if not self.threshold:
            logger.warn("Threshold is not specified for card %s" % self)
            return True
        return self.balance > self.threshold