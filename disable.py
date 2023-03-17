import time

from ediplug import SmartPlug
from creds import *
from general import logger


def disable_plug(p):
    if float(p.power) == 0 and float(p.current) == 0:
        logger.info("Already Off")
    else:
        logger.info("Turning off")
        p.state = "OFF"
    return True


def main():
    p = SmartPlug(host, (login, password))
    disable_plug(p)


if __name__ == '__main__':
    main()
