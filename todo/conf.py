# bertrandterrier@codeberg/utilities/todo/conf.py

import toml
import os

FILE_PATH:str = os.path.dirname(os.path.abspath(__file__))
CONF_TMPL_PATH:str = os.path.join(FILE_PATH,"files/settings.conf")
CONF_DIR:str = os.path.expanduser("~/.todo")
CONF_PATH:str = os.path.expanduser("~/.todo/settings.conf")

UNFIN = "\033[31m✗\033[0m"
FIN = "\033[32m✔\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ------------------------------------------------- #

def check_first_time():
    if not os.path.exists(CONF_PATH):
        # Get settings
        with open(CONF_TMPL_PATH,"r") as f:
            settings = toml.load(f)
        
        # Create directory
        os.mkdir(os.path.expanduser(CONF_DIR))

        # Create settings configp

        # Create file
        with open(CONF_PATH,'w') as f:
            toml.dump(settings,f)

    return

def set_def_file(path:str) -> None:
    # Load settings file
    with open(CONF_PATH,'r') as f:
        content:dict = toml.load(f)
    

    # Change setting for default file
    content["settings"]["file"] = path

    # Save settings
    with open(CONF_PATH,'w') as f:
        toml.dump(content,f)
    print(f'  → Saved {path} as default to-do-list.')

    return

def set_conf(settings:str) -> None:
    # Load configuration settings
    with open(CONF_PATH,'r') as f:
        config:dict = toml.load(f)

    # Extract settings
    if "," in settings:
        settings:list = settings.split(',')
    else:
        settings:list = settings.split(' ')
    
    # Iterate threw setting
    for elem in settings:
        if not ":" in elem:
            continue
        
        # Split setting key from setting value
        key,val = elem.strip().split(':')

        # Set settings
        if key in config.keys():
            config[key] = val

        # Save settings
        with open(CONF_PATH,'w') as f:
            toml.dump(config,f)
        
        return
    
def get_conf() -> tuple[str,str]:
    """Loads settings and returns the table style and the default file path
    if profided.

    Returns:
        tuple[str,str]: (1) Path to default file. (2) Table settings.
    """
    # Extract directory for file
    fpath:str = os.path.abspath(__file__)
    dirname:str = os.path.dirname(fpath)

    # Create path to settings file
    settings_path:str = os.path.join(CONF_PATH)
    print(f'  → Loading {settings_path}...')

    # Load settings dictionary
    with open(settings_path,"r") as f:
        settings:dict = toml.load(f)
    
    # Extract settings
    table_style = settings["table"]
    if settings["file"] == "%NONE":
        default_file = None
    else:
        default_file = settings["file"]
    
    return (default_file,table_style)

