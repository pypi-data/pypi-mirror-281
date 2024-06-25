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
  -r, --github_repository TEXT       Name of repository containing the template to generate
  --u TEXT                           Name of github's user owning the repository
  -gac, --github_access_token TEXT   Github access token used to manage branch protection on generation (optional)
                                  
  --help                             Show this message and exit.
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Deploy a new version

```bash
pip install wheel
cd stack-gen
python setup.py sdist bdist_wheel
twine upload dist/*
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
