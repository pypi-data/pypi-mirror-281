""" This module provides utility methods for retrieving the version of the library. """

import os
import requests


class VersionUtil:
    """Provides utility methods for retrieving the version of the library."""

    def __init__(self):
        """
        Initializes a new instance of the VersionUtil class.
        """
        self.version = self.get_version()

    @staticmethod
    def get_version():
        """
        Retrieves the version of the library.

        Returns:
            str: The version of the library.
        """
        current_dir = os.path.dirname(os.path.realpath(__file__))
        pyproject_toml = os.path.join(current_dir, "..", "..", "pyproject.toml")
        if os.path.exists(pyproject_toml):
            with open(pyproject_toml, "r", encoding="UTF-8") as f:
                for line in f:
                    if "version = " in line:
                        version = line.split("=")[1].strip().replace('"', "")
                        return version
        else:
            return VersionUtil.get_version_from_gh()
        return "0.0.0"

    @staticmethod
    def get_version_from_gh():
        """
        Retrieves the latest version of the library from GitHub.

        Returns:
            str: The latest version of the library.
        """
        url = "https://api.github.com/repos/remla24-team8/lib-version/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["tag_name"]
        return "9.9.9"
