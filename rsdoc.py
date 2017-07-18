import click
import glob
import os
import requests
import subprocess
import tarfile
import tempfile
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

    # Make tarfile in a temp file
    tmpfile = tempfile.NamedTemporaryFile(delete=False)

    with tarfile.open(fileobj=tmpfile, mode="w:gz") as tar:

        old_cwd = os.getcwd()
        os.chdir(directory)
        for filename in glob.iglob('*'):
            tar.add(filename, recursive=True)

        os.chdir(old_cwd)

    tmpfile.close()

    # Upload it to the API
    api_base = 'http://localhost/api/v1/upload'
    filename = "{path}-{version}-{random}.tar.gz".format(
        path=path,
        version=version,
        random=os.path.basename(tmpfile.name),
    )

    url = "{base}/{path}/{version}/{filename}/".format(
        base=api_base,
        path=path,
        version=version,
        filename=filename
    )

    fp = open(tmpfile.name, 'rb')

    r = requests.post(
        url=url,
        files={'file': fp},
        headers={'Authorization': 'Token {}'.format(token)}
    )

    fp.close()
    os.unlink(tmpfile.name)

    if r.status_code == 200:
        click.secho("Docset updated", fg='green')
    elif r.status_code == 201:
        click.secho("New Docset version created", fg='green')
    else:
        click.secho("Upload error:", fg='red')
        click.secho(r.json())


@cli.command()
@click.option('--cookiecutter-repo-url', default='https://github.com/revsys/revsys-doc-cookiecutter')
def create(cookiecutter_repo_url):
    """ Create a new DocSet using the REVSYS cookiecutter template """

    # Create the docs using cookiecutter
    click.secho('Running cookiecutter, it will ask you some questions:', fg='green')
    cookiecutter(cookiecutter_repo_url)
    click.secho('Cookiecutter creation finished!', fg='green')
