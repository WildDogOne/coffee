import time
from data.general import logger


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
            go = False
        else:
            logger.debug(f"Watt Check: {check_down}")
    return True

def disable_plug(p):
    if p.power == 0 and p.current == 0:
        logger.info("Already Off")
        p.state = "OFF"
        return "Already Off"
    else:
        logger.info("Turning off")
        p.state = "OFF"
        return "Turned Off"
