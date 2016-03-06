# Strelka bot
This is a Telegram bot which is able to get information about balance of card 'Strelka' (http://strelkacard.ru/).

# Requirements

* [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot/)
* [`requests`](https://github.com/kennethreitz/requests)

# Setup

Create file `token.lst` with your bot's token.

# Running

```
python strelka_bot.py
```

# Supported commands

* `/help` -- Show help
* `/getcardbalance` -- Returns balance for specified card
* `/addcard` -- Add a card to the list of registered cards
* `/removecard` -- Remove a card to the list of registered cards
* `/getcards` -- Returns balance for all registered cards
* `/setthreshold` -- Set threshold value for card(s)