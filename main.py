# -*- coding: utf-8 -*-

DATA = "someinfo.txt"
DATA_QUEUE = "queue.txt"

import logging
import json
import random
from collections import OrderedDict

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue, CallbackContext
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

QUEUE = OrderedDict()
logger = logging.getLogger(__name__)

bvm = """вылазий
покажи личико
высовывайся
встать
проснись"""
bvm = bvm.split("\n")

bm = """баклажанчик
баклофенчик
бананчик
баобаб ты мой роскошный
барабасик
барабулечка
бармалей
бармалейчик
барсик
басечка
батончик
бевальгинчик
бегемотик
белласпончик
беллатаминальчик
бемитильчик
бензональчик
берлидормик
бесючичка
бесюш ик
бетамаксик
биоксетинчик
бирулестик
бирюллик ты мой"""
bm = bm.split("\n")


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('ухади')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('помощи не проси, помощи больше нет, помощь принял ислам')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("ухади")
    print("CHAT_ID", update.chat.id)
    if update.message:
        print(update.message)
    print(context)

def add_student(update, context):
    uid, name = (update.message.from_user.id, update.message.from_user.first_name)
    uid = int(uid)
    l = json.load(open(DATA))
    l[str(uid)] = name # добавляем пидоров в список
    json.dump(l, open(DATA, "w"))
    update.message.reply_text("теперь ты поставлен на учет в дурку")

def me(update, context):
    global QUEUE
    global reminder
    uid, name = (update.message.from_user.id, update.message.from_user.first_name)
    uid = int(uid)
    l = json.load(open(DATA))
    print(l)
    l[str(uid)] = name # добавляем пидоров в список
    json.dump(l, open(DATA, "w"))

    num = len(QUEUE) + 1
    if uid in QUEUE:
        num = list(QUEUE.keys()).index(uid) + 1
    else:
        QUEUE[uid] = name

    update.message.reply_text(f"ты {num}-й в очереди")

def delete_student(update, context):
    global QUEUE
    uid, name = (update.message.from_user.id, update.message.from_user.first_name)
    del[QUEUE[uid]]
    update.message.reply_text("ну и ухади отсюда)0))0)")

def list_queue(update, context):
    i = 0
    msg = ""
    for uid, name in QUEUE.items():
        i += 1
        msg += str(i) + ". " + name + "\n"
    update.message.reply_text(msg)

def list_students(update, context):
    l = json.load(open(DATA))
    msg = "список пациентов:\n\n" + "\n===\n".join(l.values())
    update.message.reply_text(msg)
    
def generate_queue(update, context):
    global QUEUE

    mentions = json.load(open(DATA)).items()

    new_faggots = []

    for uid, name in mentions:
        uid = int(uid)
        try:
            _ = QUEUE[uid]
        except KeyError:
            new_faggots.append((uid, name))

    random.shuffle(new_faggots)
    for uid, name in new_faggots:
        uid = int(uid)
        QUEUE[uid] = name
    
    update.message.reply_text(f"кол-во принуждённых: {len(new_faggots)}, добровольнопринудительно)0")

def load_queue(update, context):
    global QUEUE
    QUEUE = OrderedDict()

    for uid, name in json.load(open(DATA_QUEUE)).items():
        uid = int(uid)
        QUEUE[uid] = name

    update.message.reply_text("загрузил вроде")



def next_student(update, context):
    global QUEUE
    if QUEUE:
        uid, name = QUEUE.popitem(False)
        mention = f"[{escape_markdown(name)}](tg://user?id={uid})"
        adj = random.choice(bm)
        verb = random.choice(bvm)
        msg = f"{escape_markdown(adj.title())} {mention}\, {escape_markdown(verb)}\n осталось {len(QUEUE)}\.\.\."
        print(msg)
        update.message.reply_text(msg, parse_mode='MarkdownV2')
    else:
        update.message.reply_text("люди вмерли, очередь пуста (^_^)")


def clear_queue(update, context):
    global QUEUE
    QUEUE = OrderedDict()
    update.message.reply_text("очередь за таблетками резко опустела")


def main():
    """Start the bot."""
    updater = Updater("1383885881:AAH66xHHVbfbRFkCjw0i8_6vttNLfy0A7F8", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("add", add_student))
    dp.add_handler(CommandHandler("del", delete_student))
    dp.add_handler(CommandHandler("me", me))
    dp.add_handler(CommandHandler("queue", list_queue))
    dp.add_handler(CommandHandler("next", next_student))
    dp.add_handler(CommandHandler("clear", clear_queue))

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("generate_queue", generate_queue))
    dp.add_handler(CommandHandler("load_queue", load_queue))
    dp.add_handler(CommandHandler("list_students", list_students))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()