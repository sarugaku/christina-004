import asyncio
import logging

import aiohttp
import aiohttp.web as web
import cachetools
import gidgethub.aiohttp
import gidgethub.sansio

from . import envs
from .routers import router


cache = cachetools.LRUCache(maxsize=100)    # Size is set arbitraily.

logger = logging.getLogger('')


async def main(request):
    try:
        body = await request.read()
        event = gidgethub.sansio.Event.from_http(
            request.headers, body,
            secret=envs.GITHUB_SECRET,
        )
        logger.debug('GitHub delivery ID %s', event.delivery_id)
        if event.event == 'ping':
            return web.Response(status=200)
        async with aiohttp.ClientSession() as session:
            github = gidgethub.aiohttp.GitHubAPI(
                session, envs.USERNAME,
                oauth_token=envs.GITHUB_TOKEN,
                cache=cache,
            )

            # Give GitHub some time to reach internal consistency.
            await asyncio.sleep(1)
            await router.dispatch(event=event, github=github, session=session)
        return web.Response(status=200)
    except Exception as e:
        logger.exception(str(e))
        return web.Response(status=500)


def run():
    app = web.Application()
    app.router.add_post('/', main)
    try:
        port = int(envs.PORT)
    except KeyError:
        port = None
    logger.info('Starting server at %d', port)
    web.run_app(app, port=port)
