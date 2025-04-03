import tomllib

with open("pyproject.toml", "rb") as project:
    data = tomllib.load(project)

NAME = data["project"]["name"]
VERSION = data["project"]["version"]
DESCRIPTION = data["project"]["description"]

USAGE = f"""
{NAME} ({VERSION})
{DESCRIPTION}

Usage:
  {NAME} [--config CONFIG_FILE] <LANGUAGE> <PROJECT_TYPE> <PROJECT_PATH>
  {NAME} [--config CONFIG_FILE] (-l | --list) [--lang LANGUAGE]
  {NAME} --todo
  {NAME} (-h | --help | --version)

Arguments:
    <LANGUAGE>      The language type for the project to create
    <PROJECT_TYPE>  The type of project to create, these are defined in the
                    config
    <PROJECT_PATH>  The path at which to create the new project.

Options:
    -l --list               list the available project types.
    --lang LANGUAGE         used in conjuntion with --list to limit the list to
                            a specific language.
    -c FILE --config=FILE   Specify the config file to use.
    --todo                  Show stuff left to implement.
    -h --help               Show this screen.
    --version               Show version.

"""
