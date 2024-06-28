from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple, TypedDict

import yaml


class Resource(TypedDict, total=False):
    path: str
    connection: Optional[str]
    storagePath: Optional[str]
    output_path: Optional[str]


class Coordinates(TypedDict):
    x: int
    y: int
    w: int
    h: int


class Job(TypedDict):
    name: str
    schedule: str
    timezone: str


class CanvasAlias(TypedDict):
    coordinates: Coordinates
    parents: Optional[List[str]]


class Canvas(TypedDict, total=False):
    jobs: Optional[Job]
    cells: Dict[str, CanvasAlias]


class Config(TypedDict):
    version: str
    resources: Dict[str, Resource]
    canvases: Dict[str, Canvas]


MORPH_CONFIG_NAME = "morph.yaml"


class MorphConfig:
    def __init__(self):
        def find(start_dir: str) -> Tuple[str, Dict]:
            current_dir = start_dir
            while True:
                morph_config_path = os.path.join(current_dir, MORPH_CONFIG_NAME)
                if os.path.isfile(morph_config_path):
                    with open(morph_config_path, encoding="utf-8") as f:
                        config = yaml.safe_load(f)
                    return os.path.dirname(morph_config_path), config

                parent_dir = os.path.dirname(current_dir)
                if current_dir == parent_dir:
                    break

                current_dir = parent_dir
            return None

        current_dir = os.getcwd()

        config_path, config = find(current_dir)
        if config_path is None or config is None:
            raise Exception("morph.yaml not found")

        self.config = Config(**config)
        self.config_path = config_path

    def get_config(self) -> Config:
        return self.config

    def get_config_path(self) -> str:
        return self.config_path

    def get_filepath(self, alias: str) -> Optional[str]:
        resource = self.config["resources"].get(alias)
        return (
            os.path.join(self.config_path, os.path.relpath(resource["path"]))
            if resource and "path" in resource
            else None
        )

    def get_connection(self, alias: str) -> Optional[str]:
        resource = self.config["resources"].get(alias)
        return resource["connection"] if resource and "connection" in resource else None

    def get_alias(self, abs_path: str) -> str:
        for alias, resource in self.config["resources"].items():
            if (
                os.path.join(self.config_path, os.path.relpath(resource["path"]))
                == abs_path
            ):
                return alias
        return None

    def get_output_path(self, alias: str) -> Optional[str]:
        resource = self.config["resources"].get(alias)
        # default output path(/path/to/config/src/data/outputs/output_{alias})
        return (
            os.path.join(self.config_path, os.path.realpath(resource["output_path"]))
            if resource and "output_path" in resource
            else os.path.join(
                self.config_path, "src", "data", "outputs", f"output_{alias}"
            )
        )

    @staticmethod
    def get_cell_type(filepath: str) -> str:
        ext = os.path.splitext(filepath)[1][1:]
        if ext == "sql":
            return "sql"
        elif ext == "py":
            return "python"
        elif ext == "":
            return "directory"
        else:
            return "file"

    @staticmethod
    def get_code(path_to_config_dir: str, filepath: str) -> str:
        path = (
            os.path.join(path_to_config_dir, filepath)
            if not filepath.startswith(path_to_config_dir)
            else filepath
        )
        with open(path, "r") as f:
            return f.read()
