#!/usr/bin/python

from telegram import Updater, User
import logging
import shelve
import checker

STORED_FILE = 'strelka_bot_shelve.db'
TOKEN_FILENAME = 'token.lst'

users = {}

# Enable Logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

class CardInfo:
    def __init__(self, card_number):
        self.card_number = card_number

class UserInfo:
    
    def __init__(self, user):
        self.user = user
        self.cards = {}

    def add_card(self, card_number):
        self.cards[card_number] = CardInfo(card_number)

def store_users():
    db = shelve.open(STORED_FILE)
    db['users'] = users
    db.close()

def restore_users():
    db = shelve.open(STORED_FILE)
    if db.has_key('users'):
        global users
        users = db['users']
        logger.info("Successful load users info from file %s" % STORED_FILE)
    else:
        logger.info("Can't get users info from file %s" % STORED_FILE)
    db.close()

def get_description():
    return """/help - Show help
/getcardbalance - Returns balance for specified card
/addcard - Add a card to the list of registered cards
/removecard - Remove a card to the list of registered cards
/getcards - Returns balance for all registered cards"""

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi! Use next commands:\n%s'%(get_description()))

def help(bot, update):
    bot.sendMessage(update.message.chat_id
        , text="Supported commands:\n%s"%(get_description()))

def get_cards(bot, update):
    logger.info("New get_cards message\nFrom: %s\nchat_id: %d\nText: %s" %
                (update.message.from_user,
                 update.message.chat_id,
                 update.message.text))
    telegram_user = update.message.from_user
    if not users.has_key(telegram_user.id) or len(users[telegram_user.id].cards) == 0:
        bot.sendMessage(update.message.chat_id
        , text="There are now saved cards for you. Please use command /addcard CARD_NUMBER")
        return

    user = users[telegram_user.id]
    cards = user.cards
    response = ""
    for card_number in cards.keys():
        balance = checker.get_balance(card_number)
        if len(response) != 0:
            response += '\n'
        response += "Card balance for %s: %.2f"%(card_number, balance)

    bot.sendMessage(update.message.chat_id
        , text=response)

def add_card(bot, update, args):
    logger.info("New add_card message\nFrom: %s\nchat_id: %d\nText: %s" %
                (update.message.from_user,
                 update.message.chat_id,
                 update.message.text))
    if len(args) != 1:
        bot.sendMessage(update.message.chat_id, text="Usage:\n/addcard 1234567890")
        return
    card_number = args[0]
    telegram_user = update.message.from_user
    if not users.has_key(telegram_user.id):
        users[telegram_user.id] = UserInfo(telegram_user)

    user = users[telegram_user.id]
    if not user.cards.has_key(card_number):
        user.add_card(card_number)
        store_users()
        bot.sendMessage(update.message.chat_id, text="Card %s successfully added" % (card_number))
    else:
        bot.sendMessage(update.message.chat_id, text="Card %s already added. Do nothing" % (card_number))

def remove_card(bot, update, args):
    logger.info("New remove_card message\nFrom: %s\nchat_id: %d\nText: %s" %
                (update.message.from_user,
                 update.message.chat_id,
                 update.message.text))
    if len(args) != 1:
        bot.sendMessage(update.message.chat_id, text="Usage:\n/removecard 1234567890")
        return
    card_number = args[0]
    telegram_user = update.message.from_user
    if not users.has_key(telegram_user.id):
        bot.sendMessage(update.message.chat_id, text="There are no cards registered for you")
        return
    user = users[telegram_user.id]
    if user.cards.has_key(card_number):
        user.cards.pop(card_number)
        store_users()
        bot.sendMessage(update.message.chat_id, text="Card %s successfully removed" % (card_number))
    else:
        bot.sendMessage(update.message.chat_id, text="Card %s has not being added. Do nothing" % (card_number))


def get_card_balance(bot, update, args):
    logger.info("New get_card_balance message\nFrom: %s\nchat_id: %d\nText: %s" %
                (update.message.from_user,
                 update.message.chat_id,
                 update.message.text))

    if len(args) != 1:
        bot.sendMessage(update.message.chat_id, text="Usage:\n/getcardbalance 1234567890")
        return

    card_number = args[0]
    balance = checker.get_balance(card_number)

    bot.sendMessage(update.message.chat_id
        , text="Card balance for %s: %.2f"%(card_number, balance))

def read_token():
    f = open(TOKEN_FILENAME)
    token = f.readline().strip()
    f.close()
    return token

def main():
    restore_users()
    # Create the EventHandler and pass it your bot's token.

    token = read_token()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # This is how we add handlers for Telegram messages
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("getcardbalance", get_card_balance)
    dp.addTelegramCommandHandler("addcard", add_card)
    dp.addTelegramCommandHandler("removecard", remove_card)
    dp.addTelegramCommandHandler("getcards", get_cards)


    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()