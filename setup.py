from setuptools import setup

setup(
    name="branch2commit",
    version="0.1.0",
    py_modules=["cli"],
    entry_points={
        "console_scripts": [
            "branch2commit=cli:main"
        ]
    },
)
