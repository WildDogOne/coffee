from ediplug import SmartPlug
from data.creds import *
from data.functions import enable_plug, watch_heatup


def main():
    p = SmartPlug(host, (login, password))
    if enable_plug(p):
        watch_heatup(p)


if __name__ == '__main__':
    main()
