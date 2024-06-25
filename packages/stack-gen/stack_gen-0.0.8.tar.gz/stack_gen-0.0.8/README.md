# Stack Generator

Stack generator is a CLI tool that allows you to generate an application template in one command.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install stack generator.

```bash
pip install stack-gen
```

## Usage

```bash
sg --template=fastapi
sg --template=vuejs
```

## Help

```bash
Options:
  -t, --template [fastapi|vuejs]     The name of the template to generate:
                                     fastapi | vuejs
  --url TEXT                         GIT url of the template
  -gac, --github_access_token TEXT   GITHUB access token
                                  
  --help                             Show this message and exit.
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
