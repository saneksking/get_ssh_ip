"""
--------------------------------------------------------
Licensed under the terms of the BSD 3-Clause License
(see LICENSE for details).
Copyright © 2024, A.A. Suvorov
All rights reserved.
--------------------------------------------------------
"""
import os
import sys
import time

from utils.bot_commands import SshIpInformer
from utils.messenger import TelegramMessenger
from utils.parser import ConfigParser


class AppManager:
    def __init__(self):
        self.parser = ConfigParser('config.json')
        self.messenger = None
        self.bot_command = SshIpInformer()

    def run(self):
        token = self.parser.get_token()
        if not token:
            self.exit_app(
                message='Token is missing',
            )

        self.messenger = TelegramMessenger(
            token=token,
        )

        admins = self.parser.get_admins()
        if not admins:
            self.exit_app(
                message='Admin is missing',
            )

        local_ip = self.bot_command.get_ssh_ip()
        if local_ip is None:
            self.exit_app(
                message='Local IP is missing',
            )

        print('Waiting 30sec ...')
        time.sleep(30)
        user_login = os.getlogin()
        local_ip_info = f"Local IP: {local_ip}"
        user_info = f"User: {user_login}"
        command_info = f"Command: ssh {user_login}@{local_ip}"

        message = f"{user_info}\n{local_ip_info}\n{command_info}"

        for admin in admins:
            self.messenger.send_message(admin, message)
            print(f"Message send to {self.mask_admin_chat_id(admin)} [OK]")

    @staticmethod
    def mask_admin_chat_id(chat_id):
        if len(chat_id) > 4:
            masked_admin = chat_id[:2] + '*' * (len(chat_id) - 4) + chat_id[-2:]
        else:
            masked_admin = chat_id
        return masked_admin

    @staticmethod
    def exit_app(message):
        print(message)
        sys.exit(0)
