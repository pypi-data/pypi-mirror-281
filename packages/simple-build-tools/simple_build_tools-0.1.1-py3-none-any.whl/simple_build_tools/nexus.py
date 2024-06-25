""" Setup PIP and Poetry for publishing to Nexus and using Nexus as the primery source """
import os
import subprocess
from .environment_tools import setup_pypi, read_credentials


def configure_python_for_nexus():
    """ Configure Python to publish to Nexus """
    print("Configuring Python to publish to Nexus")

    # Upgrade pip to the latest version
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # Write the .pypirc file and the ~/.config/pip/pip.conf file
    setup_pypi()

    # List the configuration
    subprocess.run(["pip", "config", "list"], check=True)

    # Install all the dependencies this project needs
    subprocess.run(["pip", "install", "poetry", "poetry-dynamic-versioning"], check=True)
    subprocess.run(["pip", "install", "pyinstaller"], check=True)

    print('Add the Nexus repository to the list of poetry sources as the "primary" source')
    nexus_server, repository, nexus_username, nexus_password = read_credentials("credentials-read")

    if not all([nexus_server, nexus_username, nexus_password]):
        raise ValueError("NEXUS_SERVER, NEXUS_USERNAME, and NEXUS_PASSWORD environment variables must be set")

    if not nexus_server.startswith("https://"):
        nexus_server = f"https://{nexus_server}"

    subprocess.run(["poetry", "source", "add", "--priority=primary", "nexus", f"{nexus_server}{repository}/simple/"], check=True)
    subprocess.run(["poetry", "source", "add", "--priority=explicit", "PyPI"], check=True)

    # Password for our 'nexus' server
    subprocess.run(["poetry", "config", "http-basic.nexus", nexus_username, nexus_password], check=True)

    print('Add a publishing location with "poetry publish --repository nexus-releases"')
    nexus_server, repository, nexus_username, nexus_password = read_credentials("credentials-write")

    if not all([nexus_server, nexus_username, nexus_password]):
        raise ValueError("NEXUS_SERVER, NEXUS_USERNAME, and NEXUS_PASSWORD environment variables must be set")

    if not nexus_server.startswith("https://"):
        nexus_server = f"https://{nexus_server}"

    subprocess.run(["poetry", "config", "repositories.nexus-releases", f"{nexus_server}{repository}/"], check=True)
    subprocess.run(["poetry", "config", "http-basic.nexus-releases", nexus_username, nexus_password], check=True)

    subprocess.run(["poetry", "update"], check=True)
    subprocess.run(["poetry", "install", "--all-extras"], check=True)
