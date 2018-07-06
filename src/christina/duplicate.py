import gidgethub.routing

from . import actions


router = gidgethub.routing.Router()


@router.register('issue_comment', action='created')
async def close_duplicate(event, github, session):
    """Close the issue as duplicate on triggering issue comment.

    The comment should be made by a public team member, of project
    collaborator. It should mention this bot, contains the word "duplicate" or
    "dup", and at least one issue mention.

    Example triggering comment::

        @christina-004 dup #10.

    The bot will

    1. Tag the issue with label "duplicate".
    2. Close the issue with a polite message.
    3. Delete the triggering comment (if possible).
    """
    data = event.data
    if not await actions.is_by_admin(github, data['comment']['user']):
        return
    print(data)
