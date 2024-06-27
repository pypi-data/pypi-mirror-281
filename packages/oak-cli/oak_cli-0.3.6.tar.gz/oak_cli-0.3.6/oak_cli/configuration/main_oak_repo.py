import pathlib

import typer

from oak_cli.configuration.auxiliary import ConfigKey, prompt_for_path
from oak_cli.configuration.common import (
    check_and_handle_config_file,
    get_config_value,
    handle_missing_key_access_attempt,
    update_config_value,
)
from oak_cli.utils.typer_augmentations import AliasGroup

app = typer.Typer(cls=AliasGroup)


def get_main_oak_repo_path_from_config() -> pathlib.Path:
    check_and_handle_config_file()
    config_string = get_config_value(ConfigKey.MAIN_OAK_REPO_PATH_KEY)
    handle_missing_key_access_attempt(
        config_string_key=config_string,
        what_should_be_found="main oakestra repository path",
    )
    return pathlib.Path(config_string)


@app.command(
    "configure",
    help="Configure the path to the main oakestra repo.",
)
def configure_main_oak_repo_path() -> None:
    # NOTE: There is no support for paths as input params with proper autocomplete.
    main_oak_repo = prompt_for_path(path_name="the main oakestra repository")
    check_and_handle_config_file()
    update_config_value(
        key=ConfigKey.MAIN_OAK_REPO_PATH_KEY,
        value=str(main_oak_repo),
    )
