import asyncio
import logging
import os

import aiohttp
import aiohttp.web as web
import cachetools
import gidgethub.aiohttp
import gidgethub.routing
import gidgethub.sansio


cache = cachetools.LRUCache(maxsize=100)    # Size is set arbitraily.

logger = logging.getLogger('')

router = gidgethub.routing.Router()


async def main(request):
    try:
        body = await request.read()
        event = gidgethub.sansio.Event.from_http(
            request.headers, body,
            secret=os.environ['GITHUB_SECRET'],
        )
        logger.info('GitHub delivery ID %(id)s', id=event.delivery_id)
        if event.event == 'ping':
            return web.Response(status=200)
        async with aiohttp.ClientSession() as session:
            github = gidgethub.aiohttp.GitHubAPI(
                session, os.environ['FUTURE_GADGET_LAB'],
                oauth_token=os.environ['GITHUB_OAUTH_TOKEN'],
                cache=cache,
            )

            # Give GitHub some time to reach internal consistency.
            await asyncio.sleep(1)
            await router.dispatch(event, github)
        return web.Response(status=200)
    except Exception as e:
        logger.exception(str(e))
        return web.Response(status=500)


def run():
    app = web.Application()
    app.router.add_post('/', main)
    try:
        port = int(os.environ['PORT'])
    except KeyError:
        port = None
    web.run_app(app, port=port)
