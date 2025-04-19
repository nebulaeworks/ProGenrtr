from pathlib import Path

## the absolute path to the project
PROJECT_ROOT: str = Path(__file__).parent.parent

## the absolute path to the fallback config
FALLBACK_PATH: str = f"{PROJECT_ROOT}/templates/fallback.ini"



def read_file(path: str) -> str:
    """!
    reads and returns a file as a string, used to turn config files into strings
    for use in unit tests.
    
    @returns a string containing the (formatting preserved) contents of the
             minimal fallback.ini template
    """
    with open(path, 'r') as f:
        return f.read()


## convenience string containing the contents of the template fallback.ini
MINIMAL_FALLBACK_INI: str = read_file("test/resources/fallback.ini")
