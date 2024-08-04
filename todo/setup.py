# bertrandterrier@codeberg.org/utilities/todo/setup.py

from setuptools import setup, find_packages

# ============================================================

setup(
    name="ToDo",
    version="0.1.1",
    package=find_packages(),
    install_requires=[
        "pandas",
        "tabulate"
    ],
    entry_points={
        "console_scripts":[
            "ToDo=todo.main:main"
        ]
    }
) 