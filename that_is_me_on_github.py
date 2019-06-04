import click
from typing import List
from typing import Dict
from github import Github, RateLimitExceededException
from github.Commit import Commit
from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository

g = Github()


class Render:
    def render(
        self,
        user_info: NamedUser,
        repos: List[Repository],
        prs: List[Issue],
        issues: List[Issue],
    ):
        tpl = self._render_user(user_info)
        tpl += self._render_repos(repos)
        tpl += self._render_prs(prs)
        tpl += self._render_issues(issues)

        click.echo(tpl)

        f = open("that_is_me_on_github.md", "w+")
        f.write(tpl)
        f.close()

    @staticmethod
    def _render_user(user_info: NamedUser):
        return """
# That Is Me On Github
## User Info
username: [{}]({})

followers: {}
        """.format(
            user_info.name, user_info.html_url, user_info.followers
        )

    @staticmethod
    def _render_repos(repos: List[Repository]):
        tpl = """
## Owned Repostories
Total: {}
        """.format(
            len(repos)
        )

        for repo in repos:
            tpl += """
* [{}]({}), folks: {}
            """.format(
                repo.name, repo.html_url, repo.forks
            )

        return tpl

    @staticmethod
    def _render_prs(prs: Dict[str, List[Issue]]):
        tpl = """
## Pull Requests
Total: {}
""".format(
            sum(len(items) for repo_name, items in prs.items())
        )
        for repo_name, items in prs.items():
            tpl += """
{}
            """.format(
                repo_name
            )
            for pr in items:
                tpl += """
* [{}]({}) \[{}\]
                """.format(
                    pr.title, pr.html_url, pr.state
                )

        return tpl

    @staticmethod
    def _render_issues(issues: Dict[str, List[Issue]]):
        tpl = """
 ## Issues:
Total: {}
        """.format(
            sum(len(items) for repo_name, items in issues.items())
        )

        for repo_name, items in issues.items():
            tpl += """
{}
            """.format(
                repo_name
            )
            for item in items:
                tpl += """
* [{}]({}) \[{}\]
                """.format(
                    item.title, item.html_url, item.state
                )

        return tpl


# build query by params
def build_query(params: str) -> str:
    return " ".join(params)


# get user info by username
def single_user(username) -> NamedUser:
    return g.get_user(username)


# get repos owned by username
def owned_repos(username, is_public=True) -> List[Repository]:
    params = ["user:{}".format(username)]

    if is_public:
        params.append("is:public")

    return [
        repo for repo in g.search_repositories(build_query(params), "stars", "desc")
    ]


# get commits authored by username and filtered by certain repos or organizations
def commits(username, is_public=True, orgs=[], repos=[]) -> List[Commit]:
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
    username, is_public=True, type="", orgs=[], repos=[]
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


@click.group()
def that_is_me_on_github():
    pass


@that_is_me_on_github.command()
@click.option("--username", help="Username of github.")
@click.option(
    "--org_filter",
    default="",
    help="Organizations you want to collect, default all organizations related with username",
)
@click.option(
    "--repo_filter",
    default="",
    help="Repositories you want to collect, default all repositories related with username",
)
@click.option(
    "--auth_username",
    default="",
    help="Provide github account to avoid reaching rate limit",
)
@click.option(
    "--auth_password",
    default="",
    help="Provide github account to avoid reaching rate limit",
)
def generate(
    username, auth_username: str, auth_password: str, org_filter: str, repo_filter: str
):
    if auth_username and auth_password:
        global g
        g = Github(auth_username, auth_password)

    user = single_user(username)
    if not user:
        click.echo("User {} Not Found.".format(username))
        click.Abort

    click.echo("Please wait for a few seconds.")

    org_filter = [item.strip() for item in org_filter.split(",")] if org_filter else []
    repo_filter = (
        [item.strip() for item in repo_filter.split(",")] if repo_filter else []
    )

    Render().render(
        user,
        owned_repos(username),
        issues_and_prs(username, type="pr", orgs=org_filter, repos=repo_filter),
        issues_and_prs(username, type="issue", orgs=org_filter, repos=repo_filter),
    )


if __name__ == "__main__":
    try:
        that_is_me_on_github()
    except RateLimitExceededException:
        click.echo(
            "Github rate limit reached, Please provide username, password or api_token, and try again"
        )
