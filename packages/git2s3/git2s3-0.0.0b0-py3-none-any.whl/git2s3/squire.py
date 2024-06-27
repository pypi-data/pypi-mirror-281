import json
import logging
import os
import pathlib
from datetime import datetime
from typing import Dict

import yaml

from git2s3 import config


def env_loader(filename: str | os.PathLike) -> config.EnvConfig:
    """Loads environment variables based on filetypes.

    Args:
        filename: Filename from where env vars have to be loaded.

    Returns:
        config.EnvConfig:
        Returns a reference to the ``EnvConfig`` object.
    """
    env_file = pathlib.Path(filename)
    if env_file.suffix.lower() == ".json":
        with open(env_file) as stream:
            env_data = json.load(stream)
        return config.EnvConfig(**{k.lower(): v for k, v in env_data.items()})
    elif env_file.suffix.lower() in (".yaml", ".yml"):
        with open(env_file) as stream:
            env_data = yaml.load(stream, yaml.FullLoader)
        return config.EnvConfig(**{k.lower(): v for k, v in env_data.items()})
    elif not env_file.suffix or env_file.suffix.lower() in (
        ".text",
        ".txt",
        "",
    ):
        return config.EnvConfig.from_env_file(env_file)
    else:
        raise ValueError(
            "\n\tUnsupported format for 'env_file', can be one of (.json, .yaml, .yml, .txt, .text, or null)"
        )


def source_detector(repo: Dict[str, str], env: config.EnvConfig) -> config.DataStore:
    """Detects the type of source to clone and returns the DataStore model.

    Args:
        repo: Repository information as a dict.
        env: Environment configuration.

    Returns:
        config.DataStore:
        DataStore model.
    """
    if repo.get("comments_url") == f"{env.git_api_url}/gists/{repo['id']}/comments":
        return config.DataStore(
            source=config.SourceControl.gist,
            clone_url=repo["git_pull_url"],
            name=repo["id"],
            description=repo["description"],
            private=not repo["public"],
        )
    return config.DataStore(
        source=config.SourceControl.repo,
        clone_url=repo["clone_url"],
        name=repo["name"],
        description=repo["description"],
        private=repo["private"],
    )


def default_logger(env: config.EnvConfig) -> logging.Logger:
    """Generates a default console logger.

    Args:
        env: Environment configuration.

    Returns:
        logging.Logger:
        Logger object.
    """
    if env.log == config.LogOptions.file:
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        logfile: str = datetime.now().strftime(
            os.path.join("logs", "pyfilebrowser_%d-%m-%Y.log")
        )
        handler = logging.FileHandler(filename=logfile)
    else:
        handler = logging.StreamHandler()
    logger = logging.getLogger(__name__)
    if env.debug:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.INFO)
    handler.setFormatter(
        fmt=logging.Formatter(
            fmt="%(asctime)s - %(levelname)-8s - [%(funcName)s:%(lineno)d] - %(message)s"
        )
    )
    logger.addHandler(hdlr=handler)
    return logger


def check_file_presence(root: str | os.PathLike) -> bool:
    """Get a list of all subdirectories and check for file presence.

    Args:
        root: Root directory to check for file presence.

    Returns:
        bool:
        Returns a bool indicating if files are present in the subdirectories.
    """
    for subdir in [
        os.path.join(root, subdir)
        for subdir in os.listdir(root)
        if os.path.isdir(os.path.join(root, subdir))
    ]:
        if [
            file
            for file in os.listdir(subdir)
            if os.path.isfile(os.path.join(subdir, file))
        ]:
            return True
    return False
