from c2.constants import WHEATLY_SERVER_PORT, WHEATLY_SERVER_HOST
from c2.network.server import WheatleyServer
from c2.shell import WheatleyServerShell


def start():
    server = WheatleyServer(WHEATLY_SERVER_HOST, WHEATLY_SERVER_PORT)
    server.start_daemon()
    WheatleyServerShell(server).launch()
