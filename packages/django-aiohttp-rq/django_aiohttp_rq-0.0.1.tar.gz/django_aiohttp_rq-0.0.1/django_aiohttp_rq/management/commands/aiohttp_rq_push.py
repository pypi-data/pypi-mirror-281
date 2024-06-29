import json

from django.conf import settings
from django.core.management.base import BaseCommand

from aiohttp_rq.redis_client import REDIS, REQUEST_QUEUE as QUEUE
from ...models import Request

class Command(BaseCommand):
    def handle(self, *args, **options):
        request_list = list(Request.objects.all())
        if request_list:
            data_list = []
            for request in request_list:
                data_list+=[dict(
                    id=request.id,
                    url=request.url,
                    method=request.method,
                    headers=request.headers,
                    data=request.data,
                    allow_redirects=request.allow_redirects
                )]
            if settings.DEBUG:
                self.stdout.write('PUSH %s (%s)\n' % (QUEUE,len(request_list)))
            pipe = REDIS.pipeline()
            for data in data_list:
                REDIS.lpush(QUEUE, json.dumps(data))
            pipe.execute()
            id_list = list(map(lambda r:r.id,request_list))
            Request.objects.filter(id__in=id_list).delete()
