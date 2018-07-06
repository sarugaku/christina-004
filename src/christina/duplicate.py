import asyncio
import logging

import gidgethub.routing

from . import actions, envs, utils


logger = logging.getLogger('duplicate')

router = gidgethub.routing.Router()


HEADER_TEMPLATES = [
    # Plural.
    "Hello there! It looks like your issue is a duplicate to {issue_list}. "
    "Kindly refer to their discussion threads for more information.",

    # Singlar.
    "Hello there! It looks like your issue is a duplicate to {issue_list}. "
    "Kindly refer to its discussion thread for more information.",
]

BLABBER_TEMPLATE = """
In there future, please remember to check for all issues in the \
[issue tracker](https://github.com/{repo}/issues) first, \
**both open and closed**.

It must be frustrating to encounter a bug. Our maintainers feel your pain. \
They are, however, volunteers spending free time helping others. \
Each duplicate issue costs valuable time to respond, and has negative impact \
on work needing to be done. \
Please be considerate, and make the best use of our available resources.

This issue is closed as a duplicate to keep the tracker tidy. \
Sorry again for the problem, and thanks so much for taking time to report it. \
Let’s work together to make Pipenv better!

🤖🌰🍚💨
"""

KEYWORDS = {
    'duplicate', 'duplicates',
    'dupe', 'dupes',
    'dup', 'dups',
}


@router.register('issue_comment', action='created')
async def close_duplicate(event, github, session):
    """Close the issue as duplicate on triggering issue comment.

    The comment should be made by a public team member, of project
    collaborator. It should mention this bot, contains one the keywords,
    and at least one issue mention.

    Example triggering comment::

        @christina-004 dup #10.

    The bot will

    1. Tag the issue with label "duplicate".
    2. Close the issue with a polite message.
    3. Delete the triggering comment.
    """
    data = event.data
    if not await actions.is_by_admin(github, data['comment']):
        return

    words = set(w.lower() for w in utils.find_words(data['comment']['body']))
    if f'@{envs.USERNAME}'.lower() not in words:
        return
    if not any(w in words for w in KEYWORDS):
        return

    ref_issue_numbers = sorted(set(utils.iter_issue_number(words)))
    if not ref_issue_numbers:
        return

    t = HEADER_TEMPLATES[0 if len(ref_issue_numbers) > 1 else 1]
    message = '\n'.join([
        t.format(issue_list=' '.join(f'#{n}' for n in ref_issue_numbers)),
        BLABBER_TEMPLATE.format(repo=envs.FUTURE_GADGET_LAB),
    ])

    current_issue_no = data['issue']['number']
    await asyncio.wait([
        actions.close(github, current_issue_no, labels=['duplicate']),
        actions.comment(github, current_issue_no, message),
        actions.delete_comment(github, data['comment']['id']),
    ])
