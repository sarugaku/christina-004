import logging
import posixpath

from . import envs


HTTP_CREATED = 201

logger = logging.getLogger('actions')


def get_endpoint(*parts):
    name = posixpath.join(*parts)
    url = f'https://api.github.com/{name}'
    return url


def get_org_endpoint(*parts):
    return get_endpoint('orgs', envs.CRT_WORKSHOP, *parts)


def get_repo_endpoint(*parts):
    return get_endpoint('repos', envs.FUTURE_GADGET_LAB, *parts)


class ActionError(RuntimeError):
    pass


async def comment(github, issue_no, message):
    """Leave a comment on an issue (or pull request).
    """
    url = get_repo_endpoint('issues', issue_no, 'comments')
    data = {'body': message}
    resp = await github.post(url, data=data)
    if resp.status != HTTP_CREATED:
        logger.error(
            'Unexpected response for comment (%d) %s',
            resp.status, await resp.text,
        )
        raise ActionError(url)
    data = await resp.json()
    logger.info('Comment created at %s\n%s', data['html_url'], message)
    return data


async def is_by_admin(github, message):
    if any(value in message['author_association']
           for value in ['MEMBER', 'OWNER', 'COLLABORATOR']):
        return True
    async for item in github.getiter(get_org_endpoint('members')):
        print(item['login'])
        if item['login'] == message['user']['login']:
            return True
    return False
