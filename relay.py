import time
import socket


buffer_size = 4096
delay = 0.0001
relay_timeout = 60
banner = b"RPIVOT"
banner_response = b"RPIVOT_OK"
socks_server_reply_success = b"\x00\x5a\x00\x00\x00\x00\x00\x00"
socks_server_reply_fail = b"\x00\x5b\x00\x00\x00\x00\x00\x00"
COMMAND_CHANNEL = 0

CHANNEL_CLOSE_CMD = '\xcc'
CHANNEL_OPEN_CMD = '\xdd'
FORWARD_CONNECTION_SUCCESS = '\xee'
FORWARD_CONNECTION_FAILURE = '\xff'
CLOSE_RELAY = '\xc4'
PING_CMD = '\x70'

cmd_names = {
    '\xcc': 'CHANNEL_CLOSE_CMD',
    '\xdd': 'CHANNEL_OPEN_CMD',
    '\xee': 'FORWARD_CONNECTION_SUCCESS',
    '\xff': 'FORWARD_CONNECTION_FAILURE',
    '\xc4': 'CLOSE_RELAY',
    '\x70': 'PING_CMD'
}


class ClosedSocket(Exception):
    pass


class RelayError(Exception):
    pass


def recvall(sock, data_len):
    buf = ''
    while True:
        buf += sock.recv(data_len - len(buf))
        if len(buf) == data_len:
            break
        time.sleep(delay)
    assert(data_len == len(buf))
    return buf


def close_sockets(sockets):
    for s in sockets:
        try:
            s.close()
        except socket.error:
            pass
