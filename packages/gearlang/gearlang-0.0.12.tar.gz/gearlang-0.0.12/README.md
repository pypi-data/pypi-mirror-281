# Gear

Gear is a logic based compiler for the Gear language. 


## Installation

```bash
pip install gearlang
```

## Development

First, make sure you have ``poetry`` installed and then build the project using the following command:
```bash
pip install poetry
```

Don't forget to add your Python installation's Scripts directory to your PATH if you haven't already. [Here](https://bobbyhadz.com/blog/python-the-script-is-installed-in-which-is-not-on-path) is a guide on how to do it.

Then, you can build the project using the following commands:
```bash
poetry build
poetry install
```
You can then interact with the CLI using the following command:
```bash
poetry run gear
```

To update ``pyproject.toml`` after adding a new dependency, use the following command:
```bash	
poetry lock
```

### Compiling Grammar

```bash
./scripts/compile-antlr.bat
```

### Compiling Gear

#### As C Library
```bash
make lib
```

#### As Binaries
##### On current OS
```bash
make build
```

##### All targets
Only on Linux and MacOS or WSL/Git Bash on Windows
```bash
make compile-all
```


## Troubleshooting

If the CLI is not working, make sure that the Scripts directory of your Python installation is in your PATH. [Here](https://bobbyhadz.com/blog/python-the-script-is-installed-in-which-is-not-on-path) is a guide on how to do it.

---
License - [MIT](./LICENSE)