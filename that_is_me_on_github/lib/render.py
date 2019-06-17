import click
from typing import List
from typing import Dict
from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository


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
        return """# That Is Me On Github
## User Info
username: [{}]({})

email: [{}]({})

followers: {}

![avatar]({} "avatar")

        """.format(
            user_info.name,
            user_info.html_url,
            user_info.email,
            user_info.email,
            user_info.followers,
            user_info.avatar_url,
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
* [{}]({}), stars: {}, folks: {}
            """.format(
                repo.name, repo.html_url, repo.stargazers_count, repo.forks
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
* [{}]({}) \[{}\] \[{}\]
                """.format(
                    pr.title,
                    pr.html_url,
                    pr.state,
                    "merged" if pr.as_pull_request().is_merged() else "not_merged",
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
