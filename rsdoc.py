import click
import glob
import os
import requests
import tarfile
import tempfile
import warnings

from cookiecutter.main import cookiecutter
from envparse import env

# Load defaults from a .rsdoc file in env format
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    env.read_envfile('.rsdoc')


def upload_option_precendence(path, version, token):
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


def api_path(base_url, path):
    """ Build the API URL with base + path """
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    if path.startswith('/'):
        path = path[1:]

    return "{}/{}".format(base_url, path)


@click.group()
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print("Help!!!")


@cli.command()
@click.option('--path', default=None, help='DocSet Path')
@click.option('--version', default=None, help='DocSet Version String')
@click.option('--token', default=None, help='DocSet Token')
@click.option('--api-url', default='https://docs.revsys.com', help='Base API Endpoint')
@click.argument('directory', type=click.Path(exists=True))
def upload(path, version, token, directory, api_url):
    """ Create and upload docs to docs.revsys.com """

    # Can set these values
    path, version, token = upload_option_precendence(path, version, token)

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


@cli.command()
def init():
    """ Generate a .rsdoc file based on commandline options or prompts """
    if os.path.exists('./.rsdoc'):
        click.secho("ERROR: .rsdoc already exists, remove it or edit it yourself", fg='red')
        raise click.Abort()

    click.secho("Generating a new .rsdoc file, but we need some info from you:", fg='green')
    path = click.prompt('The docset path', type=str)
    version = click.prompt('The docset version', type=str)
    token = click.prompt('The docset upload token', type=str)

    with open('./.rsdoc', 'w') as f:
        f.write("""RSDOC_PATH="{}"\n""".format(path))
        f.write("""RSDOC_VERSION="{}"\n""".format(version))
        f.write("""RSDOC_TOKEN="{}"\n""".format(token))

    click.secho("\n.rsdoc file generated, it's contents are:\n", fg='green')

    f = open('./.rsdoc')
    for line in f:
        print(line.strip())

    click.secho("\nDONE", fg='green')


######################################################################
# Admin only related functions
######################################################################
def get_auth_token():
    """ Get admin API token or abort """
    token = env('RSDOC_API_TOKEN', None)

    home_path = os.path.expanduser('~/.rsdoc')

    if token is None and os.path.exists(home_path):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            env.read_envfile(home_path)
            token = env('RSDOC_API_TOKEN', None)

    if token is None:
        click.secho('ERROR: Cannot find your admin API token in RSDOC_API_TOKEN, please set it in the environment or in ~/.rsdoc')
        raise click.Abort()

    return token


def api(url, token, data=None, method="GET"):
    if method == "GET":
        r = requests.get(
            url,
            headers={'Authorization': 'Token {}'.format(token)}
        )

        if r.status_code != 200:
            click.secho('ERROR: API Returned Status {}'.format(r.status_code), fg='red')
            click.secho(r.content)
            raise click.Abort()

    else:
        r = requests.post(
            url,
            data=data,
            headers={'Authorization': 'Token {}'.format(token)}
        )

        if r.status_code < 200 or r.status_code >= 300:
            click.secho('ERROR: API Returned Status {}'.format(r.status_code), fg='red')
            click.secho(str(r.json()))
            raise click.Abort()

    return r


def list_clients(base_url, token):
    """ Retrieve existing clients from the API """
    r = api(api_path(base_url, '/api/v1/clients/?page_size=500'), token)
    data = r.json()
    click.secho("{:<40}  Name".format('Client Slug'), fg='green')

    for item in data['results']:
        click.echo("{:<40}  {}".format(item['slug'], item['name']))

    click.secho("DONE", fg='green')


def create_client(base_url, token):
    """ Create a new client if it doesn't exist, prompting for slug and name """
    click.secho('Creating new Client...', fg='green')
    slug = click.prompt('New slug')
    name = click.prompt('Display Name')
    data = {
        'slug': slug,
        'name': name,
    }

    click.secho('Calling API...', fg='green')

    r = api(api_path(base_url, '/api/v1/clients/'), token, data=data, method="POST")
    import pprint
    pprint.pprint(r.json())
    click.secho('Client Created', fg='green')


@cli.command()
@click.option('--create', is_flag=True, help="Create new client")
@click.option('--add', default=None, help="Add user to Client")
@click.option('--ls', is_flag=True, help="List clients")
@click.option('--api-url', default='https://docs.revsys.com', help='API Base URL')
def client(create, add, ls, api_url):
    """ Manage clients """
    token = get_auth_token()

    if not any([create, add, ls]):
        click.secho("Manage clients")
        click.secho("  --create will create a new client")
        click.secho("  --add will add a user to a client")
        click.secho("  --ls lists all clients")
        return

    if ls is True:
        list_clients(api_url, token)
        return

    if create is True:
        create_client(api_url, token)
        return

    if add:
        print("Add a user {}".format(add))
        return

