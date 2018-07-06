import gidgethub.routing

from . import duplicate


router = gidgethub.routing.Router(
    duplicate.router,
)
