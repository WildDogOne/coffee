import asyncio

from data.creds import host, userid
from data.functions import disable_plug, enable_plug, get_plug_status
from data.general import logger
from functools import wraps

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Dirty hack variable to check if machine is heating up or not.
heating = False


def restricted(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user.id
        if user == userid:
            return await func(update, context, *args, **kwargs)
        else:
            await update.effective_message.reply_text("Unauthorized access. You are not allowed to use this bot.")
    return wrapper


class CustomApplication(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.heatup_task = None


async def heatup(chat_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE, timeout: int = 10) -> None:
    global heating
    heating = True

    go = True
    check_down = 0
    while go and heating:
        await asyncio.sleep(10)
        status = get_plug_status(host)
        wats = float(status["Ws"])
        amps = float(status["power"])
        logger.info(f"{wats} w - {amps} a")
        if wats < 1000 and amps < 6:
            check_down += 1
        elif check_down > 0:
            check_down -= 1
        if check_down == 10:
            logger.info("Coffee Maker Ready")
            go = False
        else:
            logger.debug(f"Watt Check: {check_down}")
    await context.bot.send_message(chat_id, text=f"Boiler Heatup Done!\nSetting Timer for Brewgroup")
    await asyncio.sleep(20 * 60)
    if heating:
        await context.bot.send_message(chat_id, text=f"Brewgroup Hot")

    await asyncio.sleep(timeout * 60)
    if heating:
        await context.bot.send_message(chat_id, text=f"Forgot to turn off machine!\nTurning off now")
        await off(update=update, context=context)


@restricted
async def on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user.id
    if len(context.args) > 0:
        try:
            timeout = int(context.args[0])
        except:
            await update.effective_message.reply_text("Usage: /on <minutes> or just /on")
            return
    else:
        timeout = 10
    try:
        if heating:
            await update.effective_message.reply_text(f"Already heating up, be patient!")
        else:
            enable_plug(host)
            await update.effective_message.reply_text(f"Turned on the Coffeemaker\n"
                                                      f"Now waiting for heatup to complete")
            context.application.heatup_task = context.application.create_task(
                heatup(user, context=context, timeout=timeout, update=update))
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


@restricted
async def off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        context.application.heatup_task.cancel()
    except:
        await update.effective_message.reply_text("No heatup running")
    global heating
    heating = False
    try:
        await update.effective_message.reply_text(disable_plug(host))
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


@restricted
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status = get_plug_status(host)
    await update.effective_message.reply_text(f"Power: {status['Ws']}w\nCurrent: {status['power']}a")


@restricted
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if context.application.heatup_task and not context.application.heatup_task.done():
            context.application.heatup_task.cancel()
            global heating
            heating = False
            await update.effective_message.reply_text("Heatup cancelled.")
        else:
            await update.effective_message.reply_text("No ongoing heatup task to cancel.")
    except:
        await update.effective_message.reply_text("No ongoing heatup task to cancel.")


@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi!\n"
                                    "Use /on to start the coffee-machine\n"
                                    "Use /off to stop the coffee-machine\n"
                                    "Use /cancel to stop the heatup task, without turning off the machine\n"
                                    "Or user /status to get the current power consumption")
