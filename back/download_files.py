# import configparser
# import json
# import io
# import database
# import os
# from telethon.sync import TelegramClient
# from datetime import date, datetime
# # класс для работы с сообщениями
# from telethon.tl.functions.messages import GetHistoryRequest
#
#
# class FilesDownload:
#     # путь скачивания файлов
#     @staticmethod
#     def get_path_for_download(self, channel_name):
#         # pwd = os.getcwd()  # текущая директория - pwd
#         pwd = os.path.dirname(os.path.abspath(__file__))  # директория скрипта
#         dir_path = os.path.join(pwd, channel_name)
#         return dir_path
#
#     async def dump_all_files(channel):
#         """Записывает json-файл с информацией о всех сообщениях канала/чата"""
#         offset_msg = 0  # номер записи, с которой начинается считывание
#         limit_msg = 100  # максимальное число записей, передаваемых за один раз
#
#         all_messages = []  # список всех сообщений
#         total_messages = 0
#         total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения
#
#         path = PATH4STORING + '/' + channel.title
#         while True:
#             history = await client(GetHistoryRequest(
#                 peer=channel,
#                 offset_id=offset_msg,
#                 offset_date=None, add_offset=0,
#                 limit=limit_msg, max_id=0, min_id=0,
#                 hash=0))
#             if not history.messages:
#                 break
#             messages = history.messages
#             for message in messages:
#                 # файл приложен к сообщению
#                 # < 9000
#                 if message.file != None and message.file.name != None and message.file.ext != '.mp4' and message.file.ext != '.mp3' \
#                         and 8000 < message.id <= 8925 \
#                         and message.id not in (1745,1746,1747,1748,1749,1750) \
#                         and message.id not in (1751,1752,1753,1754,1755,1756,1757,1758,1759,1760,1761,1762):
#                     filename = path + '/' + message.file.name
#                     # размер файла на диске и в телеграмме не совпадает
#                     is_file_exist = os.path.isfile(filename)
#                     disk_file_size = os.stat(filename).st_size if is_file_exist else 0;
#                     if is_file_exist and disk_file_size != message.file.size:
#                         os.remove(filename)
#                     # файла нет на диске
#                     if not is_file_exist:  # and message.file.size < 5*1024*1024: # 5Mb
#                         if message.message != None:
#                             with io.open(filename + '.txt', 'w', encoding='utf8') as file:
#                                 text = message.message + '\n' + \
#                                        'id: ' + str(message.id) + '\n' + \
#                                        'date: ' + str(message.date) + '\n' + \
#                                        'size: ' + '{:,.0f}'.format(message.file.size) + 'Kb'
#                                 file.write(text)
#                         # print('File Name :' + str(message.file.name))
#                         file_path = await client.download_media(message.media, path)
#             offset_msg = messages[len(messages) - 1].id
#             total_messages = len(all_messages)
#             if total_count_limit != 0 and total_messages >= total_count_limit:
#                 break
#
#
# async def main():
#     # url = input("Введите ссылку на канал или чат: ")
#     # url = 'https://t.me/test12734' # Test
#     urls = [
#         # 'https://t.me/DataScience_Books',  # Data Science Books
#         # 'https://t.me/frontendarchive', # !!! Javascript js frontend
#         # 'https://t.me/bookofgeek',  # Книги для программиста
#         ## 'https://t.me/+KTJB5MeJzJRhMDk8', # Data Science Books (Backup Channel)
#         # 'https://t.me/dl_stories', # DLStories | Нейронные сети и ИИ
#         'https://t.me/physics_lib'  # Physics.Math.Code
#         # 'https://t.me/techrocksarchive' # !!! Архив программиста
#         # 'https://t.me/dblib' # Архив книг по Базам данным
#         # 'https://t.me/javalib' # !!! Java библиотека
#
#         # 'https://t.me/medbooksmed' # Medbooks | Medbooking®️
#         # 'https://t.me/scladmedbooksmed2' # Склад Medbooks | Medbooking 2
#     ]
#     for url in urls:
#         channel = await client.get_entity(url)
#         # await dump_all_participants(channel)
#         # await dump_all_messages(channel)
#         await dump_all_files(channel)
#
#
# with client:
#     client.loop.run_until_complete(main())
#
# def test():
#     urls = [
#         ('Data Science Books', 'https://t.me/DataScience_Books'),
#         ('Javascript js frontend', 'https://t.me/frontendarchive'),  # !!!
#         ('Книги для программиста', 'https://t.me/bookofgeek'),
#         ('Data Science Books (Backup Channel)', 'https://t.me/+KTJB5MeJzJRhMDk8'),
#         ('DLStories | Нейронные сети и ИИ', 'https://t.me/dl_stories'),
#         ('Physics.Math.Code', 'https://t.me/physics_lib'),
#         ('Архив программиста', 'https://t.me/techrocksarchive'),  # !!!
#         ('Архив книг по Базам данным', 'https://t.me/dblib'),
#         ('Java библиотека', 'https://t.me/javalib')  # !!!
#     ]
#
#     db = database.DB()
#     db.db_connect()
#     db.db_create_tables()
#     for i in urls:
#         db.add_channel(i[0], i[1])
#     db.add_book(1, 1, datetime.date.today(), 'test', 3000, 'RESERVED')
#     st = db.set_book_state(1, 'test', 'PROCESSED')
#     db.db_disconnect()
#
#
# if __name__ == '__main__':
#     test()
