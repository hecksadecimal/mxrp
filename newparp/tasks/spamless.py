from celery import chord
from celery.utils.log import get_task_logger
from random import shuffle
from sqlalchemy import and_, func, or_
from uuid import uuid4
import re
import hashlib
import json
from newparp.tasks import celery, WorkerTask
from random import randint
from celery.utils.log import get_task_logger
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from newparp.helpers.chat import send_message
from newparp.model import AnyChat, ChatUser, Message, User, SpamlessFilter
from newparp.model.connections import session_scope, NewparpRedis, redis_pool

logger = get_task_logger(__name__)


lists = {"reload": "0"}


class Mark(Exception):
    pass


class Silence(Exception):
    pass


@celery.task(base=WorkerTask, queue="spamless")
def check_spam_task(chat_id, data, raw_text):
    redis = check_spam_task.redis

    if len(data["messages"]) == 0:
        return

    load_lists(redis)

    for message in data["messages"]:
        if message["user_number"] is None:
            continue

        redis.set("spamless:last_id", message["id"])

        message["hash"] = hashlib.md5(
            ":".join([message["color"], message["acronym"], message["text"]])
            .encode("utf-8").lower()
        ).hexdigest()

        try:
            check_connection_spam(chat_id, message, redis, raw_text)
            check_banned_names(chat_id, message, redis, raw_text)
            check_message_filter(chat_id, message, redis, raw_text)
            check_warnlist(chat_id, message, redis, raw_text)


        except Mark as e:
            with session_scope() as db:
                q = db.query(Message).filter(Message.id == message["id"]).update({"spam_flag": str(e)})
                message.update({"spam_flag": str(e)})
                redis.publish("spamless:live", json.dumps(message))

        except Silence as e:
            with session_scope() as db:
                # XXX maybe cache this?
                try:
                    chat_user, user, chat = db.query(
                        ChatUser, User, AnyChat,
                    ).join(
                        User, ChatUser.user_id == User.id,
                    ).join(
                        AnyChat, ChatUser.chat_id == AnyChat.id,
                    ).filter(and_(
                        ChatUser.chat_id == chat_id,
                        ChatUser.number == message["user_number"],
                    )).one()
                except NoResultFound:
                    continue

                if chat.type != "group":
                    flag_suffix = chat.type.upper()
                elif chat_user.computed_group in ("admin", "creator"):
                    flag_suffix = chat_user.computed_group.upper()
                else:
                    flag_suffix = "SILENCED"

                db.query(Message).filter(Message.id == message["id"]).update({
                    "spam_flag": str(e) + " " + flag_suffix,
                })

                message.update({"spam_flag": str(e) + " " + flag_suffix})
                redis.publish("spamless:live", json.dumps(message))

                if flag_suffix == "SILENCED":
                    db.query(ChatUser).filter(and_(
                        ChatUser.chat_id == chat_id,
                        ChatUser.number == message["user_number"]
                    )).update({"group": "silent"})
                    send_message(db, redis, Message(
                        chat_id=chat_id,
                        type="spamless",
                        name="The Spamless",
                        acronym="\u00a7",
                        text="Spam has been detected and silenced. Please ask a chat moderator to unsilence you if this was an accident.",
                        color="626262"
                    ), force_userlist=True,
                    raw_text="Spam has been detected and silenced. Please ask a chat moderator to unsilence you if this was an accident."
)
    return

def check_connection_spam(chat_id, message, redis, raw_text):
    if message["type"] not in ("join", "disconnect", "timeout", "user_info"):
        return
    attempts = redis.increx("spamless:join:%s:%s" % (chat_id, message["user_number"]), expire=5)
    if attempts <= 10:
        return
    raise Silence("connection")

def check_banned_names(chat_id, message, redis, raw_text):
    if not message["name"]:
        return
    lower_name = message["name"].lower()
    for name in lists["banned_names"]:
        if name.search(lower_name):
            raise Silence("name")

def check_message_filter(chat_id, message, redis, raw_text):
    if message["type"] not in ("ic", "ooc", "me"):
        return

    message_key = "spamless:message:%s" % message["hash"]
    user_key = "spamless:blacklist:%s:%s" % (chat_id, message["user_number"])

    for phrase, points in lists["blacklist"]:
        total_points = len(phrase.findall(raw_text)) * int(points)
        redis.increx(message_key, expire=60, incr=total_points)
        redis.increx(user_key, expire=10, incr=total_points)

    message_attempts = redis.increx(message_key, expire=60)
    user_attempts = redis.increx(user_key, expire=10)

    if message_attempts >= randint(10, 35) or user_attempts >= 15:
        raise Silence("x%s" % max(message_attempts, user_attempts))
    elif message_attempts >= 10 or user_attempts >= 10:
        raise Mark("x%s" % max(message_attempts, user_attempts))

def check_warnlist(chat_id, message, redis, raw_text):
    if message["type"] in ("join", "disconnect", "timeout"):
        return
    lower_text = raw_text.lower()
    stripped_text = lower_text.replace(' ', '')
    for phrase in lists["warnlist"]:
        if phrase.search(lower_text) or phrase.search(stripped_text):
            raise Mark("warnlist")

def load_lists(redis):
    if lists["reload"] == redis.get("spamless:reload"):
        return

    logger.info("reload")
    lists["reload"] = redis.get("spamless:reload")

    with session_scope() as db:
        filters = db.query(SpamlessFilter).all()

        lists["banned_names"] = [
            re.compile(_.regex, re.IGNORECASE | re.MULTILINE)
            for _ in filters if _.type == "banned_names"
        ]
        lists["blacklist"] = [
            (re.compile(_.regex, re.IGNORECASE | re.MULTILINE), _.points)
            for _ in filters if _.type == "blacklist"
        ]
        lists["warnlist"] = [
            re.compile(_.regex, re.IGNORECASE | re.MULTILINE)
            for _ in filters if _.type == "warnlist"
        ]
