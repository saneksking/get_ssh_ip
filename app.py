"""
--------------------------------------------------------
Licensed under the terms of the BSD 3-Clause License
(see LICENSE for details).
Copyright © 2024, A.A. Suvorov
All rights reserved.
--------------------------------------------------------
"""
import socket
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    login = os.getenv('LOGIN')
    bot.reply_to(message, f'Server local IP-address: {local_ip};\n'
                          f'Command: ssh {login}@{local_ip}')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
