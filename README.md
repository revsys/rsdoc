# rsdoc - Command line utility for interacting with docs.revsys.com

**NOTE**: This utility is useful **ONLY** to [REVSYS](http://www.revsys.com)
clients and staff.

## Installation

For now you need to build the Go binary yourself, we'll have it up for download soon.

## Usage

```
Manage and upload REVSYS documentation located at docs.revsys.com

Usage:
  rsdoc [command]

Available Commands:
  client      Manage clients and access
  create      Create a new set of docs with cookiecutter
  get         Retrieve information about this set of docs
  group       Manage user membership and create new doc groups
  help        Help about any command
  init        Configure a new set of docs
  open        Open these docs in your browser
  upload      Upload new or updated documentation

Flags:
      --config string    config file (default is .rsdoc.json)
  -h, --help             help for rsdoc
  -p, --path string      DocSet URL Path
  -t, --token string     DocSet Token to use
  -v, --verbose          Turn on verbose output
      --version string   Version of the DocSet to use (default "v1")

Use "rsdoc [command] --help" for more information about a command.
```

To create a new template for documentation simply run:

    rsdoc create

**NOTE**: To use the default REVSYS theme you will need to install [hugo](https://gohugo.io/) which for OSX is typically done with a simple `brew install hugo`

To upload docs, finish editing your content, generate it and then run:

    rsdoc upload ./path/to/generated/content/

So the typically workflow becomes:

1. Create docs skeleton using Cookiecutter via `rsdoc create`
1. Edit your docs in `./docs/` using `hugo server` locally to verify everything is working correctly.
1. cd into `./docs/` and run `hugo build`
1. hugo will create a `public/` directory relative to your current path with the built files.
1. To upload these run `rsdoc upload ./public/`

Assuming your `.rsdoc.json` settings are correct this will tar up the contents of the hugo generated folder and deploy them via REST to docs.revsys.com

### Open the docs

Just run `rsdoc open` the configured DocSet and Version will be opened. 

## Configuration

`rsdoc` uses an env style file named `.rsdoc` in the current directory.  Here is a simple example template that includes all of the values you need:

```
{
    "docpath": "revsys-docs",
    "version": "v1",
    "token": "68ff2d4-token-43f2065ade"
}
```

These will come from the DocSet model and associated upload Token defined in the system.

You can generate this config easily by running `rsdoc init`. It will prompt you for the 3 different values. 


## Client, Group, and User management

**NOTE** This portion is not working yet. 

If you're an admin user of docs.revsys.com you can get and set your API Token in `~/.rsdoc.json` like this:

```
{
    "admin_token": "<Your Admin Token>"
}
```

This will allow you to interact with the docs API to manage clients, groups, and putting users into clients and groups.

## Building

To build this you will need Go 1.9+ and the following dependencies: 

- go get github.com/spf13/cobra
- go get github.com/spf13/viper
- go get github.com/tcnksm/go-input
- go get github.com/skratchdot/open-golang/open

Then it's just a simple matter of: 

`go build main.go`
 
## Questions?

Contact Frank
