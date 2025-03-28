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

# Changed from string characters to integer values
CHANNEL_CLOSE_CMD = 0xCC
CHANNEL_OPEN_CMD = 0xDD
FORWARD_CONNECTION_SUCCESS = 0xEE
FORWARD_CONNECTION_FAILURE = 0xFF
CLOSE_RELAY = 0xC4
PING_CMD = 0x70

# Updated cmd_names to use integer keys
cmd_names = {
    CHANNEL_CLOSE_CMD: 'CHANNEL_CLOSE_CMD',
    CHANNEL_OPEN_CMD: 'CHANNEL_OPEN_CMD',
    FORWARD_CONNECTION_SUCCESS: 'FORWARD_CONNECTION_SUCCESS',
    FORWARD_CONNECTION_FAILURE: 'FORWARD_CONNECTION_FAILURE',
    CLOSE_RELAY: 'CLOSE_RELAY',
    PING_CMD: 'PING_CMD'
}


class ClosedSocket(Exception):
    pass


class RelayError(Exception):
    pass


def recvall(sock, data_len):
    buf = b''  # Initialize as bytes
    while len(buf) < data_len:
        chunk = sock.recv(data_len - len(buf))
        if not chunk:
            raise RelayError("Socket connection broken")
        buf += chunk
    return buf


def close_sockets(sockets):
    for s in sockets:
        try:
            s.close()
        except socket.error:
            pass
