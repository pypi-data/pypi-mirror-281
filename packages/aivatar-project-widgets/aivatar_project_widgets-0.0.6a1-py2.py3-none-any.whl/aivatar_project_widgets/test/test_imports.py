# -*- coding: utf-8 -*-
"""Import Test."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import importlib
import pkgutil

# Import third-party modules
import aivatar_project_widgets


def test_imports():
    """Test import modules."""
    prefix = "{}.".format(aivatar_project_widgets.__name__)
    iter_packages = pkgutil.walk_packages(
        aivatar_project_widgets.__path__,  # noqa: WPS609
        prefix,
    )
    for _, name, _ in iter_packages:
        module_name = name if name.startswith(prefix) else prefix + name
        importlib.import_module(module_name)
