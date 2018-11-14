from setuptools import setup

setup(
    name='nlp-data-py',

    entry_points={
        'console_scripts': [
            'peace=dataset.command_line:peace',
        ],
    },
)