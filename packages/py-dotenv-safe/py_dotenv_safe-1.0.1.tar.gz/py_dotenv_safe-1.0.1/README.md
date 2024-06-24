# py-dotenv-safe

Effortlessly load and verify all your environment variables from `.env` files, ensuring they are all present and correctly configured.

`py-dotenv-safe` ensures that all required environment variables are defined after reading from `.env`. The names of the required variables are read from `.env.example`, which should be committed along with your project.

## Installation

You can install the library using pip:

```sh
pip install py-dotenv-safe
```

## Getting Started

To start using py-dotenv-safe, follow these steps:

1. Create .env and .env.example Files:
Ensure you have both .env and .env.example files in your project repository.

2. Use the Library in Your Code:
Import the library and configure it to load your environment variables.

## Usage

Here is a basic example of how to use the library:

```python
from py_dotenv_safe import config

options = {
    "dotenvPath": ".env",        # Path to the environment file
    "examplePath": ".env.example", # Path to the example environment file
    "allowEmptyValues": False,   # Set to True if you want to allow empty values
}

try:
    config(options)
    print("Environment variables loaded successfully.")
except Exception as e:
    print(f"Error: {e}")

```

### Configuration Options

- `dotenvPath` (str): Path to the `.env` file.
- `examplePath` (str): Path to the `.env.example` file.
- `allowEmptyValues` (bool): Whether to allow empty values. Defaults to `False`.

### Example

Assume you have the following `.env` file:

```
DATABASE_URL=postgres://user:password@localhost:5432/mydatabase
SECRET_KEY=mysecretkey
```

And an `.env.example` file:

```
DATABASE_URL=
SECRET_KEY=
```

Using the `config` function ensures that all required environment variables are present and correctly configured. If any variables are missing, a `MissingEnvVarsError` will be raised, indicating which variables are missing.

### Handling Missing Variables

If your provided `.env` file does not contain all the variables defined in `.env.example`, an exception is thrown:

```
MissingEnvVarsError: The following variables were defined in .env.example but are not present in the environment:
  TOKEN, KEY
Make sure to add them to .env or directly to the environment.

If you expect any of these variables to be empty, you can use the allowEmptyValues option:
config({"allowEmptyValues": True})
```

Not all the variables have to be defined in `.env`; they can be supplied externally. For example, the following would work:

```sh
$ python config.py
```

### Advanced Usage

Requiring and loading is identical:

```python
from dotenv_safe import config

config({
    "dotenvPath": ".env",
    "examplePath": ".env.example",
    "allowEmptyValues": False,
})
```

This will load environment variables from `.env` as usual, but will also read any variables defined in `.env.example`. If any variables are already defined in the environment before reading from `.env`, they will not be overwritten. If any variables are missing from the environment, a `MissingEnvVarsError` will be thrown, which lists the missing variables. Otherwise, returns an object with the following format:

```python
{
  "parsed": {"SECRET": "topsecret", "TOKEN": ""},          # parsed representation of .env
  "required": {"SECRET": "topsecret", "TOKEN": "external"} # key-value pairs required by .env.example and defined by environment
}
```

### Continuous Integration (CI)

It can be useful to depend on a different set of example variables when running in a CI environment. For example:

```python
from dotenv_safe import config

config({
    "examplePath": ".env.ci"
})
```

## Options

All options supported by `dotenv` are also supported by `py-dotenv-safe`, in addition to the options below:

```python
config({
    "dotenvPath": ".env",
    "allowEmptyValues": True,
    "examplePath": "./.my-env-example-filename"
})
```

Starting from version 1.0.0, `dotenv` is a peer dependency of `py-dotenv-safe`. This means that the actual version of `dotenv` used defaults to the latest available at install time, or whatever is specified by your application.

### `allowEmptyValues`

If a variable is defined in the example file and has an empty value in the environment, enabling this option will not throw an error after loading. Defaults to `False`.

### `examplePath`

Path to the example environment file. Defaults to `.env.example`.

### `dotenvPath`

Path to the environment file. Defaults to `.env`.

## Motivation

I regularly use apps that depend on `.env` files but don't validate if all the necessary variables have been defined correctly. Instead of having to document and validate this manually, I prefer to commit a self-documenting `.env.example` file that may have placeholder or example values filled in. This can be used as a template or starting point for an actual `.env` file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
