import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import socketserver

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import random
import http.client

ip_list = set()

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if '/register' in self.path:
            print("I was called")
            query_components = parse_qs(urlparse(self.path).query)
            ip_list.add(query_components["ip"][0])
            print("ip's: ", ip_list)
            self.send_response_only(200)
            self.wfile.write('Hello World'.encode())

PORT = 6060

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    value = update.message.text
    if value == "1":
        update.message.reply_text("Alan mifrestam dawsh")
    elif value == "2":
        random_ip = random.sample(ip_list, k=1)
        connection = http.client.HTTPConnection(random_ip[0])
        result = connection.request("GET", "/daemon")
        print(result)
        update.message.reply_text(result)
    else:
        update.message.reply_text("You've Entered a wrong value")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5930875085:AAHwLEBMYuB5-jTJjQBa8pxC_ihi6d8sg6U")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    with socketserver.TCPServer(("", PORT), GetHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()


if __name__ == '__main__':
    main()
