import click
from github import RateLimitExceededException
from config import VERSION
from lib.render import Render
from lib.utils import *
import os
from time import time


@click.group()
def that_is_me_on_github():
    pass


@that_is_me_on_github.command()
def version():
    click.echo(VERSION)


@that_is_me_on_github.command()
@click.option("-u", "--username", help="Username of github.")
@click.option(
    "--org_filter",
    default="",
    type=str,
    help="Organizations you want to collect, default all organizations related with username.",
)
@click.option(
    "--repo_filter",
    default="",
    type=str,
    help="Repositories you want to collect, default all repositories related with username.",
)
@click.option(
    "--do_auth",
    default=False,
    type=bool,
    help="Provide github auth info will get a higher rate limit for github api, which is recommended.",
)
@click.option(
    "--auth_username",
    default=None,
    type=str,
    help="Provide github account to avoid reaching rate limit.",
)
@click.option(
    "--auth_password",
    default=None,
    type=str,
    hide_input=True,
    help="Provide github account to avoid reaching rate limit.",
)
@click.option(
    "-o",
    "--output",
    default="that_is_me_on_github.md",
    type=click.Path(),
    help="The output markdown file path. default value is `./that_is_me_on_github.md`",
)
def generate(
        username: str,
        do_auth: bool,
        auth_username: str,
        auth_password: str,
        org_filter: str,
        repo_filter: str,
        output: str,
):
    start = time()
    path = os.path.expanduser(output)
    try:
        f = open(path, "w+")
        f.close()
    except IOError:
        click.echo("Error: output path not exist and not creatable.")
        raise click.Abort()
    
    try:
        if do_auth:
            if not auth_username:
                auth_username = click.prompt("Your github username", type=str)
            if not auth_password:
                auth_password = click.prompt(
                    "Your github password", type=str, hide_input=True
                )
            
            g = Github(auth_username, auth_password)
        else:
            g = Github()
        
        click.echo("Please wait for a few seconds.")
        
        org_filter = (
            [item.strip() for item in org_filter.split(",")] if org_filter else []
        )
        repo_filter = (
            [item.strip() for item in repo_filter.split(",")] if repo_filter else []
        )
        
        container = [
            {"func": owned_repos, "args": [g, username]},
            {"func": issues_and_prs, "args": [g, username], "kwargs": {'type': "pr",
                                                                       'orgs': org_filter,
                                                                       'repos': repo_filter}},
            {"func": single_user, "args": [g, username]},
            {"func": issues_and_prs, "args": [g, username], "kwargs": {'type': "issue",
                                                                       'orgs': org_filter,
                                                                       'repos': repo_filter}},
            
        ]
        t3 = time()
        results = handle_tasks(container)
        if not results[2]:
            click.echo("User {} Not Found.".format(username))
            raise click.Abort()
        
        t4 = time()
        click.echo(f"request github cost time: {t4 - t3}")
        
        t5 = time()
        Render().render(
            results[2],
            results[0],
            results[1],
            results[3],
            path,
        )
        t6 = time()
        click.echo(f"render cost time: {t6 - t5}")
        end = time()
        click.echo(f"cost time {end - start} seconds")
    except RateLimitExceededException:
        click.echo(
            "Github rate limit reached, Please provide username, password or api_token (not support yet), and try again"
        )


if __name__ == "__main__":
    that_is_me_on_github()
