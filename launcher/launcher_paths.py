import os

LAUNCHER_NAME = "RadkeLauncher"

def get_launcher_directory():
    appdata = os.getenv("APPDATA")
    
    if appdata:
        launcher_dir = os.path.join(appdata, LAUNCHER_NAME)
    else:
        launcher_dir = os.path.join(os.getcwd(), LAUNCHER_NAME)
    
    os.makedirs(launcher_dir, exist_ok=True)
    return launcher_dir

def get_config_file():
    return os.path.join(get_launcher_directory(), "config.txt")