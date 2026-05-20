from launcher.launcher_paths import get_config_file

DEFAULT_VERSION = "1.20.1"


def save_selected_version(version):
    config_file = get_config_file()

    with open(config_file, "w", encoding="utf-8") as file:
        file.write(version)


def load_selected_version():
    config_file = get_config_file()

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            version = file.read().strip()

            if version:
                return version

    except FileNotFoundError:
        pass

    return DEFAULT_VERSION