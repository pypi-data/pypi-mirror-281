import click
import os


@click.command()
@click.option(
    "repository",
    "-r",
    prompt="""Welcome on stack-gen !\nRepository name containing the template to generate""",
    help="Name of the repository containing the cookicutter template",
)
@click.option(
    "--user",
    "-u",
    prompt="Github user owning the repository",
    help="Github user on which stack generator searches for template repository",
)
@click.option("--access_token", "-gac", help="GITHUB access token")
def main(repository, user, access_token):
    exit_status = os.system(f"git clone git@github.com:{user}/{repository}.git --quiet")
    if exit_status != 0:
        exit(1)

    exit_status = os.system(
        f"pip install -r {repository}/requirements.txt --quiet",
    )
    if exit_status != 0:
        os.system(f"rm -rf {repository}")
        exit(1)

    if access_token:
        with open(
            f"{repository}/app/{{{{cookiecutter.project_slug}}}}/.env", "a+"
        ) as file:
            file.write(f'\nGITHUB_ACCESS_TOKEN="{access_token}"')

    os.system(f"cookiecutter {repository}/app")
    os.system(f"rm -rf {repository}")


if __name__ == "__main__":
    main()
