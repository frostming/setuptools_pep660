"""
Implement PEP 660, plus the existing setuptools PEP 517 hooks.
"""

import setuptools.build_meta

from setuptools.build_meta import *  # noqa


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    return setuptools.build_meta._BACKEND._build_with_temp_dir(
        ["editable_wheel"], ".whl", wheel_directory, config_settings
    )


def get_requires_for_build_editable(config_settings=None):
    return []
