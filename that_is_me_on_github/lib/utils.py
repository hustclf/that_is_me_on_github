from typing import List
from typing import Dict
from github.Commit import Commit
from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository
from github import Github

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
    g: Github, username, is_public=True, type="", orgs=[], repos=[]
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
