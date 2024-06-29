import logging
import sys
import time

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

RESTART_INTERVAL = getattr(settings,'AIOHTTP_RQ_BRIDGE_RESTART_INTERVAL',None)
SLEEP_INTERVAL = getattr(settings,'AIOHTTP_RQ_BRIDGE_SLEEP_INTERVAL',0.1)
QUERY = getattr(settings,'AIOHTTP_RQ_BRIDGE_QUERY',None)
RESTART_AT = None
if RESTART_INTERVAL:
    RESTART_AT = time.time()+RESTART_INTERVAL
STARTED_AT = time.time()

class Command(BaseCommand):

    def handle(self, *args, **options):
        while not RESTART_AT or time.time()<RESTART_AT:
            try:
                if QUERY:
                    cursor = connection.cursor()
                    cursor.execute(QUERY)
                call_command('aiohttp_rq_pull')
                call_command('aiohttp_rq_push')
                time.sleep(0.1)
            except Exception as e:
                logging.error(e)
                if STARTED_AT+30>time.time():
                    time.sleep(10) # slowdown restarts/logging spam
                sys.exit(1)
