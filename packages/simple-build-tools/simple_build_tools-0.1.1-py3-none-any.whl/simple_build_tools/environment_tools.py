""" Write the configuration for PIP and Poetry to use Nexus as the primary source """
import configparser
import os
import subprocess
from urllib.parse import urlparse


def add_host_to_pypirc(section_name, host, repository, username, password):
    """
    Add to pypirc file.  Make sure that repository starts with /.  You have to add it
    so you can add a port.

    do NOT put the port on the "host" variable

    ex.
        host = pypi.org
        repository = :9091/repository/pypi-group
        repository = /repository/pypi-release

    :param section_name:
    :param host:
    :param repository:
    :param username:
    :param password:
    :return:
    """

    repository = repository.rstrip("/")

    # Read the existing .pypirc file
    # Define the path to the .pypirc file
    home_folder = os.path.expanduser("~")
    pypirc_file = os.path.join(home_folder, ".pypirc")
    config = configparser.ConfigParser()
    config.read(pypirc_file)

    # Update or add the sections and options as needed
    if section_name not in config:
        config.add_section(section_name)

    config.set(section_name, "repository", f"https://{host}{repository}/")
    if not username and config.has_option(section_name, "username"):
        config.remove_option(section_name, "username")
    else:
        config.set(section_name, "username", username)
    if not password and config.has_option(section_name, "password"):
        config.remove_option(section_name, "password")
    else:
        config.set(section_name, "password", password)

    if 'distutils' not in config:
        config.add_section('distutils')
    if config.has_option('distutils', 'index-servers'):
        indexes = config.get("distutils", "index-servers")
    else:
        indexes = ""
    if section_name not in indexes:
        if indexes:
            indexes = indexes + "\n"
        indexes = indexes + section_name
        config.set("distutils", "index-servers", indexes)

    # Save the updated .pypirc file
    with open(pypirc_file, "w") as configfile:
        config.write(configfile)


def add_to_gitignore():
    # Read the credentials from the external file (credentials.ini)
    # Please do NOT commit this to your repository!

    # Define the file to check and the line to add
    file_to_check = '.gitignore'
    line_to_add = 'credentials.ini\n'

    # Check if the line is already in the file
    if not os.path.isfile(file_to_check):
        with open(file_to_check, 'w') as gitignore_file:
            gitignore_file.write(line_to_add)
    else:
        with open(file_to_check, 'r') as gitignore_file:
            lines = gitignore_file.readlines()

        if line_to_add not in lines:
            with open(file_to_check, 'a') as gitignore_file:
                gitignore_file.write(line_to_add)


def split_url(url):
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port
    print(protocol, host, port)
    return protocol, host, port

def read_credentials(section):

    if not os.path.exists("credentials.ini"):
        print("credentials.ini file not found.  Using environment variables.")
        server_name = os.getenv("NEXUS_SERVER", "htpps://pypi.org/simple")
        username = os.getenv("NEXUS_USERNAME", "")
        password = os.getenv("NEXUS_PASSWORD", "")
        _, host, port = split_url(server_name)
        repository = "/repository/pypi" if section == "credentials-read" else "/repository/pypi-releases"
        return f"{host}:{port}", repository, username, password

    credentials_config = configparser.ConfigParser()
    files = credentials_config.read("credentials.ini")

    if files:
        # Read the username and password from the credentials.ini file
        host = credentials_config.get(section, "host")
        repository = credentials_config.get(section, "repository")
        username = credentials_config.get(section, "username")
        password = credentials_config.get(section, "password")
    else:
        host = "pypi.org"
        repository = ""
        username = ""
        password = ""

    return host, repository, username, password


def update_pip_ini(section, host, repository):
    """
    Sets the INDEX URL in pip.ini so that it points to the specified repository and can
    read python packages from there.

    :param section: set to "global" to use the global section of pip.ini.
    :param host:
    :param repository:
    :return:
    """

    repository = repository.rstrip("/")
    index_url = f"https://{host}{repository}"

    # Set trusted host and the repository location.
    #
    # Update pip.ini so that we know where to get the package.
    # In Windows, this is ~\AppData\Roaming\pip\pip.ini
    # In Linux, this is ~/.config/pip/pip.conf
    #
    # NOTE: YOU DO NOT need credentials here.  Credentials will be stored
    # in .pypirc in your $HOME folder

    commands = [
        f'pip config --user set {section}.index "{index_url}/"',
        f'pip config --user set {section}.index-url "{index_url}/simple/"',
        f'pip config --user set {section}.trusted-host "{host}"'
    ]

    for command in commands:
        subprocess.run(command, shell=True, check=True)


def setup_pypi():
    read_host, read_repository, read_username, read_password = read_credentials("credentials-read")
    add_host_to_pypirc("pypi", read_host, read_repository, read_username, read_password)
    update_pip_ini("global", read_host, read_repository)

    write_host, write_repository, write_username, write_password = read_credentials("credentials-write")
    add_host_to_pypirc("pypi-publish", write_host, write_repository, write_username, write_password)
