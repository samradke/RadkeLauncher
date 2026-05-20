import subprocess
import minecraft_launcher_lib

from launcher.launcher_paths import get_launcher_directory


def install_minecraft(version, callback=None):
    minecraft_directory = get_launcher_directory()

    if callback:
        callback(f"Verificando/instalando Minecraft {version}...")

    minecraft_launcher_lib.install.install_minecraft_version(
        version,
        minecraft_directory
    )

    if callback:
        callback("Minecraft instalado/verificado com sucesso!")


def launch_minecraft(version, callback=None):
    minecraft_directory = get_launcher_directory()

    if callback:
        callback("Preparando para iniciar Minecraft...")

    options = minecraft_launcher_lib.utils.generate_test_options()
    options["username"] = "PlayerTeste"

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        version,
        minecraft_directory,
        options
    )

    if callback:
        callback("Abrindo Minecraft...")

    subprocess.Popen(minecraft_command)


def start_minecraft(version, callback=None):
    install_minecraft(version, callback)
    launch_minecraft(version, callback)


def get_available_versions(limit=30):
    minecraft_directory = get_launcher_directory()

    versions = minecraft_launcher_lib.utils.get_available_versions(
        minecraft_directory
    )

    result = []

    for index, version in enumerate(versions):
        result.append({
            "id": version["id"],
            "type": version["type"]
        })

        if index + 1 >= limit:
            break

    return result