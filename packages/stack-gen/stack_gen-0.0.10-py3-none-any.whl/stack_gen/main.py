import click
import os


@click.command()
@click.option(
    "--github_repository",
    "-r",
    prompt="""- - - Welcome on stack-gen ! - - -\n
Repository name containing the template:
""",
    help="Name of the repository containing the cookicutter template",
)
@click.option(
    "--github_user",
    "-u",
    prompt="Github user owner:",
    help="Github user on which stack generator searches for template repository",
)
@click.option("--github_access_token", "-gac", help="GITHUB access token")
def main(repository, github_user, github_access_token):
    os.system(f"git clone git@github.com:{github_user}/{repository}.git --quiet")
    os.system(
        f"python3 -m pip install -r {repository}/requirements.txt --quiet",
    )
    if github_access_token:
        with open(
            f"{repository}/app/{{{{cookiecutter.project_slug}}}}/.env", "a+"
        ) as file:
            file.write(f'\nGITHUB_ACCESS_TOKEN="{github_access_token}"')

    os.system(f"cookiecutter {repository}/app")
    os.system(f"rm -rf {repository}")


if __name__ == "__main__":
    main()
