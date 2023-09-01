import time
from data.general import logger
import requests


def enable_plug(host):
    status = get_plug_status(host)
    logger.debug(f"Enabling: {status['power']} - {status['Ws']}")
    if status["relay"]:
        logger.debug("Already on")
    else:
        logger.debug("Turning on")
        requests.get(f"http://{host}/relay?state=1")
    logger.info("Turned on Smartplug")
    return True


def watch_heatup(host):
    go = True
    check_down = 0
    while go:
        time.sleep(10)
        status = get_plug_status(host)
        Ws = float(status["Ws"])
        power = float(status["power"])
        logger.info(f"{Ws} average since last call - {power} w")
        if power < 800:
            check_down += 1
        elif check_down > 0:
            check_down -= 1
        if check_down == 10:
            logger.info("Coffee Maker Ready")
            go = False
        else:
            logger.debug(f"Watt Check: {check_down}")
    return True

def disable_plug(host):
    status = get_plug_status(host)["relay"]
    if status:
        logger.info("Turning off")
        requests.get(f"http://{host}/relay?state=0").status_code
        return "Turned Off"
    else:
        logger.info("Already Off")
        requests.get(f"http://{host}/relay?state=0").status_code
        return "Already Off"

def get_plug_status(host):
    return requests.get(f"http://{host}/report").json()
