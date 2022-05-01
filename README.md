# experimental-python-settings-management

Small repository that contains experiments around settings management in python.

## Features

Loading settings from a file. Configuration is defined in `config.py` and loaded in any other Python module you wish
by simply importing `settings` from `config`.

`settings` is a `Dynaconf` object but act as a normal Python dictionary.

```python
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["settings.yaml"], # load all files in this list
    folder="config", # defines the folder from where to load the files
    core_loaders=["yaml"], # defines the loader to use for the files ; Dynaconf support a lot of loaders
    envvar_prefix="MYAPP_", # defines the prefix for the environment variables loaded
    load_dotenv=True, # load the .env file
    merge_enabled=True # merge all the loaded settings together
)
```

Dynamic variables in settings files.

```yaml
postgresql:
  user: postgres
  # password will be loaded from an environment variable called NGX_FILE_MANAGER_POSTGRES_PASSWORD
  # usually, you inject those at deployment time
  password: "@format {env[MYAPP_POSTGRES_PASSWORD]}"
  host: localhost
  port: 5432
  # database variable will be set from an already defined value: postgresql.user
  database: "@format {this.postgresql.user}"
```

Validation of settings is also possible with `Dynaconf` but I prefer personally to use `dataclasses` or `pydantic`
to define validated data classes.

See the [core implementation](database.py) for more details.

## References

Here's a list of references I used to implement this project:
- https://www.dynaconf.com/
- https://github.com/rochacbruno/dynaconf