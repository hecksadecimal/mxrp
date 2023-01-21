import os
from random import randint
import re
import hashlib
import json

import sentry_sdk
from celery import Celery, Task
from celery.utils.log import get_task_logger
from sentry_sdk.integrations.celery import CeleryIntegration
from classtools import reify

from newparp.model.connections import NewparpRedis, redis_pool

if "SENTRY_PRIVATE_DSN" in os.environ:
    sentry_sdk.init(
        dsn=os.environ["SENTRY_PRIVATE_DSN"],
        integrations=[
            CeleryIntegration(),
        ],
    )

celery = Celery("newparp", include=[
    "newparp.tasks.background",
    "newparp.tasks.matchmaker",
    "newparp.tasks.reaper",
    "newparp.tasks.chat",
    "newparp.tasks.test",
    "newparp.tasks.spamless",
])

# Sentry exception logging if there is a sentry object.


celery.config_from_object('newparp.tasks.config')

class WorkerTask(Task):
    abstract = True

    @reify
    def redis(self):
        return NewparpRedis(connection_pool=redis_pool)

    def after_return(self, *args, **kwargs):
        if hasattr(self, "redis"):
            del self.redis
