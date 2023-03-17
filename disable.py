from ediplug import SmartPlug
from data.creds import *
from data.functions import disable_plug


def main():
    p = SmartPlug(host, (login, password))
    disable_plug(p)


if __name__ == '__main__':
    main()
