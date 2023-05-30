import unittest
from unittest.mock import MagicMock
from data.bot_functions import on, off, status, start, cancel
from telegram import Update
from telegram.ext import ContextTypes
from ediplug import SmartPlug


class TestBotFunctions(unittest.TestCase):
    def setUp(self):
        self.update = Update(update_id=0)
        self.context = MagicMock(ContextTypes.DEFAULT_TYPE)
        self.context.args = []

    def test_start(self):
        self.context.message.reply_text = MagicMock()
        self.update.message = MagicMock()

        asyncio.run(start(self.update, self.context))
        self.context.message.reply_text.assert_called_once()

    def test_on(self):
        self.context.application.create_task = MagicMock()
        self.context.application.heatup_task = None
        self.context.args = []
        self.update.effective_message = MagicMock()
        self.update.effective_message.reply_text = MagicMock()

        with unittest.mock.patch("data.bot_functions.enable_plug") as mocked_enable_plug:
            with unittest.mock.patch("data.bot_functions.SmartPlug") as mocked_smart_plug:
                mocked_smart_plug.return_value = SmartPlug(host=None, auth=None)
                asyncio.run(on(self.update, self.context))
                mocked_enable_plug.assert_called_once()
                self.update.effective_message.reply_text.assert_called()

    def test_off(self):
        self.context.application.heatup_task = MagicMock()
        self.update.effective_message = MagicMock()
        self.update.effective_message.reply_text = MagicMock()

        with unittest.mock.patch("data.bot_functions.disable_plug") as mocked_disable_plug:
            with unittest.mock.patch("data.bot_functions.SmartPlug") as mocked_smart_plug:
                mocked_smart_plug.return_value = SmartPlug(host=None, auth=None)
                asyncio.run(off(self.update, self.context))
                mocked_disable_plug.assert_called_once()
                self.update.effective_message.reply_text.assert_called()

    def test_status(self):
        self.update.effective_message = MagicMock()
        self.update.effective_message.reply_text = MagicMock()

        with unittest.mock.patch("data.bot_functions.SmartPlug") as mocked_smart_plug:
            mocked_smart_plug.return_value = SmartPlug(host=None, auth=None)
            mocked_smart_plug.return_value.power = 1000
            mocked_smart_plug.return_value.current = 6
            asyncio.run(status(self.update, self.context))
            self.update.effective_message.reply_text.assert_called_once()

    def test_cancel(self):
        self.context.application.heatup_task = MagicMock()
        self.update.effective_message = MagicMock()
        self.update.effective_message.reply_text = MagicMock()

        asyncio.run(cancel(self.update, self.context))
        self.context.application.heatup_task.cancel.assert_called_once()
        self.update.effective_message.reply_text.assert_called_once()


if __name__ == "__main__":
    unittest.main()