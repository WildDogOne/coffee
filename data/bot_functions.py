import asyncio

from ediplug import SmartPlug

from data.creds import host, login, password, userid
from data.functions import disable_plug, enable_plug
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


@restricted
async def heatup(chat_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE, timeout: int = 10) -> None:
    global heating
    heating = True

    p = SmartPlug(host, (login, password))
    go = True
    check_down = 0
    while go and heating:
        await asyncio.sleep(10)
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
    if heating:
        await context.bot.send_message(chat_id, text=f"Heatup Done!")
    else:
        await context.bot.send_message(chat_id, text=f"Heatup Stopped!")

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
        timeout = 15
    try:
        p = SmartPlug(host, (login, password))
        # context.task = asyncio.create_task(heatup(user, context=context))
        if heating:
            await update.effective_message.reply_text(f"Already heating up, be patient!")
        else:
            enable_plug(p)
            await update.effective_message.reply_text(f"Turned on the Coffeemaker")
            await update.effective_message.reply_text(f"Now waiting for heatup to complete")
            # context.application.create_task(heatup(user, context=context, timeout=timeout, update=update),update=update)
            context.application.heatup_task = context.application.create_task(
                heatup(user, context=context, timeout=timeout, update=update))
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


@restricted
async def off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.application.heatup_task.cancel()
    global heating
    heating = False
    try:
        p = SmartPlug(host, (login, password))
        await update.effective_message.reply_text(disable_plug(p))
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


@restricted
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    p = SmartPlug(host, (login, password))
    await update.effective_message.reply_text(f"Power: {p.power}w\nCurrent: {p.current}a")


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
