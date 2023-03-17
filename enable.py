import time

from ediplug import SmartPlug
from creds import *
from general import logger

def enable_plug(p):
    if p.power == 0 and p.current == 0:
        logger.info("Turning on")
        p.state = "ON"
    else:
        logger.info("Already on")
    return True


def watch_heatup(p):
    go = True
    check_down = 0
    while go:
        time.sleep(10)
        power = float(p.power)
        current = float(p.current)
        print(f"{power} w - {current} a")
        if power < 1000 and current < 6:
            check_down += 1
        elif check_down > 0:
            check_down -= 1
        if check_down == 10:
            logger.info("Coffee Maker Ready")
            go = False
        else:
            print(check_down)


def main():
    p = SmartPlug(host, (login, password))

    if enable_plug(p):
        watch_heatup(p)


if __name__ == '__main__':
    main()
