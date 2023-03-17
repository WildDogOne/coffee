# Coffee Bot

Little repository to remotely start my coffeemaker via a Smartplug.


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