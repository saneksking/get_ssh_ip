"""
--------------------------------------------------------
Licensed under the terms of the BSD 3-Clause License
(see LICENSE for details).
Copyright © 2024, A.A. Suvorov
All rights reserved.
--------------------------------------------------------
"""
import socket


class SshIpInformer:

    @classmethod
    def get_ssh_ip(cls):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ssh_ip = s.getsockname()[0]
            s.close()
            return ssh_ip
        except Exception as e:
            print(e)
            return None
