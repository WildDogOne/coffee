# Coffee Bot

A Telegram bot that allows you to control your coffee machine using the Edimax SmartPlug. The bot provides commands to
turn the coffee machine on and off, cancel the heat-up process, and check the machine's status.

## Features

- Start the coffee machine
- Stop the coffee machine
- Cancel the heat-up process
- Check the coffee machine's power consumption and current

## Prerequisites

- Python 3.7+
- Edimax SmartPlug

## Dependencies

- `python-telegram-bot`
- `edi-plug`

To install the dependencies, run:

```bash
pip install python-telegram-bot edi-plug
```

## Setup

1. Rename `data/creds.py.example` to `data/creds.py` and fill in the required information:

```python
host = "your_smartplug_ip"
login = "your_smartplug_login"
password = "your_smartplug_password"
userid = your_telegram_user_id
```

1. Set up the logging configuration in `data/general.py`:

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
```

## Usage

1. Run the Python script:

```bash
python coffee_machine_controller.py
```

1. Use the following commands in the Telegram chat:

- `/on`: Turn on the coffee machine and start the heat-up process. Optionally, you can add a timeout (in minutes) after
  which the coffee machine will automatically turn off, e.g., `/on 20`.
- `/off`: Turn off the coffee machine.
- `/cancel`: Cancel the heat-up process if it's ongoing.
- `/status`: Check the coffee machine's power consumption (in watts) and current (in amperes).

1. In case you need to add the main function to run the script, you can use the following template:

```python
from telegram.ext import Updater


def main() -> None:
    token = "YOUR_BOT_TOKEN"
    updater = Updater(token, context_types=ContextTypes(default=CustomApplication), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("on", on, pass_args=True))
    dp.add_handler(CommandHandler("off", off))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
```

Replace `YOUR_BOT_TOKEN` with your actual bot token.

1. After setting up the main function, start the bot by running the script:

```bash
python coffee_machine_controller.py
```

Now you can control your coffee machine through the Telegram bot by sending the commands listed above. Make sure to
start a chat with your bot on Telegram, and you'll be able to interact with it to control your coffee machine.

## Troubleshooting

If you encounter any issues with the bot or the coffee machine, make sure to check the following:

1. Ensure the Edimax SmartPlug is connected to your coffee machine and the network.
2. Verify your SmartPlug credentials and IP address in `data/creds.py`.
3. Ensure you have the correct Telegram user ID in `data/creds.py`.
4. Check the logs for any errors or information about the bot's actions.

## License

This project is provided under the [MIT License](https://choosealicense.com/licenses/mit/).

### Service

sudo vim /etc/systemd/system/coffeebot.service

```
[Unit]
Description=coffeebot
[Service]
Type=simple
PIDFile=/run/coffeebot.pid
User=pi
Group=pi
WorkingDirectory=/home/pi/coffee
VIRTUAL_ENV=/home/pi/coffee/env/
Environment=PATH=$VIRTUAL_ENV/bin:$PATH
ExecStart=/home/pi/coffee/env/bin/python3 /home/pi/coffee/bot.py
Restart=on-failure
RestartSec=5s
[Install]
WantedBy=multi-user.target
```

sudo systemctl enable coffeebot
sudo systemctl start coffeebot