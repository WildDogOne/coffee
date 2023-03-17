import time

from ediplug import SmartPlug
from creds import *
from general import logger
from tkinter import *
from tkinter import messagebox


def enable_plug(p):
    logger.debug(f"Enabling: {p.power} - {p.current}")
    if p.power == 0 and p.current == 0:
        logger.debug("Turning on")
        p.state = "ON"
    else:
        logger.debug("Already on")
    logger.info("Turned on Smartplug")
    return True


def watch_heatup(p):
    go = True
    check_down = 0
    while go:
        time.sleep(10)
        power = float(p.power)
        current = float(p.current)
        logger.info(f"{power} w - {current} a")
        if power < 1000 and current < 6:
            check_down += 1
        elif check_down > 0:
            check_down -= 1
        if check_down == 10:
            logger.info("Coffee Maker Ready")
            top = Tk()
            top.geometry("100x100")
            messagebox.showinfo("information", "Coffee Maker Ready")
            top.mainloop()
            go = False
        else:
            logger.debug(f"Watt Check: {check_down}")


def main():
    p = SmartPlug(host, (login, password))
    if enable_plug(p):
        watch_heatup(p)


if __name__ == '__main__':
    main()
