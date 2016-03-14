from argparse import ArgumentParser
import logging
import socket


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_client_settings():
    parser = ArgumentParser()
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--file', type=str)
    parser.add_argument('--buffer', type=int)
    return parser.parse_args()


settings = get_client_settings()

s = socket.socket()
s.connect((settings.host, settings.port))
logger.debug('Sending...')


with open(settings.file, 'rb') as f:
    buf = f.read(settings.buffer)
    while buf:
        logger.debug('Sending...')
        s.send(buf)
        buf = f.read(settings.buffer)


logger.debug('Done Sending')
s.shutdown(socket.SHUT_WR)
s.recv(1024)
s.close()
