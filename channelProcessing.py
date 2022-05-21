import configparser
import asyncio
from database import DB
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

NOT_PROCESSED_EXT = ['mp4', 'mp3']


class ChannelProcessing:
    client: TelegramClient
    tasks: []

    def __init__(self):
        self.tasks = []

    def connect_to_telegram(self):
        # Считываем учетные данные
        config = configparser.ConfigParser()
        config.read("config.ini")

        # Присваиваем значения внутренним переменным
        api_id = config['Telegram']['api_id']
        api_hash = config['Telegram']['api_hash']
        username = config['Telegram']['username']

        self.client = TelegramClient(username, api_id, api_hash)
        self.client.start()

    def disconnect_from_telegram(self):
        self.client.disconnect()

    # Записывает json-файл с информацией о всех сообщениях канала/чата
    async def process_channel(self, channel_tech_name, db):
        offset_msg = 0  # номер записи, с которой начинается считывание
        limit_msg = 100  # максимальное число записей, передаваемых за один раз

        # channel = await client.get_entity(url)
        db_channel_id = db.get_channel_id(channel_tech_name)
        # цикл, так как получаем сообщения порциями
        while True:
            print(channel_tech_name + ": " + str(offset_msg))
            history = GetHistoryRequest(
                peer=channel_tech_name,
                offset_id=offset_msg,  # номер записи, с которой начинается считывание
                offset_date=None,  # дата, с которой начинается считывание
                add_offset=0,
                limit=limit_msg,  # максимальное число записей, передаваемых за один раз
                max_id=0,
                min_id=0,
                hash=0)
            try:
                history = await self.client(history)
            except ValueError as error:
                print(channel_tech_name + ": " + str(error))
                break
            except Exception as error:
                print("Exception: " + error)
                break
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                # файл приложен к сообщению
                if message.file is not None and message.file.name is not None \
                        and message.file.ext not in NOT_PROCESSED_EXT:
                    db.add_book(db_channel_id, message.id, message.date, message.file.name, message.file.size,
                                "NOT_SAVED")
            offset_msg = messages[len(messages) - 1].id

    def add_channel_processing(self, channel_tech_name, db):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.process_channel(channel_tech_name, db), name=channel_tech_name)
        self.tasks.append(task)

    def wait_channel_processing(self):
        # await asyncio.wait(self.tasks)
        loop = asyncio.get_event_loop()
        #loop.run_forever() # run_until_complete(asyncio.sleep(3))
        for task in self.tasks:
            loop.run_until_complete(task)


    def process_channels(self, urls, db, cp):
        for channel_name, channel_tech_name in urls:
            db.add_channel(channel_name, channel_tech_name)
            cp.add_channel_processing(channel_tech_name, db)
        self.wait_channel_processing()


def main():
    urls = [
        ('Data Science Books', 'https://t.me/DataScience_Books'),
        ('Javascript js frontend', 'https://t.me/frontendarchive'),  # !!!
        ('Книги для программиста', 'https://t.me/bookofgeek'),
        ('Data Science Books (Backup Channel)', 'https://t.me/+KTJB5MeJzJRhMDk8'),
        ('DLStories | Нейронные сети и ИИ', 'https://t.me/dl_stories'),
        ('Physics.Math.Code', 'https://t.me/physics_lib'),
        ('Архив программиста', 'https://t.me/techrocksarchive'),  # !!!
        ('Архив книг по Базам данным', 'https://t.me/dblib'),
        ('Java библиотека', 'https://t.me/javalib')  # !!!
    ]

    db = DB()
    cp = ChannelProcessing()
    db.db_connect()
    cp.connect_to_telegram()
    # asyncio.run(cp.process_channels(urls, db, cp))
    cp.process_channels(urls, db, cp)
    cp.disconnect_from_telegram()
    db.db_disconnect()


if __name__ == '__main__':
    main()
