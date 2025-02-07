#!/usr/bin/python3

# ВЕРСИЯ СКРИПТА 2.2.2

import asyncio
import subprocess
import os
import stat
import time

import telebot
from telebot import types
from telethon.sync import TelegramClient
import base64
import requests
import json
import bot_config as config

token = config.token
usernames = config.usernames
routerip = config.routerip
localportsh = config.localportsh
localportvless = config.localportvless
dnsovertlsport = config.dnsovertlsport
dnsoverhttpsport = config.dnsoverhttpsport

repo = "dkuytrewq"

# Начало работы программы
bot = telebot.TeleBot(token)
level = 0
bypass = -1
sid = "0"

# список смайлов для меню
#  ✅ ❌ ♻️ 📃 📆 🔑 📄 ❗ ️⚠️ ⚙️ 📝 📆 🗑 📄️⚠️ 🔰 ❔ ‼️ 📑
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username not in usernames:
        bot.send_message(message.chat.id, 'Вы не являетесь автором канала')
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🔰 Установка и удаление")
    item2 = types.KeyboardButton("🔑 Ключи и мосты")
    item3 = types.KeyboardButton("📝 Списки обхода")
    item4 = types.KeyboardButton("⚙️ Сервис")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, '✅ Добро пожаловать в меню!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    try:
        main = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m1 = types.KeyboardButton("🔰 Установка и удаление")
        m2 = types.KeyboardButton("🔑 Ключи и мосты")
        m3 = types.KeyboardButton("📝 Списки обхода")
        m4 = types.KeyboardButton("📄 Информация")
        m5 = types.KeyboardButton("⚙️ Сервис")
        main.add(m1, m2, m3)
        main.add(m4, m5)

        service = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m1 = types.KeyboardButton("♻️ Перезагрузить сервисы")
        m2 = types.KeyboardButton("‼️Перезагрузить роутер")
        m3 = types.KeyboardButton("‼️DNS Override")
        m4 = types.KeyboardButton("🔄 Обновления")
        back = types.KeyboardButton("🔙 Назад")
        service.add(m1, m2)
        service.add(m3, m4)
        service.add(back)

        if message.from_user.username not in usernames:
            bot.send_message(message.chat.id, 'Вы не являетесь автором канала')
            return
        if message.chat.type == 'private':
            global level, bypass

            if message.text == '⚙️ Сервис':
                bot.send_message(message.chat.id, '⚙️ Сервисное меню!', reply_markup=service)
                return

            if message.text == '♻️ Перезагрузить сервисы' or message.text == 'Перезагрузить сервисы':
                bot.send_message(message.chat.id, '🔄 Выполняется перезагрузка сервисов!', reply_markup=service)
                os.system('/opt/etc/init.d/S22shadowsocks restart')
                os.system('/opt/etc/init.d/S24xray restart')
                bot.send_message(message.chat.id, '✅ Сервисы перезагружены!', reply_markup=service)
                return

            if message.text == '‼️Перезагрузить роутер' or message.text == 'Перезагрузить роутер':
                os.system("ndmc -c system reboot")
                service_router_reboot = "🔄 Роутер перезагружается!\nЭто займет около 2 минут."
                bot.send_message(message.chat.id, service_router_reboot, reply_markup=service)
                return

            if message.text == '‼️DNS Override' or message.text == 'DNS Override':
                service = types.ReplyKeyboardMarkup(resize_keyboard=True)
                m1 = types.KeyboardButton("✅ DNS Override ВКЛ")
                m2 = types.KeyboardButton("❌ DNS Override ВЫКЛ")
                back = types.KeyboardButton("🔙 Назад")
                service.add(m1, m2)
                service.add(back)
                bot.send_message(message.chat.id, '‼️DNS Override!', reply_markup=service)
                return

            if message.text == "✅ DNS Override ВКЛ" or message.text == "❌ DNS Override ВЫКЛ":
                if message.text == "✅ DNS Override ВКЛ":
                    os.system("ndmc -c 'opkg dns-override'")
                    time.sleep(2)
                    os.system("ndmc -c 'system configuration save'")
                    bot.send_message(message.chat.id, '✅ DNS Override включен!\n🔄 Роутер перезагружается.',
                                     reply_markup=service)
                    time.sleep(5)
                    os.system("ndmc -c 'system reboot'")
                    return

                if message.text == "❌ DNS Override ВЫКЛ":
                    os.system("ndmc -c 'no opkg dns-override'")
                    time.sleep(2)
                    os.system("ndmc -c 'system configuration save'")
                    bot.send_message(message.chat.id, '✅ DNS Override выключен!\n🔄 Роутер перезагружается.',
                                     reply_markup=service)
                    time.sleep(5)
                    os.system("ndmc -c 'system reboot'")
                    return

                service_router_reboot = "🔄 Роутер перезагружается!\n⏳ Это займет около 2 минут."
                bot.send_message(message.chat.id, service_router_reboot, reply_markup=service)
                return

            if message.text == '📄 Информация':
                url = "https://raw.githubusercontent.com/dkuytrewq/bypass_keenetic/main/info.md"
                info_bot = requests.get(url).text
                bot.send_message(message.chat.id, info_bot, parse_mode='Markdown', disable_web_page_preview=True,
                                 reply_markup=main)
                return

            if message.text == '/keys_free':
                url = "https://raw.githubusercontent.com/dkuytrewq/bypass_keenetic/main/keys.md"
                keys_free = requests.get(url).text
                bot.send_message(message.chat.id, keys_free, parse_mode='Markdown', disable_web_page_preview=True)
                return

            if message.text == '🔄 Обновления' or message.text == '/check_update':
                url = "https://raw.githubusercontent.com/dkuytrewq/bypass_keenetic/main/version.md"
                bot_new_version = requests.get(url).text

                with open('/opt/etc/bot.py', encoding='utf-8') as file:
                    for line in file.readlines():
                        if line.startswith('# ВЕРСИЯ СКРИПТА'):
                            s = line.replace('# ', '')
                            bot_version = s.strip()

                service_bot_version = "*ВАША ТЕКУЩАЯ " + str(bot_version) + "*\n\n"
                service_new_version = "*ПОСЛЕДНЯЯ ДОСТУПНАЯ ВЕРСИЯ:*\n\n" + str(bot_new_version)
                service_update_info = service_bot_version + service_new_version
                # bot.send_message(message.chat.id, service_bot_version, parse_mode='Markdown', reply_markup=service)
                bot.send_message(message.chat.id, service_update_info, parse_mode='Markdown', reply_markup=service)

                service_update_msg = "Если вы хотите обновить текущую версию на более новую, нажмите сюда /update"
                bot.send_message(message.chat.id, service_update_msg, parse_mode='Markdown', reply_markup=service)
                return

            if message.text == '/update':
                bot.send_message(message.chat.id, 'Устанавливаются обновления, подождите!', reply_markup=service)
                os.system("curl -s -o /opt/root/script.sh https://raw.githubusercontent.com/dkuytrewq/bypass_keenetic/main/script.sh")
                os.chmod(r"/opt/root/script.sh", 0o0755)
                os.chmod('/opt/root/script.sh', stat.S_IRWXU)

                update = subprocess.Popen(['/opt/root/script.sh', '-update'], stdout=subprocess.PIPE)
                for line in update.stdout:
                    results_update = line.decode().strip()
                    bot.send_message(message.chat.id, str(results_update), reply_markup=service)
                return

            if message.text == '🔙 Назад' or message.text == "Назад":
                bot.send_message(message.chat.id, '✅ Добро пожаловать в меню!', reply_markup=main)
                level = 0
                bypass = -1
                return

            if level == 1:
                # значит это список обхода блокировок
                dirname = '/opt/etc/unblock/'
                dirfiles = os.listdir(dirname)

                for fln in dirfiles:
                    if fln == message.text + '.txt':
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton("📑 Показать список")
                        item2 = types.KeyboardButton("📝 Добавить в список")
                        item3 = types.KeyboardButton("🗑 Удалить из списка")
                        back = types.KeyboardButton("🔙 Назад")
                        markup.row(item1, item2, item3)
                        markup.row(back)
                        level = 2
                        bypass = message.text
                        bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                        return

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("🔙 Назад")
                markup.add(back)
                bot.send_message(message.chat.id, "Не найден", reply_markup=markup)
                return

            if level == 2 and message.text == "📑 Показать список":
                file = open('/opt/etc/unblock/' + bypass + '.txt')
                flag = True
                s = ''
                sites = []
                for line in file:
                    sites.append(line)
                    flag = False
                if flag:
                    s = 'Список пуст'
                file.close()
                sites.sort()
                if not flag:
                    for line in sites:
                        s = str(s) + '\n' + line.replace("\n", "")
                if len(s) > 4096:
                    for x in range(0, len(s), 4096):
                        bot.send_message(message.chat.id, s[x:x + 4096])
                else:
                    bot.send_message(message.chat.id, s)
                #bot.send_message(message.chat.id, s)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("📑 Показать список")
                item2 = types.KeyboardButton("📝 Добавить в список")
                item3 = types.KeyboardButton("🗑 Удалить из списка")
                back = types.KeyboardButton("🔙 Назад")
                markup.row(item1, item2, item3)
                markup.row(back)
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 2 and message.text == "📝 Добавить в список":
                bot.send_message(message.chat.id,
                                 "Введите имя сайта или домена для разблокировки, "
                                 "либо воспользуйтесь меню для других действий")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("🔙 Назад")
                markup.add(back)
                level = 3
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 2 and message.text == "🗑 Удалить из списка":
                bot.send_message(message.chat.id,
                                 "Введите имя сайта или домена для удаления из листа разблокировки,"
                                 "либо возвратитесь в главное меню")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("🔙 Назад")
                markup.add(back)
                level = 4
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 3:
                f = open('/opt/etc/unblock/' + bypass + '.txt')
                mylist = set()
                for line in f:
                    mylist.add(line.replace('\n', ''))
                f.close()
                k = len(mylist)
                if len(message.text) > 1:
                    mas = message.text.split('\n')
                    for site in mas:
                        mylist.add(site)
                sortlist = []
                for line in mylist:
                    sortlist.append(line)
                sortlist.sort()
                f = open('/opt/etc/unblock/' + bypass + '.txt', 'w')
                for line in sortlist:
                    f.write(line + '\n')
                f.close()
                if k != len(sortlist):
                    bot.send_message(message.chat.id, "✅ Успешно добавлено")
                else:
                    bot.send_message(message.chat.id, "Было добавлено ранее")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("📑 Показать список")
                item2 = types.KeyboardButton("📝 Добавить в список")
                item3 = types.KeyboardButton("🗑 Удалить из списка")
                back = types.KeyboardButton("🔙 Назад")
                markup.row(item1, item2, item3)
                markup.row(back)
                subprocess.call(["/opt/bin/unblock_update.sh"])
                level = 2
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 4:
                f = open('/opt/etc/unblock/' + bypass + '.txt')
                mylist = set()
                for line in f:
                    mylist.add(line.replace('\n', ''))
                f.close()
                k = len(mylist)
                mas = message.text.split('\n')
                for site in mas:
                    mylist.discard(site)
                f = open('/opt/etc/unblock/' + bypass + '.txt', 'w')
                for line in mylist:
                    f.write(line + '\n')
                f.close()
                if k != len(mylist):
                    bot.send_message(message.chat.id, "✅ Успешно удалено")
                else:
                    bot.send_message(message.chat.id, "Не найдено в списке")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("📑 Показать список")
                item2 = types.KeyboardButton("📝 Добавить в список")
                item3 = types.KeyboardButton("🗑 Удалить из списка")
                back = types.KeyboardButton("🔙 Назад")
                markup.row(item1, item2, item3)
                markup.row(back)
                level = 2
                subprocess.call(["/opt/bin/unblock_update.sh"])
                bot.send_message(message.chat.id, "Меню " + bypass, reply_markup=markup)
                return

            if level == 5:
                shadowsocks(message.text)
                time.sleep(2)
                os.system('/opt/etc/init.d/S22shadowsocks restart')
                level = 0
                bot.send_message(message.chat.id, '✅ Успешно обновлено', reply_markup=main)
                # return

            if level == 8:
                if message.text == 'Shadowsocks':
                    #bot.send_message(message.chat.id, "Скопируйте ключ сюда")
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    back = types.KeyboardButton("🔙 Назад")
                    markup.add(back)
                    level = 5
                    bot.send_message(message.chat.id, "🔑 Скопируйте ключ сюда", reply_markup=markup)
                    return

                if message.text == 'Vless':
                    #bot.send_message(message.chat.id, "Скопируйте ключ сюда")
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    back = types.KeyboardButton("🔙 Назад")
                    markup.add(back)
                    level = 9
                    bot.send_message(message.chat.id, "🔑 Скопируйте ключ сюда", reply_markup=markup)
                    return

            if level == 9:
                vless(message.text)
                os.system('/opt/etc/init.d/S24xray restart')
                level = 0
                bot.send_message(message.chat.id, '✅ Успешно обновлено', reply_markup=main)

            if message.text == '🔰 Установка и удаление':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("♻️ Установка & переустановка")
                item2 = types.KeyboardButton("⚠️ Удаление")
                back = types.KeyboardButton("🔙 Назад")
                markup.row(item1, item2)
                markup.row(back)
                bot.send_message(message.chat.id, '🔰 Установка и удаление', reply_markup=markup)
                return

            if message.text == '♻️ Установка & переустановка':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Fork by dkuytrewq")
                back = types.KeyboardButton("🔙 Назад")
                markup.row(item1)
                markup.row(back)
                bot.send_message(message.chat.id, 'Выберите репозиторий', reply_markup=markup)
                return

            if message.text == "Fork by dkuytrewq":
                url = "https://raw.githubusercontent.com/dkuytrewq/bypass_keenetic/main/script.sh".format(repo)
                os.system("curl -s -o /opt/root/script.sh " + url + "")
                os.chmod(r"/opt/root/script.sh", 0o0755)
                os.chmod('/opt/root/script.sh', stat.S_IRWXU)

                install = subprocess.Popen(['/opt/root/script.sh', '-install'], stdout=subprocess.PIPE)
                for line in install.stdout:
                    results_install = line.decode().strip()
                    bot.send_message(message.chat.id, str(results_install), reply_markup=main)

                bot.send_message(message.chat.id,
                                 "Установка завершена. Теперь нужно немного настроить роутер и перейти к "
                                 "спискам для разблокировок. "
                                 "Ключи для Vless, Shadowsocks необходимо установить вручную",
                                 reply_markup=main)

                bot.send_message(message.chat.id,
                                 "Что бы завершить настройку роутера, Зайдите в меню сервис -> DNS Override -> ВКЛ. "
                                 "Учтите, после выполнения команды, роутер перезагрузится, это займет около 2 минут.",
                                 reply_markup=main)

                subprocess.call(["/opt/bin/unblock_update.sh"])
                # os.system('/opt/bin/unblock_update.sh')
                return

            if message.text == '⚠️ Удаление':
                os.system("curl -s -o /opt/root/script.sh https://raw.githubusercontent.com/dkuytrewq/bypass_keenetic/main/script.sh")
                os.chmod(r"/opt/root/script.sh", 0o0755)
                os.chmod('/opt/root/script.sh', stat.S_IRWXU)

                remove = subprocess.Popen(['/opt/root/script.sh', '-remove'], stdout=subprocess.PIPE)
                for line in remove.stdout:
                    results_remove = line.decode().strip()
                    bot.send_message(message.chat.id, str(results_remove), reply_markup=service)
                return

            if message.text == "📝 Списки обхода":
                level = 1
                dirname = '/opt/etc/unblock/'
                dirfiles = os.listdir(dirname)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markuplist = []
                for fln in dirfiles:
                    # markup.add(fln.replace(".txt", ""))
                    btn = fln.replace(".txt", "")
                    markuplist.append(btn)
                markup.add(*markuplist)
                back = types.KeyboardButton("🔙 Назад")
                markup.add(back)
                bot.send_message(message.chat.id, "📝 Списки обхода", reply_markup=markup)
                return

            if message.text == "🔑 Ключи и мосты":
                level = 8
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Shadowsocks")
                item2 = types.KeyboardButton("Vless")
                markup.add(item1, item2)
                back = types.KeyboardButton("🔙 Назад")
                markup.add(back)
                bot.send_message(message.chat.id, "🔑 Ключи и мосты", reply_markup=markup)
                return

    except Exception as error:
        file = open("/opt/etc/error.log", "w")
        file.write(str(error))
        file.close()
        os.chmod(r"/opt/etc/error.log", 0o0755)

def vless(key):
    # global password, localportvless
    encodedkey = key[8:]
    s = base64.b64decode(encodedkey).decode('utf8').replace("'", '"')
    jsondata = json.loads(s)
    f = open('/opt/etc/xray/config.json', 'w')
    sh = '{"log":{"access":"/opt/etc/xray/access.log","error":"/opt/etc/xray/error.log","loglevel":"info"},' \
         '"inbounds":[{"port":' + str(localportvless) + ',"listen":"::","protocol":"dokodemo-door",' \
         '"settings":{"network":"tcp","followRedirect":true},'\
         '"sniffing":{"enabled":true,"destOverride":["http","tls"]}}],' \
         '"outbounds":[{"tag":"proxy","domainStrategy":"UseIPv4","protocol":"vless",' \
         '"settings":{"vnext":[{"address":"' + str(jsondata["add"]) + '","port":' + str(jsondata["port"]) + ',' \
         '"users":[{"id":"' + str(jsondata["id"]) + '","alterId":' + str(jsondata["aid"]) + ',' \
         '"email":"t@t.tt","security":"auto"}]}]},"streamSettings":{"network":"' + str(jsondata["net"]) + '",' \
         '"security":"tls","tlsSettings":{"allowInsecure":true,"serverName":"' + str(jsondata["add"]) + '"},' \
         '"wsSettings":{"path":"' + str(jsondata["path"]) + '","headers":{"Host":"' + str(jsondata["host"]) + '"}},' \
         '"tls":"' + str(jsondata["tls"]) + '"},"mux":{"enabled":true,"concurrency":-1,"xudpConcurrency": 16,"xudpProxyUDP443":"reject"}}],' \
         '"routing":{"domainStrategy":"IPIfNonMatch",' \
         '"rules":[{"type":"field","port":"0-65535","outboundTag":"proxy","enabled":true}]}}'
    f.write(sh)
    f.close()

def shadowsocks(key=None):
    # global password, localportsh
    encodedkey = str(key).split('//')[1].split('@')[0] + '=='
    password = str(str(base64.b64decode(encodedkey)[2:]).split(':')[1])[:-1]
    server = str(key).split('@')[1].split('/')[0].split(':')[0]
    port = str(key).split('@')[1].split('/')[0].split(':')[1].split('#')[0]
    method = str(str(base64.b64decode(encodedkey)).split(':')[0])[2:]
    f = open('/opt/etc/shadowsocks.json', 'w')
    sh = '{"server": ["' + server + '"], "mode": "tcp_and_udp", "server_port": ' \
         + str(port) + ', "password": "' + password + \
         '", "timeout": 86400,"method": "' + method + \
         '", "local_address": "::", "local_port": ' \
         + str(localportsh) + ', "fast_open": false,    "ipv6_first": true}'
    f.write(sh)
    f.close()

# bot.polling(none_stop=True)
try:
    bot.infinity_polling()
except Exception as err:
    fl = open("/opt/etc/error.log", "w")
    fl.write(str(err))
    fl.close()
