#!/usr/bin/python

from cardinfo import CardInfo

class UserInfo:
    def __init__(self, user):
        self.user = user
        self.cards = {}

    def add_card(self, card_number):
        card = CardInfo(card_number)
        if card.cardblocked:
            return False
        self.cards[card_number] = CardInfo(card_number)
        return True
