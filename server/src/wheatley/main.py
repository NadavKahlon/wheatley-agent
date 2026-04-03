from wheatley.constants import WHEATLY_SERVER_PORT, WHEATLY_SERVER_HOST
from wheatley.network.server import WheatleyServer
from wheatley.shell import WheatleyServerShell


def start():
    server = WheatleyServer(WHEATLY_SERVER_HOST, WHEATLY_SERVER_PORT)
    server.start_daemon()
    WheatleyServerShell(server).launch()
