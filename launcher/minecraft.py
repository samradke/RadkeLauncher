import subprocess
import minecraft_launcher_lib

from launcher.launcher_paths import get_launcher_directory

def install_minecraft(version):
    minecraft_directory = get_launcher_directory()
    
    print("")
    print(f"Verificando/instalando Minecraft {version}...")
    
    minecraft_launcher_lib.install.install_minecraft_version(
        version,
        minecraft_directory
    )
    
def launch_minecraft(version):
    minecraft_directory = get_launcher_directory()
    
    print("")
    print("Preparando para iniciar o Minecraft...")
    
    options = minecraft_launcher_lib.utils.generate_test_options()
    options["username"] = "PlayerTeste"
    
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        version,
        minecraft_directory,
        options
    )
    
    print("Iniciando Minecraft...")
    subprocess.run(minecraft_command)
    
def get_available_versions():
    minecraft_directory = get_launcher_directory()
    
    return minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
    
def show_available_versions(limit=30):
    print("")
    print("Buscando versões disponíveis...")
    print("")
    
    versions = get_available_versions()
    
    for index, version in enumerate(versions):
        print(f'{version["id"]} | tipo: {version["type"]}')
        
        if index + 1 >= limit:
            break
        
    print("")
    print(f"Mostrando apenas as {limit} primeiras versões.")
    