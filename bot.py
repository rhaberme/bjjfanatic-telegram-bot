import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import time
import bs4
import requests


def update_deals():
    r = requests.get('https://bjjfanatics.com/collections/daily-deals', timeout=5)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    mydivs = soup.find_all("div", {"class": "product-card__name"})
    deals = []
    for div in mydivs:
        deals.append(div.contents[0])
    return deals


def new_deals(old_deals):
    maybe_new_deals = update_deals()
    if old_deals == maybe_new_deals:
        return False
    else:
        return True


PORT = int(os.environ.get('PORT', 443))

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = 'TOKEN'


def start(update, context):
    while True:
        deals = update_deals()
        for deal in deals:
            update.message.reply_text(deal)
        while True:
            if new_deals(deals):
                update.message.reply_text('New Deals!')
                deals = update_deals()
                for deal in deals:
                    update.message.reply_text(deal)
                time.sleep(600)
                break
            time.sleep(180)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='HEROKU-WEBAPP' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
