import logging
import posixpath

from . import envs


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204

logger = logging.getLogger('actions')


def get_endpoint(*parts):
    name = posixpath.join(*(str(p) for p in parts))
    url = f'https://api.github.com/{name}'
    return url


def get_org_endpoint(*parts):
    return get_endpoint('orgs', envs.CRT_WORKSHOP, *parts)


def get_repo_endpoint(*parts):
    return get_endpoint('repos', envs.FUTURE_GADGET_LAB, *parts)


async def comment(github, issue_no, message):
    """Leave a comment on an issue (or pull request).
    """
    url = get_repo_endpoint('issues', issue_no, 'comments')
    data = {'body': message}
    data = await github.post(url, data=data)
    logger.info('Comment created at %s\n%s', data['html_url'], message)
    return data


async def close(github, issue_no, labels=None):
    """Close an issue, optionally with labels replaced.
    """
    data = {'state': 'closed'}
    if labels is not None:
        data['labels'] = labels
    url = get_repo_endpoint('issues', issue_no)
    data = await github.patch(url, data=data)
    logger.info('Closed #%s', issue_no, extra={'labels': labels})
    return data


async def delete_comment(github, comment_id):
    """Delete a comment.
    """
    url = get_repo_endpoint('issues', 'comments', comment_id)
    await github.delete(url)
    logger.info('Deleted comment %s', comment_id)


async def is_by_admin(github, message):
    """Check if a message is made by a project admin.
    """
    if any(value in message['author_association']
           for value in ['MEMBER', 'OWNER', 'COLLABORATOR']):
        return True
    async for item in github.getiter(get_org_endpoint('members')):
        if item['login'] == message['user']['login']:
            return True
    return False
