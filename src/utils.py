from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def verbose(args: dict, msg: str):
    if args["verbose"]:
        print(msg)
    
