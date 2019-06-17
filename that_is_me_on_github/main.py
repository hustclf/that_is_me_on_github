import click
from github import Github, RateLimitExceededException
from that_is_me_on_github.config import VERSION
from that_is_me_on_github.lib.render import Render
from that_is_me_on_github.lib.utils import *

g = Github()


@click.group()
def that_is_me_on_github():
    pass


@that_is_me_on_github.command()
def version():
    click.echo(VERSION)


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
    "--do_auth",
    default=False,
    help="Apply github auth info will get a higher rate limit for github api, which is suggested.",
)
@click.option(
    "--auth_username",
    default="",
    prompt="Your github username",
    help="Provide github account to avoid reaching rate limit",
)
@click.option(
    "--auth_password",
    default="",
    prompt="Your github password",
    hide_input=True,
    help="Provide github account to avoid reaching rate limit",
)
def generate(
    username,
    do_auth: bool,
    auth_username: str,
    auth_password: str,
    org_filter: str,
    repo_filter: str,
):
    if do_auth and auth_username and auth_password:
        global g
        g = Github(auth_username, auth_password)

    user = single_user(g, username)
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
        owned_repos(g, username),
        issues_and_prs(g, username, type="pr", orgs=org_filter, repos=repo_filter),
        issues_and_prs(g, username, type="issue", orgs=org_filter, repos=repo_filter),
    )


if __name__ == "__main__":
    try:
        that_is_me_on_github()
    except RateLimitExceededException:
        click.echo(
            "Github rate limit reached, Please provide username, password or api_token, and try again"
        )
