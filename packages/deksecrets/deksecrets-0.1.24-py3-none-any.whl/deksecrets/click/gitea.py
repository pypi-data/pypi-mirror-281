import sys
import typer
from typing import List
from getpass import getpass
from dektools.shell import output_data
from dektools.variables import get_user_email_from_git
from ..tools.gitea import GiteaManager

app = typer.Typer(add_completion=False)

default_name = 'default'


@app.command()
def login(url, token=None, username=None, password=None, name=default_name):
    if not username and not token:
        token = getpass('Please input token:')
    if not token:
        if not username:
            du, _ = get_user_email_from_git()
            if du:
                fmt = f"({du})"
            else:
                fmt = ""
            username = input(f'Please input username{fmt}:')
            if not username:
                username = du
        if not password:
            password = getpass('Please input password:')
    GiteaManager(name).login(url, dict(token=token, username=username, password=password))


@app.command()
def logout(name=default_name):
    GiteaManager(name).logout()


@app.command()
def init(name=default_name):
    sys.stdout.write(GiteaManager(name).init())


@app.command()
def upload(name=default_name):
    GiteaManager(name).upload()


@app.command()
def fetch(org_project_tag_environment, path=None, out=None, fmt=None, prefix=None, name=default_name):
    org, project, tag, environment = org_project_tag_environment.split('/')
    data = GiteaManager(name).fetch(org, project, tag, environment, path)
    output_data(data, out, fmt, prefix)


@app.command()
def clone(orgs: List[str], name=default_name):
    GiteaManager(name).fetch_all(orgs)
