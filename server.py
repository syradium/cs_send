from argparse import ArgumentParser
from collections import ChainMap
import logging
import os
import socket


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_server_settings():
    defaults = {'port': 1234, 'dest_file': 'data.jpg', 'buffer': 1024}

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-d', '--dest_file')
    parser.add_argument('--buffer', type=int)
    args = parser.parse_args()

    cmd_args = {k: v for k, v in vars(args).items() if v}

    return ChainMap(cmd_args, defaults)


def initialize_connection(port):
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, port))
    return s

settings = get_server_settings()
s = initialize_connection(settings['port'])
s.listen(5)

while True:
    logger.debug('Ready for connections')
    c, client_ip = s.accept()
    logger.debug('Got connection from {}'.format(client_ip))
    buf = c.recv(settings['buffer'])
    logger.debug('Receiving...')

    try:
        with open(settings['dest_file'], 'wb') as f:
            while buf:
                logger.debug('Receiving...')
                f.write(buf)
                buf = c.recv(settings['buffer'])
    except (OSError, InterruptedError):
        logger.exception('An error occuried during transmission')
        os.unlink(settings['dest_file'])

    print('Done Receiving')
    c.close()
