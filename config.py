import os

from dynaconf import Dynaconf

ENV_VAR_PREFIX = "NGX"


def get_settings_files_from_env():
    """Get the settings files from the environment variables."""
    environment = os.environ.get(f"{ENV_VAR_PREFIX}_ENV", "local")
    settings_files = ["settings.yaml", f"settings-{environment}.yaml"]
    return settings_files


settings = Dynaconf(
    settings_files=get_settings_files_from_env(),
    folder="config",
    core_loaders=["yaml"],
    envvar_prefix=ENV_VAR_PREFIX,
    load_dotenv=True,
    merge_enabled=True
)
