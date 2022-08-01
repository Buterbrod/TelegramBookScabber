# Optionl Telethon libraries
# --------------------------------------------------------------------------------------------------------
# If cryptg is installed, the telethon library will work a lot faster, since encryption and
# decryption will be made in C instead of Python.
import cryptg


import configparser
import json
import io
import os
from telethon.sync import TelegramClient
from telethon import connection
# для корректного переноса времени сообщений в json
from datetime import date, datetime
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

PATH4STORING = '/Volumes/Macintosh HD 2/Work/Telegram_Books'

# proxy = (proxy_server, proxy_port, proxy_key)
#
# client = TelegramClient(username, api_id, api_hash,
#     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate)
#     proxy=proxy)
client = TelegramClient(username, api_id, api_hash)

client.start()


async def dump_all_participants(channel):
    """Записывает json-файл с информацией о всех участниках канала/чата"""
    offset_user = 0  # номер участника, с которого начинается считывание
    limit_user = 100  # максимальное число записей, передаваемых за один раз

    all_participants = []  # список всех участников канала
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel,
                                                           filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    all_users_details = []  # список словарей с интересующими параметрами участников канала

    for participant in all_participants:
        all_users_details.append({"id": participant.id,
                                  "first_name": participant.first_name,
                                  "last_name": participant.last_name,
                                  "user": participant.username,
                                  "phone": participant.phone,
                                  "is_bot": participant.bot})

    with open('channel_users.json', 'w', encoding='utf8') as outfile:
        json.dump(all_users_details, outfile, ensure_ascii=False)


async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

        with open('channel_messages.json', 'w', encoding='utf8') as outfile:
            json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def dump_all_files(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    path = PATH4STORING + '/' + channel.title
    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            # файл приложен к сообщению
            # < 9000
            if message.file != None and message.file.name != None and message.file.ext != '.mp4' and message.file.ext != '.mp3' \
                    and 8000 < message.id <= 8925 \
                    and message.id not in (1745,1746,1747,1748,1749,1750) \
                    and message.id not in (1751,1752,1753,1754,1755,1756,1757,1758,1759,1760,1761,1762):
                filename = path + '/' + message.file.name
                # размер файла на диске и в телеграмме не совпадает
                is_file_exist = os.path.isfile(filename)
                disk_file_size = os.stat(filename).st_size if is_file_exist else 0;
                if is_file_exist and disk_file_size != message.file.size:
                    os.remove(filename)
                # файла нет на диске
                if not is_file_exist:  # and message.file.size < 5*1024*1024: # 5Mb
                    if message.message != None:
                        with io.open(filename + '.txt', 'w', encoding='utf8') as file:
                            text = message.message + '\n' + \
                                   'id: ' + str(message.id) + '\n' + \
                                   'date: ' + str(message.date) + '\n' + \
                                   'size: ' + '{:,.0f}'.format(message.file.size) + 'Kb'
                            file.write(text)
                    # print('File Name :' + str(message.file.name))
                    file_path = await client.download_media(message.media, path)
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break


async def main():
    # url = input("Введите ссылку на канал или чат: ")
    # url = 'https://t.me/test12734' # Test
    urls = [
        # 'https://t.me/DataScience_Books',  # Data Science Books
        # 'https://t.me/frontendarchive', # !!! Javascript js frontend
        # 'https://t.me/bookofgeek',  # Книги для программиста
        ## 'https://t.me/+KTJB5MeJzJRhMDk8', # Data Science Books (Backup Channel)
        # 'https://t.me/dl_stories', # DLStories | Нейронные сети и ИИ
        'https://t.me/physics_lib'  # Physics.Math.Code
        # 'https://t.me/techrocksarchive' # !!! Архив программиста
        # 'https://t.me/dblib' # Архив книг по Базам данным
        # 'https://t.me/javalib' # !!! Java библиотека

        # 'https://t.me/medbooksmed' # Medbooks | Medbooking®️
        # 'https://t.me/scladmedbooksmed2' # Склад Medbooks | Medbooking 2
    ]
    for url in urls:
        channel = await client.get_entity(url)
        # await dump_all_participants(channel)
        # await dump_all_messages(channel)
        await dump_all_files(channel)


with client:
    client.loop.run_until_complete(main())
