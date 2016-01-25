#!/usr/bin/python

import checker
import logging
from time import time, ctime

UPDATE_TIMEOUT = 10. * 60 * 1000 #10 min

logger = logging.getLogger(__name__)

class CardInfo:
    def __init__(self, card_number):
        self.card_number = card_number
        self.threshold = None
        self.listener = None
        self.prev_balance = None
        self.json = checker.get_status(self.card_number)
        self._int_update_by_json(self.json)

    def __str__(self):
        return "Card(%s, balance: %s, threshold: %s)" % (self.card_number, self.balance, self.threshold)

    def _int_update_by_json(self, json):
        self.last_updated = time()
        self.balance = json['balance']/100.
        self.cardblocked = json['cardblocked']

    def set_threshold(self, threshold):
        if threshold and threshold.isdigit():
            self.threshold = int(threshold)
        else:
            raise ValueError("Threshold should be integer")

    def set_value_changed_listener(self, listener):
        if listener.__class__ != ThresholdExceedListener:
            raise ValueError("Can't set %s as listener" % listener)
        self.listener = listener

    def update(self):
        if time() < self.last_updated + UPDATE_TIMEOUT:
            logger.info("Can't update card %s now. Next update not earlier than at %s"
                        % (self.card_number, ctime(self.last_updated + UPDATE_TIMEOUT)))
            return False
        logger.info("Updating card %s" % self.card_number)
        self.json = checker.get_status(self.card_number)
        self.prev_balance = self.balance
        self._int_update_by_json(self.json)
        self.notify_listeners_on_change()
        return True

    def notify_listeners_on_change(self):
        if not self.listener or not self.prev_balance:
            return
        if self.balance != self.prev_balance:
            self.listener.notify(self)

    def check_threshold_valid(self):
        if not self.threshold:
            self.threshold = None
            logger.warn("Threshold is not specified for card %s" % self)
            return True
        logger.info("Balance: %s, threshold: %s" % (self.balance, self.threshold))
        return self.balance > int(self.threshold)

class ThresholdExceedListener:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def notify(self, card):
        if not card.threshold:
            logger.warn("Listener notified for card %s without threshold")
            return
        if card.balance < card.threshold:
            self.bot.sendMessage(self.chat_id, text="Threshold has been exceeded for card %s." % card)
