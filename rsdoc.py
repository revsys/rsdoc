import click
import os
import warnings

from cookiecutter.main import cookiecutter
from envparse import env

# Load defaults from a .rsdoc file in env format
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_envfile('.rsdoc')


def handle_option_precendence(path, version, token):
    final_path = path
    final_version = version
    final_token = token

    if path is None:
        final_path = env('RSDOC_PATH', default=None)

    if version is None:
        final_version = env('RSDOC_VERSION', default=None)

    if token is None:
        final_token = env('RSDOC_TOKEN', default=None)

    # Handle missing environment variables or command line options
    # to let the user know what they are doing wrong.
    errors = []
    if final_path is None:
        errors.append('  RSDOC_PATH or --path needed')
    if final_version is None:
        errors.append('  RSDOC_VERSION or --version needed')
    if final_token is None:
        errors.append('  RSDOC_TOKEN or --token needed')

    if errors:
        click.secho('rsdoc usage errors:', fg='red')
        click.secho("\n".join(errors), fg='red')
        raise click.Abort()

    return final_path, final_version, final_token


@click.group()
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print("Help!!!")


@cli.command()
@click.option('--path', default=None, help='DocSet Path')
@click.option('--version', default=None, help='DocSet Version String')
@click.option('--token', default=None, help='DocSet Token')
@click.argument('directory', type=click.Path(exists=True))
def upload(path, version, token, directory):
    """ Create and upload docs to docs.revsys.com """

    # Can set these values
    path, version, token = handle_option_precendence(path, version, token)

    print(path)
    print(version)
    print(token)


@cli.command()
@click.option('--cookiecutter-repo-url', default='https://github.com/revsys/revsys-doc-cookiecutter')
@click.argument('directory', type=click.Path())
def create(cookiecutter_repo_url, directory):
    """ Create a new DocSet using the REVSYS cookiecutter template """
    if os.path.exists(directory):
        click.secho('ERROR: Directory {} already exists'.format(directory), fg='red')
        raise click.Abort()

    click.secho('Running cookiecutter, it will ask you some questions:', fg='green')
    cookiecutter(cookiecutter_repo_url)
    click.secho('Cookiecutter creation finished!', fg='green')
