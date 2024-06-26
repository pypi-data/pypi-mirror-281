from setuptools import setup, find_packages

# Read the contents of your README and CHANGELOG files
with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('CHANGELOG.md', 'r') as ch:
    long_description += "\n\n" + ch.read()

setup(
    name="b-utils-infra",
    version="0.1.0",
    author="Fahad Mawlood",
    author_email="fahadukr@gmail.com",
    description="A collection of utility functions and classes for Python projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fahadukr/b-utils-infra",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy >= 2.0.0",
        "pandas >= 2.0.0",
        "numpy < 2.0.0",
        "google-cloud-translate == 2.0.4",
        "openai >= 1.11.1",
        "slack-sdk",
        "tiktoken",
        "deepl",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
