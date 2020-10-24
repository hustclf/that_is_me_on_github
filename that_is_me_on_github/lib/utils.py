from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from github import Github
from github.Commit import Commit
from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository
from typing import Dict
from typing import List


# build query by params
def build_query(params: str) -> str:
    return " ".join(params)


# get user info by username
def single_user(g: Github, username: str) -> NamedUser:
    return g.get_user(username)


# get repos owned by username
def owned_repos(g: Github, username, is_public=True) -> List[Repository]:
    params = ["user:{}".format(username)]

    if is_public:
        params.append("is:public")

    return [
        repo for repo in g.search_repositories(build_query(params), "stars", "desc")
    ]


# get commits authored by username and filtered by certain repos or organizations
def commits(g: Github, username, is_public=True, orgs=[], repos=[]) -> List[Commit]:
    params = ["author:{}".format(username)]
    if is_public:
        params.append("is:public")

    if orgs or repos:
        for org in orgs:
            params.append("org:{}".format(org))

        for repo in repos:
            params.append("repo:{}".format(repo))

    return [
        commit
        for commit in g.search_commits(build_query(params), "author-date", "desc")
    ]


# get issues or prs authored by username and filtered by certain repos and organizations
def issues_and_prs(
        g: Github, username: str, is_public=True, type="", orgs=[], repos=[]
) -> Dict[str, List[Issue]]:
    params = ["author:{}".format(username)]

    if type:
        params.append("type:{}".format(type))

    if is_public:
        params.append("is:public")

    if orgs or repos:
        for org in orgs:
            params.append("org:{}".format(org))

        for repo in repos:
            params.append("repo:{}".format(repo))

    issues_and_prs = {}
    for issue_or_pr in g.search_issues(build_query(params), "updated", "desc"):
        if issue_or_pr.repository.name not in issues_and_prs:
            issues_and_prs[issue_or_pr.repository.name] = [issue_or_pr]
        else:
            issues_and_prs[issue_or_pr.repository.name].append(issue_or_pr)

    return issues_and_prs


class StrEnum(str, Enum):
    def __new__(cls, *args):
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError('Not str: {}'.format(arg))
        return super(StrEnum, cls).__new__(cls, *args)


def handle_tasks(tasks):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for task in tasks:
            fn, args = task["func"], task["args"]
            kwargs = task.get("kwargs", {})  # type: dict
            name = task.get("name", fn.__name__)
            future = executor.submit(fn, *args, **kwargs)
            setattr(future, "name", name)
            futures.append(future)
        results = {future.name: future.result() for future in futures}
        return results
