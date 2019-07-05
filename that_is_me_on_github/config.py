from enum import unique

from lib.utils import StrEnum

VERSION = "v0.0.4"


@unique
class TaskNameEnum(StrEnum):
    PR = "pr"
    ISSUE = "issue"
    USER = "single_user"
    OWNED_REPOS = "owned_repos"
