import configparser

from pyrogram import Client
from pyrogram import enums
import asyncio
import uvloop

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

uvloop.install()
app = Client("my_account", api_id=api_id, api_hash=api_hash)


async def main():
    async with app:
        # Send a message, Markdown is enabled by default
        await app.send_message("me", "Hi there! I'm using **Pyrogram**")
        await app.send_message(
            "me",
            (
                "<b>bold</b>, "
                "<i>italic</i>, "
                "<u>underline</u>, "
                "<s>strike</s>, "
                "<spoiler>spoiler</spoiler>, "
                "<a href=\"https://pyrogram.org/\">URL</a>, "
                "<code>code</code>\n\n"
                "<pre>"
                "for i in range(10):\n"
                "    print(i)"
                "</pre>"
            ),
            parse_mode=enums.ParseMode.HTML
        )

app.run(main())
