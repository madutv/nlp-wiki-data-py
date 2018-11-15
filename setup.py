import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nlp-data-py',
    version="0.0.1",
    author="Madhu TV",
    author_email="madhavi.tv@gmail.com",
    description="Create Test, Train and Validation datasets for NLP. "
                "Currently, creating these datasets from wikipedia is supported",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'peace=dataset.command_line:peace',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
