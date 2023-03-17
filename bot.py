from ediplug import SmartPlug

from data.creds import telegram_token, host, login, password, userid
from data.functions import disable_plug, enable_plug, watch_heatup
from data.general import logger

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi!\n"
                                    "Use /on to start the coffee-machine\n"
                                    "Use /off to stop the coffee-machine\n"
                                    "Or user /status to get the current power consumption")


async def on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    user = update.effective_user.id
    try:
        if user == userid:
            p = SmartPlug(host, (login, password))
            if enable_plug(p):
                await update.effective_message.reply_text(f"Turned on the Coffeemaker")
                await update.effective_message.reply_text(f"Now waiting for heatup to complete")
                if watch_heatup(p):
                    await update.effective_message.reply_text(f"Heatup Done!")
        else:
            await update.effective_message.reply_text("You are not allowed to use this bot")
            await update.effective_message.reply_text(f"User ID: {user}")
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


async def off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user.id
    try:
        if user == userid:
            p = SmartPlug(host, (login, password))
            await update.effective_message.reply_text(disable_plug(p))
        else:
            await update.effective_message.reply_text("You are not allowed to use this bot")
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user.id
    try:
        if user == userid:
            p = SmartPlug(host, (login, password))
            await update.effective_message.reply_text(f"Power: {p.power}w\nCurrent: {p.current}a")
        else:
            await update.effective_message.reply_text("You are not allowed to use this bot")
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("on", on))
    application.add_handler(CommandHandler("off", off))
    application.add_handler(CommandHandler("status", status))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
